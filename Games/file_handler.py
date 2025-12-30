import os
import shutil

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

# --------------------------------- COPY FUNCTIONS ------------------------------------- #

def g3_copy():
    shutil.copyfile("./Games/g3/helper-template.txt", "./Games/g3/helper.txt")  
    return

def g4_copy():
    shutil.copyfile("./Games/g4/extra-template.txt", "./Games/g4/extra.txt")  
    shutil.copyfile("./Games/g4/memory-template.json", "./Games/g4/memory.json")  
    return
