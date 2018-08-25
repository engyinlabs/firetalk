import webbrowser
from flask import Flask, redirect, url_for, session, request, jsonify

from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.config['GOOGLE_ID'] = "403847176041-1a3qahjkf5m786p54qhu5u5c2qvt0rkt.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "2YyK88tfPFMDXwtm-2p8kQC9"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

Qruri = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/oauth2callback')
def authorized():
    resp = google.authorized_response()
    access_token = resp["access_token"]
    qr_final_uri = Qruri + access_token

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    webbrowser.open_new_tab(qr_final_uri)
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


if __name__ == '__main__':
    app.run()

