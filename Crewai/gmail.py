import base64
from email.header import decode_header
import json
import os
import pickle
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    # Call the Gmail API to fetch inbox for the mails received in last 10 hours
    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            q="after: {0}".format(
                (datetime.datetime.now() - datetime.timedelta(hours=10)).strftime(
                    "%Y/%m/%d"
                )
            ),
        )
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No new messages.")
    else:
        print("Messages:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )

            # Get the email data
            payload = msg["payload"]
            headers = payload["headers"]

            # Save the subject and body in a file
            with open(f"mails/{message['id']}.txt", "w") as f:
                # write subject and body
                for d in headers:
                    if d["name"] == "Subject":
                        subject = d["value"]
                        # Decode the subject
                        subject = decode_header(subject)
                        subject = (
                            subject[0][0].decode(subject[0][1])
                            if subject[0][1]
                            else subject[0][0]
                        )
                f.write(subject)
                f.write(json.dumps(payload["body"]))

                # Get the body of the email
                parts = payload.get("parts", [])
                if parts:
                    data = parts[0]["body"]["data"]
                    data = data.replace("-", "+").replace("_", "/")
                    decoded_data = base64.b64decode(data)
                    body = decoded_data.decode()
                    f.write(body)


if __name__ == "__main__":
    main()
