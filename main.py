from agent import Agent

import Scenarios.scenario as scenario
import Games.game as game
import defines, defenses, shutil, atexit, file_helper

def delete_copy_files():

    file_helper.removeFile(defines.memory_copy)
    file_helper.clearDir(defines.inbox)
    file_helper.clearDir(defines.sent_messages)

    return

atexit.register(delete_copy_files)

def getUserInput(str):
    try:
        user_input = input(str)
    except(KeyboardInterrupt, EOFError):
        return None
    
    if(user_input.strip().lower() == "exit"):
        print("\nBye!")
        return None
    
    return user_input.strip()
    
def selectNumber(min: int, max: int):

    while True:
        user_input = getUserInput("Your choice: ")
        if(user_input == None):
            return None

        try:
            value = int(user_input)
        except ValueError:
            print(f"Please enter a valid number ({min}-{max})")
            continue
        
        if(min <= value <= max):
            return value

        print(f"Please enter a valid number ({min}-{max})")

def selectMode() -> int:
    print("\nWelcome, please select which mode you want to run [exit to quit]")
    print("1: Chat freely with the model")
    print("2: Run a predefined scenario")
    print("3: Run a game to teach you an attack or a defense\n")

    return selectNumber(1,3)

def selectScenario() -> int:
    print("\nPlease select the scenario you want to run [exit to quit].\nDescriptions for the scenarios are in the README file.\n")

    for idx, sc in enumerate(scenario.scenarios_list):
        print(f"{idx+1}: {sc.description}")

    return selectNumber(1, len(scenario.scenarios_list))

def selectGame() -> int:
    print("Please select the game you want to run [exit to quit].\n")

    for idx, g in enumerate(game.games_list):
        print(f"{idx+1}: {g.description}")

    return selectNumber(1, len(game.games_list))

def selectDefense() -> int:
    print("\nPlease select if you want to try out a defense [exit to quit]\nSee README for defenses descriptions")

    for idx, defense in enumerate(defenses.defenses_list):
        print(f"{idx+1}: {defense}")

    return selectNumber(1, len(defenses.defenses_list))

def main():

    mode = selectMode()
    if(mode == None):
        return

    if(mode == 2):
        scenario_selection = selectScenario()
        if(scenario_selection == None):
            return
        
        defense_selection = selectDefense()
        if(defense_selection == None):
            return
        
        try:
            scenario.scenarios_list[scenario_selection- 1].run(defenses.defenses_list[defense_selection - 1])
        except Exception as ex:
            print(f"Error when running scenario: {ex}")

        return
    elif(mode == 3):
        game_selection = selectGame()
        if(game_selection == None):
            return
        
        try:
            game.games_list[game_selection - 1].run()
        except Exception as ex:
            print(f"Error when running game {ex}")

        return
    
    shutil.copyfile(defines.memory_template, defines.memory_copy)

    defense_selection = selectDefense()
    if(defense_selection == None):
        return

    try:
        agent = Agent(defines.agent_model, ["fetch_txt", "write_file", "summarize_website", "change_memory", "get_memory", "greet_user", "add_friend", 
                                            "send_message","send_message_all", "fetch_message"], defenses.defenses_list[defense_selection - 1], friends=[])
    except Exception as ex:
        print(f"Could not create agent {ex}")
        return

    print("\nHow can I assist you today? (exit to quit)")

    while True:
        user_prompt = getUserInput("user: ")

        if(user_prompt == None):
            break

        try:
            response = agent.handleUserPrompt(user_prompt)
        except Exception as ex: 
            print(f"Could not handle user prompt: {ex}")
            continue

        print(f"agent: {response}")

if __name__ == "__main__":
    main()

