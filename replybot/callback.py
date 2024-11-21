from flask import Flask, request

app = Flask(__name__)


@app.route("/reddit_callback")
def reddit_callback():
    code = request.args.get("code")
    # Process the code (e.g., exchange it for a token)
    return "Authorization successful!"


if __name__ == "__main__":
    app.run(port=8000)
