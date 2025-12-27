import os

def game1_check(message) -> bool:
    if(message == "Hello World"):
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

