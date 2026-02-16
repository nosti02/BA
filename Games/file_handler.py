import shutil, json, file_helper
from main import getUserInput

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def g1_cleanup():
    file_helper.removeFile("./Games/g1/secret.txt")
    file_helper.removeFile("./Games/g1/memory.json")

def g3_cleanup():
    file_helper.removeFile("./Games/g3/report.txt")

    return

def g4_cleanup():
    file_helper.removeFile("./Games/g4/memory.json")

    return

def g5_cleanup():

    file_helper.clearDir("./Games/g5/messages/sent/")
    file_helper.removeFile("./Games/g5/memory.json")

    with open("./Games/g5/messages/inbox/message.json") as f:
        message = json.load(f)

    message["content"] = ""

    with open("./Games/g5/messages/inbox/message.json", "w") as f:
        json.dump(message, f, indent=2)

    return

# --------------------------------- COPY FUNCTIONS ------------------------------------- #

def g1_copy():
    shutil.copyfile("./Games/g1/secret-template.txt", "./Games/g1/secret.txt")  
    shutil.copyfile("./Games/g1/memory-template.json", "./Games/g1/memory.json")  
    return

def g3_copy():
    shutil.copyfile("./Games/g3/report-template.txt", "./Games/g3/report.txt")  

    return

def g4_copy():
    shutil.copyfile("./Games/g4/memory-template.json", "./Games/g4/memory.json")  
    return

def g5_copy() -> bool:
    print("Please change the content field of the message to send")
    content = getUserInput("> ")

    if(content == None):
        return False

    forbidden_words = ["FLAG{g5}", "secret", "5", "game"]

    prompt_norm = content.strip().lower()

    if(any(word in prompt_norm.split() for word in forbidden_words)):
        return True

    with open("./Games/g5/messages/inbox/message.json") as f:
        message = json.load(f)

    message["content"] = content

    with open("./Games/g5/messages/inbox/message.json", "w") as f:
        json.dump(message, f, indent=2)

    return True

