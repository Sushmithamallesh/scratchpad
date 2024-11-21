from flask import Flask, redirect, request, session, url_for
from flask_session import Session
import praw
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = tempfile.gettempdir()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False

app.permanent_session_lifetime = timedelta(minutes=5)

# Initialize PRAW (Reddit API)
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    redirect_uri="http://localhost:8080/reddit_callback",
    user_agent="rep.ly",
)


@app.route("/")
def home():
    app.logger.debug(f"Home route - Session state: {session.get('state')}")
    return """
        <h1>Welcome to MyApp</h1>
        <a href="/login">Login with Reddit</a>
    """


@app.route("/login")
def login():
    state = os.urandom(16).hex()
    session["state"] = state
    session.modified = True
    session.permanent = True
    app.logger.debug(f"Login route - Setting state in session: {state}")

    auth_url = reddit.auth.url(
        scopes=["identity", "read", "submit"], state=state, duration="permanent"
    )
    return redirect(auth_url)


@app.route("/reddit_callback")
def reddit_callback():
    app.logger.debug(f"Callback route - Session state: {session.get('state')}")
    app.logger.debug(f"Callback route - Request state: {request.args.get('state')}")
    app.logger.debug(f"Session contents: {session}")

    error = request.args.get("error")
    if error:
        return f"Error during authorization: {error}", 400

    state = request.args.get("state")
    code = request.args.get("code")

    # Logging for debugging
    app.logger.debug(f"Received state: {state}")
    app.logger.debug(f"Session state: {session.get('state')}")
    app.logger.debug(f"Received code: {code}")

    if state is None or state != session.get("state"):
        return "State mismatch. Possible CSRF attack or session expired.", 403

    try:
        refresh_token = reddit.auth.authorize(code)
        return f"Login successful! Refresh token: {refresh_token}"
    except praw.exceptions.OAuthException as e:
        app.logger.error(f"OAuthException: {e}")
        return f"Error during authorization: {str(e)}", 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return (f"Unexpected error: {str(e)}",)


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, port=8080)  # pragma: no cover
