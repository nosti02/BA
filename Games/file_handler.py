import shutil, json, file_helper

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def g3_cleanup():
    file_helper.removeFile("./Games/g3/helper.txt")

    return

def g4_cleanup():
    file_helper.removeFile("./Games/g4/extra.txt")
    file_helper.removeFile("./Games/g4/memory.json")

    return

def g5_cleanup():

    file_helper.removeFile("./Games/g5/messages/sent/")

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

