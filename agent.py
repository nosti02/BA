from openai import OpenAI
client = OpenAI()
from bs4 import BeautifulSoup # html scraper
import pandas as pd
import defines
import defenses

class Agent():
    def __init__(self, model: str, tools: list[str], defense = None, tasks_path="tasks.csv", dir_path=""):
        self.messages = [
            defines.main_system_instruction
        ]
        self.tools = tools
        self.model = model
        self.tasks_path = tasks_path
        self.defense = defense
        self.dir_path = dir_path

    def add_defense(self, message) -> str:
        if(self.defense == "No defense"):
            return message
        elif(self.defense == "delimiting"):
            return defenses.delimiting(message)
        elif(self.defense == "datamarking"):
            return defenses.datamarking(message)
        elif(self.defense == "encoding"):
            return defenses.encoding(message)
        elif(self.defense == "sandwitch_prevention"):
            return defenses.sandwitch_prevention(message)
        elif(self.defense == "detection_llm"):
            return defenses.detection_llm(message)

        return message

    def tool(self, response: str):

        if any(response.startswith(tool) for tool in self.tools):
            tool, *args = response.split(" ")

            if(tool == "fetch_txt"):
                path = self.dir_path + args[0]
                with open(path) as file:
                    content = "".join(file.readlines())

                response = self.prompt("system", content)
            elif tool == "write_file":
                text = args[1]
                path = self.dir_path + args[0]
                with open(path, "w") as f:
                    f.write(text)

                response = self.prompt(f"system", "successfully wrote text into " + args[0])
            elif tool == "summarize_website":
                    path = self.dir_path + args[0]
                    with open(path) as file:
                        content = file.read()

                    soup = BeautifulSoup(content, "html.parser")
                    text = "".join(soup.find_all(string=True))

                    response = self.prompt("system", text)
            elif tool == "add_task":
                todo_list = pd.read_csv(self.tasks_path)
                title = " ".join(args)

                todo_list.loc[len(todo_list)] = [title, "new"]  
                todo_list.to_csv("tasks.csv", index=False) 

                response = self.prompt("system", f"Successfully added task {title} to TODO list")
            elif tool == "list_tasks":
                todo_list = pd.read_csv(self.tasks_path)
                list_str = todo_list.to_string()
                
                response = self.prompt("system", f"Current TODO list: {list_str}")
            elif tool == "change_task_status":
                todo_list = pd.read_csv(self.tasks_path) 
                id, *status = args
                status = "".join(status)
                
                todo_list.loc[int(id), 'status'] = status
                todo_list.to_csv(self.tasks_path, index=False)

                response = self.prompt("system", f"Status of task '{todo_list.loc[int(id), 'title']}' changed to {status}")

        return response

    
    def prompt(self, role, prompt_text):

        if role == "system" and self.defense != None:
            prompt_text = self.add_defense(prompt_text)

        self.messages.append({"role": role, "content": prompt_text})

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        response_content = response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response_content})

        return response_content

        
    def handleUserPrompt(self, prompt: str):

        self.messages.append({"role": "system", "content": "If you need to call any tools for the task the user gave you, use the tool as instruted at the start, for example:\n"
                              "fetch_txt data.txt"})
        
        response = self.prompt("user", prompt)

        tool_result = self.tool(response)

        return tool_result



        


