# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from account.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import GeneratedModel
from ranking.models import TextGenHistory

import logging
from datetime import datetime
import urllib
from requests_oauthlib import OAuth1Session
import MeCab
import markovify

# Image draw
import io
from PIL import Image, ImageDraw, ImageFont

from . import generate_model

logger = logging.getLogger('django')
mec = MeCab.Tagger("-r /dev/null -d /usr/lib/mecab/dic/ipadic-utf8 -O wakati")

class AuthRedirectAPIView(APIView):
    def get(self, request):
        if 'callback' not in request.query_params:
            return Response(
                {
                    'message': 'callback URL not specified!'
                },
                status.HTTP_400_BAD_REQUEST
            )
        oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, None, None, request.query_params['callback'])
        oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
        url = oauth.authorization_url("https://api.twitter.com/oauth/authenticate")
        return redirect(url)

def twitter_fetch_token(request):
    oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, None, None)
    oauth.parse_authorization_response(request.build_absolute_uri())
    token = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
    return token

class AuthAndGenAPIView(APIView):
    def get(self, request):
        try:
            token = twitter_fetch_token(request)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown=true')
        oauth_token = token["oauth_token"]
        oauth_token_secret = token["oauth_token_secret"]
        oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, oauth_token, oauth_token_secret)
        twitter_id = token['user_id']
        screen_name = token['screen_name']

        try:
            tuser = oauth.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name)
            tuser_data = tuser.json()
            is_protected = tuser_data['protected']
            avatar_url = tuser_data['profile_image_url_https']
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown=true')

        if User.objects.filter(screen_name__iexact=screen_name).exists():
            user = User.objects.get(screen_name__iexact=screen_name)
            if user.twitter_id != twitter_id:
                User.objects.filter(screen_name__iexact=screen_name).delete()
        if User.objects.filter(twitter_id=twitter_id).exists():
            user = User.objects.get(twitter_id=twitter_id)
            user.screen_name = screen_name
            user.is_protected = is_protected
            user.avatar_url = avatar_url
            # don't save oauth token
            # user.access_token = oauth_token
            # user.access_token_secret = oauth_token_secret
            user.save()
            login(request, user)
        else:
            user = User.objects.create_user(screen_name, avatar_url, twitter_id, is_protected)
            # don't save oauth token
            # user.access_token = oauth_token
            # user.access_token_secret = oauth_token_secret
            user.save()
            login(request, user)

        if GeneratedModel.objects.filter(user=user).exists():
            genmodel = GeneratedModel.objects.get(user=user)
            if datetime.now().timestamp() - genmodel.date.timestamp() < 60 * 60 * 24:
                return redirect('/?error_24hour_constraint=true')
            GeneratedModel.objects.filter(user=user).delete()

        # Generate model
        params = { "screen_name": screen_name, "trim_user": 1 }
        try:
            model = generate_model.generate_from_tweets(oauth, params)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown=true')
        modeljson = model.to_json()
        genmodel = GeneratedModel()
        genmodel.user = user
        genmodel.model = modeljson
        genmodel.save()
        logger.info('LOG:MODELGEN:{}'.format(screen_name))

        return redirect('/{}?successfully_generated=true'.format(screen_name))

class AuthAndDelAPIView(APIView):
    def get(self, request):
        try:
            token = twitter_fetch_token(request)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown=true')
        twitter_id = token['user_id']
        if User.objects.filter(twitter_id=twitter_id).exists():
            user = User.objects.get(twitter_id=twitter_id)
            if GeneratedModel.objects.filter(user=user).exists():
                GeneratedModel.objects.filter(user=user).delete()
                return redirect('/' + '?successfully_deleted=true')
        return redirect('/' + '?error_deleted=true')

