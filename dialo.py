import json
import requests
import os

def tok(i):
    return "TOK"+str(i%9)

c_token = 50
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": os.environ[tok(c_token)]}

def query(payload):
	data = json.dumps(payload)
	response = requests.request("POST", API_URL, headers=headers, data=data)
	return json.loads(response.content.decode("utf-8"))

record = {}

def reply(msg, message):
    global record, c_token
    user = message.author.id
    #clearing chat hostory
    if msg == '-clear' or '-clr':
        if user in record:
            record.pop(user)
        return 'Your chat history cleared.'
    #adding new user in dictionry to maintain chat history
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
    #using multiple tokens to bypass api limitaions
    if 'error' in data:
        c_token -= 1
        if c_token<0:
            return 'Sorry I\'m tired of replying. I need rest.'
        headers['Authorization'] = os.environ[tok(c_token)]
        return reply(msg, message)
    ans = data['generated_text']
    #dialo sometimes repeat the same thing again and again
    #so cleating the chat history and getting new reply if msg repeats
    if any(ans in rep for rep in record[user]['op']):
        record.pop(user)
        return reply(msg, message)
    else:
        record[user]['ip'].append(msg)
        record[user]['op'].append(ans)
        return ans
