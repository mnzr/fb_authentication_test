# config.py
from authomatic.providers import oauth2, oauth1, openid

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

HOST = 'localhost'
PORT = 28015
DB = 'fbgrabber'
TABLE_STATUS_MESSAGE = 'statuses'
TABLE_LINK_DESC = 'links'
TABLE_PAGE_ABOUT = 'page'


CONFIG = {

    'tw': {  # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other
        # properties too:
        'consumer_key': '########################',
        'consumer_secret': '########################',
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1732750360274136',
        'consumer_secret': 'f15127605879b24f03651c38f7bb9663',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'user_posts', 'user_likes'],  # , 'publish_stream'
    },

    'oi': {

        # OpenID provider dependent on the python-openid package.
        'class_': openid.OpenID,
    }
}
