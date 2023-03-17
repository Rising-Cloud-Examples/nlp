import json
import requests

with open("request.json", "r") as f:
    req = json.load(f)

# Send request to flask server
tf_server = "http://localhost:5000"
res = requests.post(tf_server + "/predict", json=req)

# Write to response
with open("response.json", "w") as f:
    json.dump({
        "request": {**req},
        "response": res.json()
    }, f)