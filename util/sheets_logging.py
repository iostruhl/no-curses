import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Sheet ID and range
OH_HELL_SHEET_ID = '1YMAGaRRk8fyXrDx_AK-gkubVFqKnrK9p8CE9znAfZKw'
OH_HELL_SHEET_RANGE = 'Scores!B3:F'
OH_HELL_HAND_SHEET_RANGE = 'Hand_Raw_Data!A2:D'

# set up credentials
creds = None

# load creds from storage if possible
if os.path.exists(os.path.join(os.path.dirname(__file__), "token.pickle")):
    with open(os.path.join(os.path.dirname(__file__), "token.pickle"),
              'rb') as token:
        creds = pickle.load(token)
# create creds if necessary
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(os.path.dirname(__file__), "credentials.json"),
            SCOPES)
        creds = flow.run_local_server()
    # save credentials for next run
    with open(os.path.join(os.path.dirname(__file__), "token.pickle"),
              'wb') as token:
        pickle.dump(creds, token)

# create hook to api
service = build('sheets', 'v4', credentials=creds)


# [[name, hand_num, bid, tricks_taken], ...(4)]
def log_hand(raw_hand_data: list):
    print("LOGGING HAND")
    result = service.spreadsheets().values().get(
        spreadsheetId=OH_HELL_SHEET_ID,
        range=OH_HELL_HAND_SHEET_RANGE).execute()

    values = result.get('values', [])
    row_add_range = 'Hand_Raw_Data!A%d:D' % (len(values) + 2)
    print("updating to", row_add_range)
    print(raw_hand_data)

    result = service.spreadsheets().values().append(
        spreadsheetId=OH_HELL_SHEET_ID,
        range=row_add_range,
        valueInputOption="USER_ENTERED",
        body={
            'values': raw_hand_data
        }).execute()
    print(result)


def log_game(gamescores: dict):
    print("LOGGING GAME")
    result = service.spreadsheets().values().get(
        spreadsheetId=OH_HELL_SHEET_ID, range=OH_HELL_SHEET_RANGE).execute()

    values = result.get('values', [])
    row_add_range = 'Scores!B%d:F' % (len(values) + 3)
    print("updating to", row_add_range)

    result = service.spreadsheets().values().append(
        spreadsheetId=OH_HELL_SHEET_ID,
        range=row_add_range,
        valueInputOption="USER_ENTERED",
        body={
            'values': [[
                gamescores["Ben Harpe"] if "Ben Harpe" in gamescores else '',
                gamescores["Alex Mariona"] if "Alex Mariona" in gamescores else
                '', gamescores["Owen Schafer"] if "Owen Schafer" in gamescores
                else '', gamescores["Isaac Struhl"]
                if "Isaac Struhl" in gamescores else '',
                gamescores["Alex Wulff"] if "Alex Wulff" in gamescores else '',
                gamescores["Joey Minatel"] if "Joey Minatel" in gamescores else ''
            ]]
        }).execute()
    print(result)


# testing log_game
if __name__ == '__main__':
    log_game({
        "Alex Mariona": 240,
        "Owen Schafer": 150,
        "Ben Harpe": 140,
        "Alex Wulff": 130
    })
