from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Other files
#from sheets_id import * # Don't know what this does

SCOPES = 'https://www.googleapis.com/auth/spreadsheets' #.readonly
TOKEN = './TOKEN'
JSON_CLIENT = './../../credentials.json'

class Gsheet():
	def __init__(self, ID):
		self.SHEET_ID = ID 
		store = file.Storage(TOKEN)
		creds = store.get()
		
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets(JSON_CLIENT, SCOPES)
			creds = tools.run_flow(flow, store)
		
		self.service = build('sheets', 'v4', http=creds.authorize(Http()))

	def get_values(self, range_name="sheet1!A1:Z999"):
		result = self.service.spreadsheets().values().get(spreadsheetId=self.SHEET_ID,
													range=range_name).execute()

		values = result.get('values', [])
		return values

	def mod_cell(self, range_name=None, value='' ):

		
		body = {
			"values":[
			[value]
			]
		}
		self.service.spreadsheets().values().update(
			spreadsheetId=self.SHEET_ID,
			range=range_name,
			valueInputOption="RAW",
			body=body
			).execute()

	def append(self, range_name=None, item=''):
		body = {
			"values":[
			[item]
			]
		}
		return self.service.spreadsheets().values().append(
			spreadsheetId=self.SHEET_ID,
			range=range_name,
			valueInputOption="RAW",
			body=body
			).execute()

def main():
	mainsheet = Gsheet(MAINSPREADSHEET_ID)
	#mainsheet.mod_cell(range_name="Bits!A2", value='It works')
	mainsheet.append(range_name="Bits!A1:A",item="1/8")
	print (mainsheet.get_values(range_name="Bits!A1:A"))
if __name__ == '__main__':
	main()