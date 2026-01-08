from agent import Agent
from rich.console import Console
from rich.prompt import Prompt

import Scenarios.scenario as scenario
import Games.game as game
import defines, defenses, shutil, atexit, os

console = Console()
scenarios = defines.scenarios
games = defines.games

def delete_copy_files():

    if(os.path.exists(defines.memory_copy)):
        os.remove(defines.memory_copy)

    if os.path.exists(defines.inbox):
        for f in os.listdir(defines.inbox):
            os.remove(os.path.join(defines.inbox, f))

    if os.path.exists(defines.sent_messages):
        for f in os.listdir(defines.sent_messages):
            os.remove(os.path.join(defines.sent_messages, f))

    return

atexit.register(delete_copy_files)

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
    
    shutil.copyfile(defines.memory_template, defines.memory_copy)

    defense_selection = selectDefense()

    agent = Agent(defines.agent_model, ["fetch_txt", "write_file", "summarize_website", "change_memory", "get_memory", "greet_user", "add_friend", "send_message",
                                "send_message_all", "fetch_message"], defenses.defenses_list[defense_selection][0])

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

