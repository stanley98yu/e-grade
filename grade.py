import os.path
import io
import json
import csv
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import mail_client

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def auth():
    """Performs authorization flow that generates a token if it 
    doesn't exist. Must have a 'credentials.json' file in directory.
    """
    creds = None

    # token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def find_sheet(service):
    """Finds the spreadsheet containing the name of the spreadsheet."""
    while True:
        # Performs search query.
        name = input("Enter the name of your spreadsheet: ")
        query = "name contains '" + name + "'"
        query += " and mimeType='application/vnd.google-apps.spreadsheet'" # Spreadsheets only
        resp = json.dumps(service.files().list(q=query, spaces='drive').execute())
        files = json.loads(resp)["files"]
        sid = None

        # Confirms matching files with user.
        valid = {"y": True, "ye": True, "yes": True,
                 "n": False, "no": False, "r": False}
        i = 0
        while i < len(files):
            prompt = input("Is '" + files[i]["name"] + "' the file you want? [y/n/r] ")
            while prompt not in valid:
                prompt = input("Please enter either 'y' or 'n'. To retry your search, enter 'r': ")
            
            if prompt == "r": break
            elif valid[prompt]:
                sid = files[i]["id"]
                break
            else: i += 1
        
        if sid: return sid
        else: print("No matching file found. Try again.")

def dl_sheet(service, sid):
    """Downloads spreadsheet information and returns a table of values.
    If you are interested in using this script for yourself, you may have to
    change the format of the table to fit your grading sheet."""
    resp = service.files().export_media(fileId=sid, mimeType='text/csv').execute()

    # Parse comma-separated values and tabularize grades. Returns a list of 
    # dictionaries for each student.
    lines = resp.decode('utf-8').split('\r\n')
    headers = lines[0].split(',')
    tb = []
    tmp = csv.reader(lines[1:], skipinitialspace=True)
    for r in tmp:
        student = {}
        i = 0
        while i < len(headers):
            student[headers[i]] = r[i]
            i += 1
        tb.append(student)
    return tb

if __name__ == '__main__':
    # Build service
    creds = auth()
    service = build('drive', 'v3', credentials=creds)

    sid = find_sheet(service)
    tb = dl_sheet(service, sid)

    smtp_serv = mail_client.SMTPServer()
    hw_num = input("Enter homework #: ")
    print("Sending emails...")
    for student in tb:
        smtp_serv.send_grade(student, "HW" + hw_num)
    print("Done!")
