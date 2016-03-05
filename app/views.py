# Views are where the routes are defined
from pprint import pprint
import rethinkdb as r
from rethinkdb import RqlRuntimeError
from flask import render_template, url_for, request, g, redirect, make_response
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
        # pprint(vars(result.user), indent=4, depth=1, width=2)
        if result.user.credentials:
            """
            status: message
            page_like: about
            shared_link: description
            """
            # save_status_message(result)
            # save_links_desc(result)
            save_to_db(save_page_about(result), table=TABLE_PAGE_ABOUT)

            # Insert the user's ID to the URL and access the resource.

        # The rest happens inside the template.
        return render_template('login.html', result=result)

    # Don't forget to return the response.
    return response


def save_status_message(result):
    # For link descriptions
    url = 'https://graph.facebook.com/{0}?fields=feed.limit(100){{message,status_type}}'.format(result.user.id)
    response = result.provider.access(url)
    links_entry = {
        'user_id': result.user.id,
        'messages': []
    }
    if response.status == 200:
        if response.data['feed']['data']:
            for status in response.data['feed']['data']:
                if status['status_type'] == 'mobile_status_update' and 'message' in status:
                    # pprint(status['description'], indent=4, depth=4)
                    links_entry['messages'].append(status['message'])
            pprint(links_entry, indent=4, depth=4)
            return links_entry
    else:
        print("Error code [%s]" % response.status)

def save_page_about(result):
    # For link descriptions
    url = 'https://graph.facebook.com/{0}?fields=likes.limit(100){{about}}'.format(result.user.id)
    response = result.provider.access(url)
    links_entry = {
        'user_id': result.user.id,
        'messages': []
    }
    if response.status == 200:
        if response.data['likes']['data']:
            for likes in response.data['likes']['data']:
                if 'about' in likes:
                    # pprint(status['description'], indent=4, depth=4)
                    links_entry['messages'].append(likes['about'])
            pprint(links_entry, indent=4, depth=4)
            return links_entry
    else:
        print("Error code [%s]" % response.status)

def save_links_desc(result):
    # For link descriptions
    url = 'https://graph.facebook.com/{0}?fields=feed.limit(10){{link,description,type}}'.format(result.user.id)
    response = result.provider.access(url)
    entry = {
        'user_id': result.user.id,
        'messages': []
    }
    if response.status == 200:
        if response.data['feed']['data']:
            for status in response.data['feed']['data']:
                if status['type'] == 'link' and 'description' in status:
                    # pprint(status['description'], indent=4, depth=4)
                    entry['messages'].append(status['description'])
            pprint(entry, indent=4, depth=4)
            return entry
    else:
        print("Error code [%s]" % response.status)


def setup_db(table):
    """to setup a DB"""
    try:
        r.db_create(DB).run(g.db)
        r.db(DB).table_create(table).run(g.db)
        print('Using newly created database.')
    except RqlRuntimeError:
        print('Using existing database.')

def save_to_db(entry, table):
    setup_db(table=table)
    #db_entries = r.db(DB).table(table).run(g.db)
    # r.db(DB).table(table).insert(entry).run(g.db)
    db_entries = list(r.db(DB).table(table).run(g.db))
    try:
        if r.table(table).filter({"user_id": entry['user_id']}).run(g.db):
            print("exists")
            existing_entry = list(r.table(table).filter({"user_id": entry['user_id']}).run(g.db))
            for message in entry['messages']:
                for m in existing_entry:
                    if message in m['messages']:
                        continue
                    r.table(table).filter({"user_id": entry['user_id']}).update({"messages":
                                                                                r.row["messages"].append(message)
                                                                            }).run(g.db)
                    print("Appended successfully")


    except RqlRuntimeError:
        print('baler matha')
        #r.table("posts").filter({"author": "William"}).update({"status": "published"}).run(conn)for e in db_entries:
        # print(e['user_id'])
    """
    for e in db_entries:
        if 'user_id' in e and entry['user_id'] == e['user_id']:
            print('baler matha')
            # add the entry['messages']
        else:
            print('naikka')
            
    # if entry['user_id'] in [x['user_id'] for x in r.db(DB).table(table).run(g.db)]:
    #     print('baler matha')
        """