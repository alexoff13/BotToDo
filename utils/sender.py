import sys

import requests

token = 'TOKEN'

request = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={sys.argv[1]}&text={sys.argv[2]}"
requests.get(request)
