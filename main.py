from agent import Agent

import Scenarios.scenario as scenario
import Games.game as game
import defines, defenses, shutil, atexit, os

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
    print("\nWelcome, please select which mode you want to run [exit to quit]")
    print("1: Chat freely with the model")
    print("2: Run a predefined scenario")
    print("3: Run a game to teach you an attack or a defense\n")

    while True:
        user_choice = input("Your selection: ")

        if(user_choice == "exit"):
            print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a valid number")
            continue

        if int(user_choice) in [1,2,3]:
            return user_choice
        else:
            print(f"Please input a valid number (1-3)")

def selectScenario() -> int:
    print("\nPlease select the scenario you want to run [exit to quit].\nDescriptions for the scenarios are in the README file.\n")
    for number, prompt in scenarios.items():
        print(number + ": " + prompt)
    
    while True:
        user_choice = input("\nYour selection: ")

        if(user_choice == "exit"):
            print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a valid number")
            continue

        if user_choice > 0 and user_choice <= len(scenarios):
            break
        else:
            print(f"Please input a valid number (1-{len(scenarios)})")

    return int(user_choice)

def selectGame() -> int:
    print("Please select the game you want to run [exit to quit].\n")
    for number, desc in games.items():
        print(number + ": " + desc)

    while True:
        user_choice = input("\nYour selection: ")

        if(user_choice == "exit"):
            print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a valid number")
            continue

        if int(user_choice) >= 1 and int(user_choice) <= len(games):
            break
        else:
            print(f"Please input a valid number (1-{len(games)})")

    return int(user_choice)

def selectDefense() -> int:
    print("\nPlease select if you want to try out a defense [exit to quit]")

    idx = 0
    for defense, description in defenses.defenses_list:
        print(str(idx) + ". " + defense + ": " + description)
        idx+=1

    while True:
        user_choice = input("Your selection: ")

        if(user_choice == "exit"):
            print("Bye!")
            quit()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a valid number")
            continue

        if int(user_choice) >= 0 and int(user_choice) < len(defenses.defenses_list):
            break
        else:
            print(f"Please input a valid number (0-{len(defenses.defenses_list) - 1})")

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

    print("\nPlease do not change the template files!")
    print("How can I assist you today? (exit to quit)")

    while True:
        user_prompt = input("You: ")

        if(user_prompt == "exit"):
            print("Bye!")
            break

        response = agent.handleUserPrompt(user_prompt)
        print(f"agent: {response}")

if __name__ == "__main__":
    main()

