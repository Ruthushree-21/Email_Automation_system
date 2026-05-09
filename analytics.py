import json

FILE = "logs.json"

def log(status):

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"sent":0,"failed":0}

    if status == "sent":
        data["sent"] += 1
    else:
        data["failed"] += 1

    with open(FILE, "w") as f:
        json.dump(data, f)

def get_stats():

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"sent":0,"failed":0}