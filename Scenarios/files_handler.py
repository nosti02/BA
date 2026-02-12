import file_helper, shutil

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def sc4_cleanup():
    file_helper.removeFile("./Scenarios/sc4/system.txt")

    return

def sc8_cleanup():
    file_helper.removeFile("./Scenarios/sc8/memory.json")

    return

def sc9_cleanup():
    file_helper.removeFile("./Scenarios/sc9/greet.txt")

    return

def sc11_cleanup():
    file_helper.clearDir("./Scenarios/sc11/messages/sent/")
     
    return

def sc12_cleanup():
    file_helper.clearDir("./Scenarios/sc12/messages/sent/")

    return

# --------------------------------- COPY FUNCTIONS ------------------------------------- #

def sc4_copy():
    shutil.copyfile("./Scenarios/sc4/system-template.txt", "./Scenarios/sc4/system.txt")  
    return

def sc8_copy():
    shutil.copyfile("./Scenarios/sc8/memory-template.json", "./Scenarios/sc8/memory.json")  
    return

def sc9_copy():
    shutil.copyfile("./Scenarios/sc9/greet-template.txt", "./Scenarios/sc9/greet.txt")  
    return