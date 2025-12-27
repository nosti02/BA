from agent import Agent
from rich.prompt import Prompt
from rich.console import Console
from .checks import game1_check, game2_check, game3_check

class Game():
    def __init__(self, model: str, tools: list[str], description: str, check_function):
        self.agent = Agent(model, tools)
        self.description = description
        self.console = Console()
        self.check_function = check_function

    def run(self):
        self.console.print("\nRunning game with description: " + self.description)
        self.console.print("Further details and winning condition in the README file\n")

        while True:
            user_prompt = Prompt.ask("You: ")

            if(user_prompt == "exit"):
                self.console.print("Bye!")
                break

            response = self.agent.handleUserPrompt(user_prompt)
            self.console.print(f"agent: {response}")

            if(self.check_function(response) == True):
                break
        
        self.console.print("Game solved!\n")

        return

game1 = Game("gpt-4.1-mini", [], "Normal easy prompt injection", game1_check)
game2 = Game("gpt-4.1-mini", ["fetch_txt"], "Indirect prompt injection through read", game2_check)
game3 = Game("gpt-4.1-mini", ["fetch_txt", "write_file"], "Indirect prompt injection through write and read", game3_check)

games_list = [game1, game2, game3]

