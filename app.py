from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# Cognito Configuration (all values loaded from .env — no defaults to avoid leaking secrets)
COGNITO_REGION = os.environ['COGNITO_REGION']
COGNITO_USER_POOL_ID = os.environ['COGNITO_USER_POOL_ID']
COGNITO_CLIENT_ID = os.environ['COGNITO_CLIENT_ID']
COGNITO_CLIENT_SECRET = os.environ['COGNITO_CLIENT_SECRET']
COGNITO_DOMAIN = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}'

oauth = OAuth(app)

oauth.register(
    name='oidc',
    client_id=COGNITO_CLIENT_ID,
    client_secret=COGNITO_CLIENT_SECRET,
    server_metadata_url=f'{COGNITO_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={'scope': 'email openid phone'}
)


@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'''
        <html>
        <head><title>Cognito POC - Logged In</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; text-align: center;">
            <h1>Welcome!</h1>
            <p>Hello, <strong>{user.get("email", "User")}</strong></p>
            <p>Sub: {user.get("sub", "N/A")}</p>
            <hr>
            <a href="/profile" style="margin-right: 20px;">View Profile</a>
            <a href="/logout" style="color: red;">Logout</a>
        </body>
        </html>
        '''
    else:
        return '''
        <html>
        <head><title>Cognito POC - Login</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; text-align: center;">
            <h1>Cognito POC Test App</h1>
            <p>Welcome! Please log in to continue.</p>
            <a href="/login" style="display: inline-block; padding: 10px 30px; background-color: #007bff;
               color: white; text-decoration: none; border-radius: 5px; font-size: 16px;">
               Login with Cognito
            </a>
        </body>
        </html>
        '''


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    try:
        token = oauth.oidc.authorize_access_token()
        user = token.get('userinfo')
        if user:
            session['user'] = user
        return redirect(url_for('index'))
    except Exception as e:
        return f'''
        <html>
        <head><title>Auth Error</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; text-align: center;">
            <h1>Authentication Error</h1>
            <p style="color: red;">{str(e)}</p>
            <a href="/">Back to Home</a>
        </body>
        </html>
        ''', 500


@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return jsonify(user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
