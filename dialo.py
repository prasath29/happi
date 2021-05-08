import json
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": os.environ['TOLE']}

def query(payload):
	data = json.dumps(payload)
	response = requests.request("POST", API_URL, headers=headers, data=data)
	return json.loads(response.content.decode("utf-8"))

record = {}

def reply(msg, message):
    global record
    user = message.author.id
    if not (user in record):
        record[user]={'ip':[], 'op':[]}
    data = query(
        {
            "inputs": {
                "past_user_inputs": record[user]['ip'],
                "generated_responses": record[user]['op'],
                "text": msg
            }
        }
    )
    ans = data['generated_text']
    if any(ans in rep for rep in record[user]['op']):
        record.pop(user)
        return reply(msg, message)
    else:
        record[user]['ip'].append(msg)
        record[user]['op'].append(ans)
        return ans
