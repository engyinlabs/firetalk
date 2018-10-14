import sqlite3
import qrtools
import webbrowser
import cryptography.fernet as f
from user import User
import pyqrcode as qrcode
from flask import send_file
from flask import Flask, redirect, url_for, session, request, jsonify
import json
from flask_oauthlib.client import OAuth
conn=sqlite3.connect('user.db',check_same_thread=False);
c=conn.cursor()


app = Flask(__name__)
app.config['GOOGLE_ID'] = "122205084194-0uprl5t1ojun7kftp4denbkb25l7uuee.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "LwZfpJr_KLFhXB53PBEoZt3b"

app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
key1 = f.Fernet.generate_key()
k = f.Fernet(key1)

QR_URI = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="
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
        a = me.data;
        print(a);
        # print(a['email'])
        print(type(a));
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
    google_response = google.authorized_response()
    access_token = google_response["access_token"]
    #print("access toke sis "+access_token);

    print("hi", access_token);
    if google_response is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (google_response['access_token'], '')
    me = google.get('userinfo')
    print("hello");
    a=me.data;
    # obj=User(a,access_token);
    dic={
		'id': 'NULL',
		'email': 'NULL',
		'family_name' : 'NULL',
		'given_name' : 'NULL',
		'key': 'NULL'
	}
    for i,o in a.items():
         dic[i]=o;
    dic['key']=access_token
    c.execute("SELECT count(*) FROM user1 WHERE id = ?", (dic['id'],))
    data=c.fetchone()[0]
    if data==0:
        name = k.encrypt(dic['given_name'].encode('utf8'))
        family_name = k.encrypt(dic['family_name'].encode('utf8'))
        email = k.encrypt(dic['email'].encode('utf8'))
        key = k.encrypt(dic['gender'].encode('utf8'))
        c.execute("INSERT INTO user1 VALUES(?,?,?,?,?)",(dic['id'],name,family_name,email,key))
        conn.commit()
    # generating qr code which stores the encryption key and id of the user

        dict = {
            'user_id' : dic['id'],
            'key' : key.decode('utf8')
        }


        a=key1 + ','+dict['user_id']
        # .append(dict['key'])
        print()
        print()
        print()
        print()
        print('000');
       # print(type(x))
        qr = qrcode.create(a)
        qr.png('hello.png',scale=7)
        # img = qrcode.make_image(dict)
        # img.save("qrcode.png")
        print(dic)

    else:
        print();
        print();
        print();
        print();
        print();
        print("already exist");

    # dic['id']=a['id']
    # dic['email']=a['email']
    # dic['']
    #



    # # for x in a:
    # #     print(x)
    #      for y in a[x]:
    #          print(y,':',a[x][y])
    #
    # print(a['email'])
    print("byeee");

    return jsonify({"data": me.data})

# @app.route('/qrcode.png')
# def get_qrcode():
@app.route('/loginwithqr')
def loginwithqr():
    qr = qrtools.QR()
    qr.decode("hello.png")
    key, id = qr.data.split(",")
    key = key.encode()
    print(qr.data)
    qr = qrtools.QR()
    qr.decode("hello.png")
    key, id = qr.data.split(",")
    # key = key.encode('utf8')
    key = key.encode()
    k = f.Fernet(key)
    conn = sqlite3.connect("user.db")

    cur = conn.cursor()

    user_id = id
    cur.execute("SELECT * from user1 WHERE id=?", (user_id,))
    rows = cur.fetchall()
    user_info = []
    for i in range(len(rows)):
        for j in range(1, len(rows[0])):
            user_info.append(k.decrypt((rows[i][j]).encode()))

    for i in user_info:
        print(i)

    return jsonify(user_info)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


if __name__ == '__main__':
    app.run()


conn.close()

