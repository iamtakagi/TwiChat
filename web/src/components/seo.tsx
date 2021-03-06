import Head from "next/head";
import React from "react";

export const Seo: React.FC<{
  pageSubTitle?: string;
  ogImageUrl?: string;
}> = ({ pageSubTitle, ogImageUrl }) => {
  return (
    <Head>
      <meta charSet="UTF-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0" />
      <meta name="referrer" content="origin" />
      <link rel="preconnect" href="https://cdn.jsdelivr.net" />
      <link rel="stylesheet" href="./style.css" />
      <meta
        name="msapplication-square70x70logo"
        content="./favicons/site-tile-70x70.png"
      />
      <meta
        name="msapplication-square150x150logo"
        content="./favicons/site-tile-150x150.png"
      />
      <meta
        name="msapplication-wide310x150logo"
        content="./favicons/site-tile-310x150.png"
      />
      <meta
        name="msapplication-square310x310logo"
        content="./favicons/site-tile-310x310.png"
      />
      <meta name="msapplication-TileColor" content="#0078d7" />
      <link
        rel="shortcut icon"
        type="image/vnd.microsoft.icon"
        href="./favicons/favicon.ico"
      />
      <link
        rel="icon"
        type="image/vnd.microsoft.icon"
        href="./favicons/favicon.ico"
      />
      <link
        rel="apple-touch-icon"
        sizes="57x57"
        href="./favicons/apple-touch-icon-57x57.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="60x60"
        href="./favicons/apple-touch-icon-60x60.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="72x72"
        href="./favicons/apple-touch-icon-72x72.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="76x76"
        href="./favicons/apple-touch-icon-76x76.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="114x114"
        href="./favicons/apple-touch-icon-114x114.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="120x120"
        href="./favicons/apple-touch-icon-120x120.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="144x144"
        href="./favicons/apple-touch-icon-144x144.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="152x152"
        href="./favicons/apple-touch-icon-152x152.png"
      />
      <link
        rel="apple-touch-icon"
        sizes="180x180"
        href="./favicons/apple-touch-icon-180x180.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="36x36"
        href="./favicons/android-chrome-36x36.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="48x48"
        href="./favicons/android-chrome-48x48.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="72x72"
        href="./favicons/android-chrome-72x72.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="96x96"
        href="./favicons/android-chrome-96x96.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="128x128"
        href="./favicons/android-chrome-128x128.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="144x144"
        href="./favicons/android-chrome-144x144.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="152x152"
        href="./favicons/android-chrome-152x152.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="192x192"
        href="./favicons/android-chrome-192x192.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="256x256"
        href="./favicons/android-chrome-256x256.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="384x384"
        href="./favicons/android-chrome-384x384.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="512x512"
        href="./favicons/android-chrome-512x512.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="36x36"
        href="./favicons/icon-36x36.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="48x48"
        href="./favicons/icon-48x48.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="72x72"
        href="./favicons/icon-72x72.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="96x96"
        href="./favicons/icon-96x96.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="128x128"
        href="./favicons/icon-128x128.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="144x144"
        href="./favicons/icon-144x144.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="152x152"
        href="./favicons/icon-152x152.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="160x160"
        href="./favicons/icon-160x160.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="192x192"
        href="./favicons/icon-192x192.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="196x196"
        href="./favicons/icon-196x196.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="256x256"
        href="./favicons/icon-256x256.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="384x384"
        href="./favicons/icon-384x384.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="512x512"
        href="./favicons/icon-512x512.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="16x16"
        href="./favicons/icon-16x16.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="24x24"
        href="./favicons/icon-24x24.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="32x32"
        href="./favicons/icon-32x32.png"
      />
      <link rel="manifest" href="./favicons/manifest.json" />

      <title>
        TwiChat / {pageSubTitle ? pageSubTitle : "????????????????????????????????????"}
      </title>
      <meta property="description" content="????????????????????????????????????" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@919takagi" />
      <meta
        property="og:title"
        content={`TwiChat / ${
          pageSubTitle ? pageSubTitle : "????????????????????????????????????"
        }`}
      />
      <meta property="og:description" content="????????????????????????????????????" />
      <meta
        property="og:site_name"
        content="TwiChat / ????????????????????????????????????"
      />
      <meta
        property="og:image"
        content={
          ogImageUrl ? ogImageUrl : "https://twichat.iamtakagi.net/images/og_image.png"
        }
      />
      <meta property="og:type" content="website" />
      <meta property="og:url" content="https://twichat.iamtakagi.net" />
    </Head>
  );
};
