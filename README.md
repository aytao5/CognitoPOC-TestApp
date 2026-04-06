# Cognito POC Test App

A simple Flask app that demonstrates Amazon Cognito authentication using OpenID Connect (OIDC) via authlib.

## Prerequisites

- Python 3.8+
- An Amazon Cognito User Pool with an App Client configured
- The App Client must have `http://localhost:5000/authorize` as an allowed callback URL

## Setup

1. **Install dependencies:**
   ```bash
   pip install authlib werkzeug flask requests python-dotenv
   ```

2. **Configure environment variables:**
   
   Copy the example file and fill in your actual values:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and replace the placeholders with your real Cognito credentials:
   ```
   COGNITO_REGION=us-east-2
   COGNITO_USER_POOL_ID=your-actual-pool-id
   COGNITO_CLIENT_ID=your-actual-client-id
   COGNITO_CLIENT_SECRET=your-actual-client-secret
   FLASK_SECRET_KEY=some-secure-random-string
   ```

3. **Configure Cognito App Client (AWS Console):**
   - Go to **Amazon Cognito → User Pools → your pool → App integration → App clients**
   - Under **Allowed callback URLs**, add: `http://localhost:5000/authorize`
   - Under **Allowed sign-out URLs**, add: `http://localhost:5000`
   - Ensure **Authorization code grant** is enabled
   - Ensure **openid**, **email**, and **phone** scopes are allowed

## Run

```bash
python app.py
```

The app will start at [http://localhost:5000](http://localhost:5000).

## Routes

| Route        | Description                          |
|-------------|--------------------------------------|
| `/`         | Home page (login/welcome)            |
| `/login`    | Redirects to Cognito hosted login    |
| `/authorize`| Callback URL — handles OIDC token    |
| `/profile`  | Shows user info as JSON              |
| `/logout`   | Clears session and redirects home    |

## Notes

- For production, use a proper `FLASK_SECRET_KEY` instead of a random one.
- Never commit your `.env` file (it's in `.gitignore`).
- The redirect URI for production should be updated to your CloudFront or domain URL.
