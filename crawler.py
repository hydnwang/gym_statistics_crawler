import requests
import time
import httplib2
import os
import re
import pendulum
from pprint import pprint
from lxml import html

# from apiclient import discovery
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# "https://yhcsc.cyc.org.tw/api" 永和運動中心
# "https://xysc.cyc.org.tw/api"  信義運動中心
# "https://dasc.cyc.org.tw/api"  大安運動中心

sport_centers = {
    "永和運動中心": "https://yhcsc.cyc.org.tw/api", 
    "信義運動中心": "https://xysc.cyc.org.tw/api", 
    "大安運動中心": "https://dasc.cyc.org.tw/api"
}

sport_centers_e = {
    "中正運動中心": "http://www.tpejjsports.com.tw/zh-TW/onsitenum"
}

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'SportCenterAPI'

# CLIENT_SECRET_FILE = 'client_secret.json'
HOME = home_dir = os.path.dirname(os.path.realpath('__file__'))
secret_dir = os.path.join(HOME, '.secret')
CLIENT_SECRET_FILE = os.path.join(credential_dir, 'client_secret.json')

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    home_dir = os.path.dirname(os.path.realpath('__file__'))
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    time_now = pendulum.now("Asia/Taipei")
    if time_now.hour >= 22 or time_now.hour < 6:
        pprint("Sport center closed.")
        return

    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    # rangeName = 'Sheet1!A1:F'
    # result = service.spreadsheets().values().get(
    #     spreadsheetId=spreadsheetId, range=rangeName).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))
    # credentials = None
    # service = discovery.build('sheets', 'v4', credentials=credentials)
    # The ID of the spreadsheet to update.
    spreadsheet_id = '1dkQ9ezPsTugxBNwmE321dZrcnNR8AExBeqcd2t3q5v0'  # TODO: Update placeholder value.
    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'A3'  # TODO: Update placeholder value.
    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED' #'RAW'  # TODO: Update placeholder value.
    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.
    responseDateTimeRenderOption = 'FORMATTED_STRING'  # TODO: Update placeholder value.
    responseValueRenderOption = 'FORMATTED_VALUE'  # TODO: Update placeholder value.
    
    value_pack, d, da, t = [], [], [], []
    # d.append(time.strftime("%Y/%m/%d %H:%M"))
    d.append(time_now.format("%Y/%m/%d %H:%M"))
    # da.append(time.strftime("%A"))
    # t.append(time.strftime("%H:%M"))
    # value_pack.extend([d,da,t])
    value_pack.extend([d])

    # for k, v in sorted(sport_centers.items()):
    for k, v in sport_centers.items():
        r = requests.post(v)
        result = r.json()
        g0, g1, s0, s1 = [], [], [], []
        g0.append(result['gym'][0])
        g1.append(result['gym'][1])
        s0.append(result['swim'][0])
        s1.append(result['swim'][1])
        value_pack.extend([g0,g1,s0,s1])
        print("--------------------")
        print("{}".format(k))
        print("健身房：", result['gym'][0], "/", result['gym'][1])
        print("游泳池：", result['swim'][0], "/", result['swim'][1])
        print("")
        time.sleep(1)
    
    for k, v in sport_centers_e.items():
        center_info = []
        r = requests.get(v)
        html_parse = html.fromstring(r.text)
        sport_center_value_list = html_parse.xpath(
            '//div[contains(@class, "flow_number_wrap")]//h3/span/text()'
        )[:4] # ['24 人', '120人', '47 人', '300人', '29度C']
        target = re.compile(r'(\d+)')
        
        for val in sport_center_value_list:
            d = target.search(val)[0]
            value_pack.append([d])
            center_info.append(d)
        print("--------------------")
        print("{}".format(k))
        print("健身房：", center_info[0], "/", center_info[1])
        print("游泳池：", center_info[2], "/", center_info[3])
        print("")
        time.sleep(1)
    print("--------------------")
    print("Writing data to Google Spreadsheet:\n")
    for i, l in enumerate(value_pack):
        if i == 0:
            print("[", l)
        elif i % 4 == 1:
            print(l, value_pack[i+1], value_pack[i+2], value_pack[i+3], end=' ')
            if i < len(value_pack) - 4:
                print('')
                i += 4
            else:
                print(']', end='\n\n')
                print("--------------------")
                break

    value_range_body = {
        # TODO: Add desired entries to the request body.
        "majorDimension": "COLUMNS",
        "range": "A3",
        "values": value_pack
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, 
        body=value_range_body
    )
    response = request.execute()
    # TODO: Change code below to process the `response` dict:
    print("The result of updating Google Spreadsheet:\n")
    pprint(response)
    print("--------------------", end='\n\n')

if __name__ == '__main__':
    main()