class GenTextAPIView(APIView):
    def get(self, request, screen_name):
        formatted_screen_name = ''
        screen_name_list = screen_name.split(',')
        if 10 < len(screen_name_list):
            return Response(
                {
                    'status': False,
                    'message': '10??????????????????????????????????????????????????????',
                },
                status.HTTP_400_BAD_REQUEST,
            )

        model_list = []
        weight_list = []
        for screen_name in screen_name_list:
            weight = 1
            screen_name = screen_name.split(':')
            if 1 < len(screen_name):
                try:
                    weight = float(screen_name[1])
                except ValueError:
                    return Response(
                        {
                            'status': False,
                            'message': '?????????????????????????????????',
                        },
                        status.HTTP_400_BAD_REQUEST,
                    )
            screen_name = screen_name[0]
            screen_name = screen_name.lstrip('@')
            if 0 < len(formatted_screen_name):
                formatted_screen_name += ','
            formatted_screen_name += screen_name
            if weight != 1:
                formatted_screen_name += ":{}".format(weight)

            # Fetch user data
            try:
                user = User.objects.get(screen_name__iexact=screen_name)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'status': False,
                        'message': '??????????????????????????????????????????????????????'
                    },
                    status.HTTP_404_NOT_FOUND
                )
            if user.is_protected and (not request.user.is_authenticated or request.user.id != user.id):
                return Response(
                    {
                        'status': False,
                        'message': '????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????'
                    },
                    status.HTTP_401_UNAUTHORIZED
                )

            # Fetch markov-chain model
            try:
                model = GeneratedModel.objects.get(user=user)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'status': False,
                        'message': '??????????????????????????????????????????????????????'
                    },
                    status.HTTP_404_NOT_FOUND
                )
            markov = markovify.Text.from_json(model.model)

            model_list.append(markov)
            weight_list.append(weight)
        if 1 < len(model_list):
            markov = markovify.combine(model_list, weight_list)
        elif len(model_list) == 1:
            markov = model_list[0]
        else:
            return Response(
                {
                    'status': False,
                    'message': '?????????????????????????????????',
                },
                status.HTTP_400_BAD_REQUEST,
            )


        if request.query_params.get('startWith') and 0 < len(request.query_params['startWith'].strip()):
            startWithStr = mec.parse(request.query_params['startWith']).strip().split()
            if markov.state_size < len(startWithStr):
                startWithStr = startWithStr[0:markov.state_size]
            startWithStr = " ".join(startWithStr)
            try:
                text = markov.make_sentence_with_start(startWithStr, tries=100)
            except Exception:
                return Response(
                    {
                        'status': False,
                        'message': '??????????????????????????????????????????????????????'
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        elif request.query_params.get('length') and str(request.query_params['length']).isdecimal() and 0 < int(request.query_params['length']):
            text = markov.make_short_sentence(int(request.query_params['length']), tries=100)
        else:
            text = markov.make_sentence(tries=100)

        if text is None:
            return Response(
                {
                    'status': False,
                    'message': '??????????????????????????????????????????????????????'
                },
                status.HTTP_400_BAD_REQUEST
            )
        text = "".join(text.split())
        logger.info('LOG:TEXTGEN:{}:{}'.format(screen_name, text))
        text_gen_history = TextGenHistory()
        text_gen_history.target_user = user
        if request.user.is_authenticated:
            text_gen_history.request_from = request.user
        else:
            text_gen_history.request_from = None
        text_gen_history.save()
        return Response(
            {
                'status': True,
                'sentence': text,
                'avatarUrl': user.avatar_url
            },
        )

def wrap_text(img, text, font_size, max_length):
    font = ImageFont.truetype("assets/OpenSans-Bold.ttf", font_size)
    draw = ImageDraw.Draw(img)
    text_list = [text]
    while max_length < draw.textsize(text_list[-1], font=font)[0]:
        test_text = text_list[-1]
        while max_length < draw.textsize(test_text, font=font)[0]:
            test_text = test_text[:-1]
        text_list.append(text_list[-1][len(test_text):])
        text_list[-2] = test_text
    return text_list

def add_text_to_image(img, text, font_size, font_color, max_length=1000):
    font = ImageFont.truetype("assets/OpenSans-Bold.ttf", font_size)
    draw = ImageDraw.Draw(img)
    wrapped_text = wrap_text(img, text, font_size, max_length)
    if 2 < len(wrapped_text):
        wrapped_text = wrapped_text[:2]
        wrapped_text[-1] += '???'
    w, h = img.size
    for i, t in enumerate(wrapped_text):
        position = (w / 2 - draw.textsize(t, font=font)[0] / 2, 375 - (len(wrapped_text) - 1) * font_size / 2 + i * font_size)
        draw.text(position, t, font_color, font=font)
    return img

class GenImageAPIView(APIView):
    def get(self, request, screen_name=None):
        if screen_name is None:
            screen_name = ''
        screen_name = screen_name.lstrip('@')
        img = Image.open('assets/user_og_image_base.png')
        add_text_to_image(img, '@' + screen_name, 100, (0, 0, 0))
        file_obj = io.BytesIO()
        img.save(file_obj, 'PNG')
        file_obj.seek(0)
        fr = FileResponse(file_obj)
        fr['Content-Type'] = 'image/PNG'
        return fr
