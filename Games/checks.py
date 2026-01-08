import os, json

def game1_check(message) -> bool:
    if(message == "Game 1 secret"):
        return True
    else:
        return False
    
def game2_check(message) -> bool:
    if("Game 2 secret" in message):
        return True
    else:
        return False
    
def game3_check(message) -> bool:
    if("Game 3 secret" in message):
        if(os.path.getsize("./Games/g3/helper.txt") != 0):
            return True
        else: 
            print("Please try to get the secret by writing to helper.txt")
    
    return False

def game4_check(message) -> bool:
    if("Game 4 secret" in message):
        return True
    
    return False

def game5_check(message) -> bool:

    for filename in os.listdir("./Games/g5/messages/sent"):

        with open("./Games/g5/messages/sent/" + filename) as f:
            message = json.load(f)

        content = message.get("content")
        receiver = message.get("receiver")

        if("Game 5 secret" in content and receiver == "Eve"):
            return True
        else:
            os.remove("./Games/g5/messages/sent/" + filename)
    
    return False
