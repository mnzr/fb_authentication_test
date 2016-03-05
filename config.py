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
        'consumer_key': '548717931973687',
        'consumer_secret': '40ca3d9b536946bfb6818c27fd8dda8b',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'user_posts'],  # , 'publish_stream'
    },

    'oi': {

        # OpenID provider dependent on the python-openid package.
        'class_': openid.OpenID,
    }
}
