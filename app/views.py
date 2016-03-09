# Views are where the routes are defined
from pprint import pprint
import rethinkdb as r
from rethinkdb import RqlRuntimeError
from flask import render_template, request, g, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import *
from app import app


# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, SECRET_KEY, report_errors=False)


@app.before_request
def before_request():
    g.db = r.connect(host=HOST, port=PORT, db=DB)


@app.teardown_request
def teardown_request(exception):
    g.db.close()


# Root for the test site
@app.route('/')
def index():
    """
    Home handler
    """

    return render_template('index.html')


@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """

    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response),
                              provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
        # The rest happens inside the template.
        return render_template('login.html', result=result)

    # Don't forget to return the response.
    return response
