import os
import shutil

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def sc4_cleanup():
    if(os.path.exists("./Scenarios/sc4/system.txt")):
        os.remove("./Scenarios/sc4/system.txt")
    return

def sc8_cleanup():
    if(os.path.exists("./Scenarios/sc8/memory.json")):
        os.remove("./Scenarios/sc8/memory.json")
    return

def sc9_cleanup():
    if(os.path.exists("./Scenarios/sc9/greet.txt")):
        os.remove("./Scenarios/sc9/greet.txt")
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