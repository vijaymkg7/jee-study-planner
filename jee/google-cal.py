from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define OAuth 2.0 scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_info():
    """Authenticate and fetch the list of calendars."""
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the token for future use
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    # Connect to Google Calendar API
    service = build("calendar", "v3", credentials=creds)

    # Get the list of calendars
    calendar_list = service.calendarList().list().execute()

    # Display the calendars
    for calendar in calendar_list.get("items", []):
        print(f"Calendar Name: {calendar['summary']}")
        print(f"Calendar ID: {calendar['id']}\n")

if __name__ == "__main__":
    get_calendar_info()
