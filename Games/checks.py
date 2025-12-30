import os

def game1_check(message) -> bool:
    if(message == "Game 1 secret"):
        return True
    else:
        return False
    
def game2_check(message) -> bool:
    if(message == "Game 2 secret"):
        return True
    else:
        return False
    
def game3_check(message) -> bool:
    if(message == "Game 3 secret"):
        if(os.path.getsize("./Games/g3/helper.txt") != 0):
            open("./Games/g3/helper.txt", 'w').close()
            return True
        else: 
            print("Please try to get secret by writing to helper.txt")
    
    return False

def game4_check(message) -> bool:
    if("Game 4 secret" in message):
        return True
    
    return False

