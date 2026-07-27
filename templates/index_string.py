from __future__ import annotations

INDEX_PAGE_STRING = """
<!DOCTYPE html>
<html lang="es">
    <head>
        {%metas%}

        <meta name="theme-color" content="#000000">
        <meta name="background-color" content="#ffffff">

        <meta name="application-name" content="__APP_SHORT_NAME__">
        <meta name="apple-mobile-web-app-title" content="__APP_SHORT_NAME__">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">

        <meta name="mobile-web-app-capable" content="yes">
        <meta name="format-detection" content="telephone=no">

        <title>{%title%}</title>

        <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="167x167" href="/apple-touch-icon-167x167.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=__APP_VERSION__">
        <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-precomposed.png?v=__APP_VERSION__">

        <link rel="manifest" href="/manifest.webmanifest?v=__APP_VERSION__" crossorigin="use-credentials">

        <link rel="icon" sizes="192x192" href="/assets/img/branding/logos/web-app-manifest-192x192.png?v=__APP_VERSION__">
        <link rel="icon" sizes="512x512" href="/assets/img/branding/logos/web-app-manifest-512x512.png?v=__APP_VERSION__">
        <link rel="icon" href="/assets/favicon.ico?v=__APP_VERSION__" type="image/x-icon">

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">

        {%favicon%}
        {%css%}

    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


def get_index_page_string() -> str:
    return INDEX_PAGE_STRING