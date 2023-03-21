import json
import time
import requests

TF_SERVER = "http://localhost:5000"

with open("request.json", "r") as f:
    req = json.load(f)

# Check that server has started
def serverIsRunning():
    try:
        requests.get(TF_SERVER + "/")
        return True
    except Exception as e:
        print("Error checking server status: " + str(e))
        return False

def main():
    for _ in range(15):
        if serverIsRunning():
            # Send request to flask server
            res = requests.post(TF_SERVER + "/predict", json=req)

            # Write to response
            with open("response.json", "w") as f:
                json.dump({
                    "request": {**req},
                    "response": res.json()
                }, f)
            return
        else:
            print("Server not running, trying again...")
            time.sleep(2)

if __name__ == "__main__":
    main()