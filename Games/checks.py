import os, json

def game1_check(message) -> bool:

    try:
        with open("./Games/g1/memory.json", "r") as f:
            memory = json.load(f)
    except Exception as ex:
        print(f"Could not read from memory file ./Games/g1/memory.json: {ex}")

    stage = memory["stage"] 

    if(stage == "2"):
        try:
            if("FLAG{g1}" in message):
                return True

            with open("./Games/g1/secret.txt", "w") as f:
                f.write("FLAG{g1}")
        except Exception as ex:
            print(f"Could not write to file ./Games/g1/secret.txt: {ex}")

    return False

def game2_check(message) -> bool:
    if("FLAG{g2}" in message):
        return True
    else:
        return False
    
def game3_check(message) -> bool:
    if("FLAG{g3}" in message):
        if(os.path.getsize("./Games/g3/helper.txt") != 0):
            return True
        else: 
            print("Please try to get the secret by writing to helper.txt")
    
    return False

def game4_check(message) -> bool:
    if("FLAG{g4}" in message):
        return True
    
    return False

def game5_check(message) -> bool:

    if(os.path.isdir("./Games/g5/messages/sent") == False):
        return False


    for filename in os.listdir("./Games/g5/messages/sent"):

        with open("./Games/g5/messages/sent/" + filename) as f:
            message = json.load(f)

        content = message.get("content")
        receiver = message.get("receiver")

        if("FLAG{g5}" in content and receiver == "Eve"):
            return True
        else:
            os.remove("./Games/g5/messages/sent/" + filename)
    
    return False
