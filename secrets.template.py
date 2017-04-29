# https://dev.moves-app.com/docs/authentication

# Go to this URL on desktop, then enter the PIN in the mobile app, then wait
# for the desktop browser to redirect and copy 'code' below.
# https://api.moves-app.com/oauth/v1/authorize?response_type=code&client_id=<client_id>&scope=location&scope=activity

# Then run `python daily_report.py --moves-token


moves = {
    'client_id': '',
    'client_secret': '',
    'code': '',

    'access_token': ''
}

jawbone = {
    'client_id': '',
    'app_secret': '',

    'access_token': ''
}
