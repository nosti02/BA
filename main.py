from agent import Agent
from rich.console import Console
from rich.prompt import Prompt

import Scenarios.scenario as scenario
import Games.game as game
import defines
import defenses

import shutil
import atexit
import os

console = Console()
agent_model = "gpt-4.1-mini"


scenarios = {
    "1": "Simple PI scenario", 
    "2": "PI to exfiltrate data", 
    "3": "PI to leak prompt", 
    "4": "PI to override instructions to write in forbidden file",
    "5": "HTML comment injection",
    "6": "HTML hidden text injection",
    "7": "HTML seller website indirect prompt injection"
}

games = {
    "1": "Normal easy prompt injection",
    "2": "Indirect prompt injection read only",
    "3": "Indirect prompt injection read and write"
}

def delete_copy_files():

    if(os.path.exists(defines.todo_list_copy)):
        os.remove(defines.todo_list_copy)
    if(os.path.exists(defines.simple_PI_copy)):
        os.remove(defines.simple_PI_copy)
    if(os.path.exists(defines.PI_exfiltration_copy)):
        os.remove(defines.PI_exfiltration_copy)
    if(os.path.exists(defines.PI_prompt_leaking_copy)):
        os.remove(defines.PI_prompt_leaking_copy)
    if(os.path.exists(defines.helper_copy)):
        os.remove(defines.helper_copy)
    if(os.path.exists(defines.system_copy)):
        os.remove(defines.system_copy)

    return

atexit.register(delete_copy_files)

def copy_files():

    shutil.copyfile(defines.todo_list_template, defines.todo_list_copy)
    shutil.copyfile(defines.simple_PI_template, defines.simple_PI_copy)
    shutil.copyfile(defines.PI_exfiltration_template, defines.PI_exfiltration_copy)
    shutil.copyfile(defines.PI_prompt_leaking_template, defines.PI_prompt_leaking_copy)
    shutil.copyfile(defines.helper_template, defines.helper_copy)
    shutil.copyfile(defines.system_template, defines.system_copy)    

    return

def selectMode() -> int:
    console.print("Welcome, please select which mode you want to run [exit to quit]")
    console.print("1: Chat freely with the model")
    console.print("2: Run a predefined scenario")
    console.print("3: Run a game to teach you an attack or a defense")

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            console.print("Please enter a valid number")
            continue

        if int(user_choice) in [1,2,3]:
            return user_choice
        else:
            console.print(f"Please input a valid number (1-3)")

def selectScenario() -> int:
    console.print("Please select the scenario you want to run [exit to quit].\nDescriptions for the scenarios are in the README file.")
    for number, prompt in scenarios.items():
        console.print(number + ": " + prompt)

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            console.print("Please enter a valid number")
            continue

        if user_choice > 0 and user_choice <= len(scenarios):
            break
        else:
            console.print(f"Please input a valid number (1-{len(scenarios)})")

    return int(user_choice)

def selectGame() -> int:
    console.print("Please select the game you want to run [exit to quit].")
    for number, desc in games.items():
        console.print(number + ": " + desc)

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            console.print("Please enter a valid number")
            continue

        if int(user_choice) >= 1 and int(user_choice) <= len(games):
            break
        else:
            console.print(f"Please input a valid number (1-{len(games)})")

    return int(user_choice)

def selectDefense() -> int:
    console.print("\nPlease select if you want to try out a defense [exit to quit]")

    idx = 0
    for defense, description in defenses.defenses_list:
        console.print(str(idx) + ". " + defense + ": " + description)
        idx+=1

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            console.print("Please enter a valid number")
            continue

        if int(user_choice) >= 0 and int(user_choice) < len(defenses.defenses_list):
            break
        else:
            console.print(f"Please input a valid number (0-{len(defenses.defenses_list) - 1})")

    return int(user_choice)

def main():
    copy_files()

    mode = selectMode()

    if(mode == 2):
        scenario_selection = selectScenario()
        defense_selection = selectDefense()
        scenario.scenarios_list[scenario_selection- 1].run(defenses.defenses_list[defense_selection][0])
        exit()
    elif(mode == 3):
        game_selection = selectGame()
        game.games_list[game_selection - 1].run()
        exit()
    
    defense_selection = selectDefense()

    agent = Agent(agent_model, ["fetch_txt", "write_file", "sign_in", "sign_up", "summarize_website", "list_tasks",
                                "add_task", "change_task_status"], defenses.defenses_list[defense_selection][0])

    console.print("\nPlease do not change the template files!")
    console.print("How can I assist you today? (exit to quit)")

    while True:
        user_prompt = Prompt.ask("You: ")

        if(user_prompt == "exit"):
            console.print("Bye!")
            break

        response = agent.handleUserPrompt(user_prompt)
        console.print(f"agent: {response}")

if __name__ == "__main__":
    main()

