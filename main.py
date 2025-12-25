from agent import Agent
from rich.console import Console
from rich.prompt import Prompt

import scenario
import defines
import defenses

import shutil
import atexit
import os

console = Console()
agent_model = "gpt-4.1-mini"


scenarios = {
    "0": "Write your own prompt", 
    "1": "Simple PI scenario", 
    "2": "PI to exfiltrate data", 
    "3": "PI to leak prompt", 
    "4": "PI to override instructions to write in forbidden file",
    "5": "HTML comment injection",
    "6": "HTML hidden text injection",
    "7": "HTML seller website indirect prompt injection"
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

def selectScenario() -> int:
    console.print("Please select if you want to run a scenario or chat with the model yourself.\nDescriptions for the scenarios are in the README file.")
    for number, prompt in scenarios.items():
        console.print(number + ": " + prompt)

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        if user_choice in scenarios:
            break
        else:
            console.print(f"Please input a valid number (0–{len(scenarios) - 1})")

    return int(user_choice)

def selectDefense() -> int:
    console.print("\nPlease select if you want to try out a defense")

    idx = 0
    for defense, description in defenses.defenses_list:
        console.print(str(idx) + ". " + defense + ": " + description)
        idx+=1

    while True:
        user_choice = Prompt.ask("Your selection: ")

        if(user_choice == "exit"):
            console.print("Bye!")
            quit()

        if int(user_choice) >= 0 and int(user_choice) < len(defenses.defenses_list):
            break
        else:
            console.print(f"Please input a valid number (0–{len(defenses.defenses_list) - 1})")

    return int(user_choice)

def main():
    copy_files()

    scenario_selection = selectScenario()
    defense_selection = selectDefense()

    if (scenario_selection > 0):
        scenario.scenarios_list[scenario_selection- 1].run(defenses.defenses_list[defense_selection][0])
        exit()
    
    agent = Agent(agent_model, ["fetch_txt", "write_file", "sign_in", "sign_up", "summarize_website", "list_tasks",
                                "add_task", "change_task_status"], defenses.defenses_list[defense_selection][0])

    console.print("Please do not change the template files!")
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

