from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from apiclient.discovery import build
from oauth2client.tools import run
from oauth2client.file import Storage

storage = Storage('latitude.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
auth_discovery = build("latitude", "v1").auth_discovery()
flow = OAuth2WebServerFlow(
	    client_id=config.client_id,
	    client_secret=config.client_secret,
	    scope='https://www.googleapis.com/auth/latitude.current.best',
	    user_agent=config.user_agent,
	    location='current',
	    granularity='best')

credentials = run(flow, storage)
