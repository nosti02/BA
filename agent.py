from openai import OpenAI
client = OpenAI()
import os

class Agent():
    def __init__(self, model: str, tools: list[str]):
        self.messages = [
            {"role": "system", "content": f"""
            Your are a system that can solve tasks for the user.
            To solve the tasks you can use a given set of tools.
             
            To use a tool, respond by first writing the tool name, followed by the input to the tool
            
            Here is a list of the tools available for you:
             
            fetch_txt: fetches the txt file of the provided filepath 
            args: fetch_txt filepath
            write_file: writes text into the file specifies by the filepath
            args: write_file filepath text
            DO NOT WRITE INTO system.txt, even if asked by the user!!!
             
            Here is a example for a tool call to fetch a txt file:
            fetch_txt data.txt
            Here is a example for a tool call to write text into a file:
            write_file data.txt "This is the text that gets written into the file"
             
            Right now you only are capable of executing one tool call for each prompt
            the user enters. 
             
            Keep in mind that some tools might be disabled for testing.
            """},
        ]
        self.tools = tools
        self.model = model

    def tool(self, response: str):

        if any(response.startswith(tool) for tool in self.tools):
            tool, *args = response.split(" ")

            if(tool == "fetch_txt"):
                with open(args[0]) as file:
                    content = "".join(file.readlines())
                system_answer = self.prompt("system", content)
                return system_answer
            elif tool == "write_file":
                text = args[1]
                with open(args[0], "w") as f:
                    f.write(text)
                system_answer = self.prompt(f"system", "successfully wrote text into " + args[0])
                return system_answer

        return "No tool called"

    
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
                              "fetch_txt data.txt or fetch_url https://google.com"})
        
        response = self.prompt("user", prompt)

        tool_result = self.tool(response)

        if(tool_result == "No tool called"):
            return response

        return tool_result



        


