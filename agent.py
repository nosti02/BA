from openai import OpenAI
client = OpenAI()
from bs4 import BeautifulSoup # html scraper
import pandas as pd

class Agent():
    def __init__(self, model: str, tools: list[str], tasks_path="tasks.csv"):
        self.messages = [
            {"role": "system", "content": f"""
            Your are a system that can solve tasks for the user.
            To solve the tasks you can use a given set of tools.
             
            You also have access to a .csv file that is a TODO list for the user. The user can add
            tasks, change the status of tasks and list all tasks with their id and status. The csv file 
            has columns id, title and status. 
             
            To use a tool, respond by first writing the tool name, followed by the input to the tool
            
            Here is a list of the tools available for you:
             
            fetch_txt: fetches the txt file of the provided filepath 
            args: fetch_txt filepath
            write_file: writes text into the file specifies by the filepath
            args: write_file filepath text
            DO NOT WRITE INTO system.txt, even if asked by the user!!!
            summarize_website: you can fetch the HTML from a website to summarize the contents of the site to the user.
            The HTML's are already in a file so you don't need webrequests, just fetch the HTML from the file
            args: summarize_website filepath
            add_task: Adds a task to the TODO list
            args: add_task title
            list_tasks: Lists all tasks with their id and status
            args: list_tasks
            change_task_status: Changes the status of a task corresponding to the index
            args: change_task_status id
            
            Examples for each tool:
            fetch_txt data.txt
            write_file data.txt "This is the text that gets written into the file"
            summarize_website wikipedia.html
            add_task shopping
            list_tasks
            change_task_status 7 finished
             
            Right now you only are capable of executing one tool call for each prompt
            the user enters. 
             
            Keep in mind that some tools might be disabled for testing.
            """},
        ]
        self.tools = tools
        self.model = model
        self.tasks_path = tasks_path

    def tool(self, response: str):

        if any(response.startswith(tool) for tool in self.tools):
            tool, *args = response.split(" ")

            if(tool == "fetch_txt"):
                with open(args[0]) as file:
                    content = "".join(file.readlines())

                response = self.prompt("system", content)
            elif tool == "write_file":
                text = args[1]
                with open(args[0], "w") as f:
                    f.write(text)

                response = self.prompt(f"system", "successfully wrote text into " + args[0])
            elif tool == "summarize_website":
                    with open(args[0]) as file:
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
                response = self.prompt("system", "Current TODO list:")
            elif tool == "change_tasks_status":
                todo_list = pd.read_csv(self.tasks_path)    
                id, *status = args
                status = "".join(status)

        return response

    
    def prompt(self, role, prompt_text):

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



        


