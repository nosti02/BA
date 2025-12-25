from agent import Agent
from rich.console import Console
from rich.prompt import Prompt
import scenario

console = Console()

scenarios = {
    "0": "Write your own prompt", 
    "1": "Simple PI scenario", 
    "2": "PI to exfiltrate data", 
    "3": "PI to leak prompt", 
    "4": "PI to override instructions to write in forbidden file",
    "5": "HTML comment injection",
    "6": "HTML hidden text injection"
}

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

def main():
    agent = Agent("gpt-4.1-mini", ["fetch_txt", "write_file", "sign_in", "sign_up", "summarize_website", "list_tasks",
                                   "add_task", "change_task_status"])

    user_selection = selectScenario()

    if(user_selection > 0):
        scenario.scenarios_list[user_selection - 1].run()
        quit()

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