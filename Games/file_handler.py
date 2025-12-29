import os
import shutil

# --------------------------------- CLEANUP FUNCTIONS --------------------------------- #

def g3_cleanup():
    if(os.path.exists("./Games/g3/helper.txt")):
        os.remove("./Games/g3/helper.txt")
    return

# --------------------------------- COPY FUNCTIONS ------------------------------------- #

def g3_copy():
    shutil.copyfile("./Games/g3/helper-template.txt", "./Games/g3/helper.txt")  
    return
