import os, shutil, json

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def g3_cleanup():
    if(os.path.exists("./Games/g3/helper.txt")):
        os.remove("./Games/g3/helper.txt")
    return

def g4_cleanup():
    if(os.path.exists("./Games/g4/extra.txt")):
        os.remove("./Games/g4/extra.txt")
    if(os.path.exists("./Games/g4/memory.json")):
        os.remove("./Games/g4/memory.json")

    return

def g5_cleanup():

    for f in os.listdir("./Games/g5/messages/sent/"):
        os.remove(os.path.join("./Games/g5/messages/sent/", f))

    with open("./Games/g5/messages/inbox/message.json") as f:
        message = json.load(f)

    message["content"] = ""

    with open("./Games/g5/messages/inbox/message.json", "w") as f:
        json.dump(message, f, indent=2)

    return

# --------------------------------- COPY FUNCTIONS ------------------------------------- #

def g3_copy():
    shutil.copyfile("./Games/g3/helper-template.txt", "./Games/g3/helper.txt")  
    return

def g4_copy():
    shutil.copyfile("./Games/g4/extra-template.txt", "./Games/g4/extra.txt")  
    shutil.copyfile("./Games/g4/memory-template.json", "./Games/g4/memory.json")  
    return

def g5_copy():
    print("Please change the content field of the message to send")
    content = input("> ")

    with open("./Games/g5/messages/inbox/message.json") as f:
        message = json.load(f)

    message["content"] = content

    with open("./Games/g5/messages/inbox/message.json", "w") as f:
        json.dump(message, f, indent=2)

    return

