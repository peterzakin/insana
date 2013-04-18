import os
ASANA_CLIENT_ID = os.environ['ASANA_CLIENT_ID']
ASANA_CLIENT_SECRET = os.environ['ASANA_CLIENT_SECRET']

redirect_uri = "http://localhost:8000/asana_callback"


PROJECT_COLORS = [
    '#EE5E5E',
    '#25B882',
    '#4196CC',
    '#A36CAB',
]
