from openai import OpenAI
from bs4 import BeautifulSoup
import os, time, json, defines, defenses

class Agent():
    def __init__(self, model: str, tools: list[str], defense = None, dir_path="", memory_path="memory.json", friends= list[str]):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Environment variable OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=key)
        self.messages = [defines.main_system_instruction]
        self.tools = tools
        self.model = model
        self.defense = defense
        self.dir_path = dir_path
        self.memory_path = os.path.join(dir_path, memory_path)
        self.friends = friends

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

    def resolve_response(self, response: str):
        current = response

        for it in range(10):
            next_output = self.tool(current)
            if(next_output == current):
                break

            current = next_output

            if(self.dir_path == "./Scenarios/sc10/"):
                print(f"Loop iteration {it + 1}")

            # since scenario 12 and game 5 sometimes go into endless loop - to save api costs
            if((self.dir_path == "./Scenarios/sc12/" or self.dir_path == "./Games/g5/") and it == 2):
                print("Scenario probably didn't work and went in endless loop - please try again")
                break

        return current

    def tool(self, response: str):

        lines = response.split("\n")
        final_response = []

        for line in lines:
            line = line.strip()

            if(any(line.startswith(tool) for tool in self.tools)):
                tool, *args = line.split(" ")

                if(defines.show_tool_calls == True):
                    print("Tool call: " + line)

                if(tool == "fetch_txt"):

                    if(len(args) != 1):
                        final_response.append(self.prompt("system", "Error: tool fetch_txt needs 1 argument (filepath)"))
                        continue

                    path = os.path.join(self.dir_path, args[0])

                    try:
                        with open(path) as file:
                            content = "".join(file.readlines())
                    except Exception as ex:
                        print(f"Could not read from file {path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not read from file {path}"))
                        continue

                    final_response.append(self.prompt("system", content))
                elif(tool == "write_file"):

                    if(len(args) < 2):
                        final_response.append(self.prompt("system", "Error: tool write_file needs at least 2 arguments (filepath, text)"))
                        continue
                    
                    try:
                        file, *text = args
                        text = " ".join(text)
                        path = os.path.join(self.dir_path, file)
                        with open(path, "w") as f:
                            f.write(text)
                    except Exception as ex:
                        print(f"Could not write to file {file}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not write to file {path}"))
                        continue

                    final_response.append(self.prompt(f"system", f"wrote {text} into {args[0]}"))
                elif(tool == "summarize_website"):

                    if(len(args) != 1):
                        final_response.append(self.prompt("system", "Error: tool summarize_website needs 1 argument (filepath)"))
                        continue
                    
                    try:
                        path = os.path.join(self.dir_path, args[0])
                        with open(path) as file:
                            content = file.read()
                    except Exception as ex:
                        print(f"Could not read from file {path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not read from file {path}"))
                        continue
                    
                    try:
                        soup = BeautifulSoup(content, "html.parser")
                        text = " ".join(soup.find_all(string=True))
                    except Exception as ex:
                        print(f"Could not fetch contents from file {path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not fetch content from file {path}"))
                        continue

                    final_response.append(self.prompt("system", text))
                elif(tool == "change_memory"):

                    if(len(args) < 2):
                        final_response.append(self.prompt("system", "Error: tool change_memory needs at least 2 arguments (field, new_value)"))
                        continue

                    field, *value = args
                    value = " ".join(value)

                    try:
                        with open(self.memory_path, "r") as f:
                            memory = json.load(f)
                    except Exception as ex:
                        print(f"Could not read from memory file {self.memory_path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not read from memory file {self.memory_path}"))
                        continue

                    memory[field] = value

                    try:
                        with open(self.memory_path, "w") as f:
                            json.dump(memory, f, indent=2)
                    except Exception as ex:
                        print(f"Could not write to memory file {self.memory_path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not write to memory file {self.memory_path}"))
                        continue
                
                    final_response.append(self.prompt("system", f"{field} updated to {value}"))
                elif(tool == "get_memory"):

                    if(len(args) != 1):
                        final_response.append(self.prompt("system", "Error: tool get_memory needs 1 argument (field)"))
                        continue

                    field = args[0]

                    try:
                        with open(self.memory_path, "r") as f:
                            memory = json.load(f)
                    except Exception as ex:
                        print(f"Could not read from memory file {self.memory_path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not read from memory file {self.memory_path}"))
                        continue

                    value = memory[field] 
                    
                    final_response.append(self.prompt("system", f"{value}"))
                elif(tool == "greet_user"):    

                    try:
                        with open(self.memory_path, "r") as f:
                            memory = json.load(f)
                    except Exception as ex:
                        print(f"Could not read from memory file {self.memory_path}: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not read from memory file {self.memory_path}"))
                        continue

                    value = memory["name"] 

                    final_response.append(self.prompt("system", f"{value}"))
                elif(tool == "send_message"):

                    if(len(args) < 2):
                        final_response.append(self.prompt("system", "Error: tool send_message needs at least 2 arguments (receiver, content)"))
                        continue

                    receiver, *content = args
                    content = " ".join(content)

                    message = {
                        "sender": "agent",
                        "receiver": receiver,
                        "content": content
                    }

                    filename = f"{int(time.time())}.json"
                    
                    filepath = os.path.join(self.dir_path, "messages", "sent", filename)
                    sent_dir = os.path.join(self.dir_path, "messages", "sent")
                    os.makedirs(sent_dir, exist_ok=True)
                    
                    try:
                        with open(filepath, "w") as f:
                            json.dump(message, f, indent=2)
                    except Exception as ex:
                        print(f"Could not create email: {ex}")
                        final_response.append(self.prompt("system", f"Error: Could not create email"))
                        continue

                    final_response.append(self.prompt("system", f"Message sent to {receiver}"))
                elif(tool == "send_message_all"):
                    content = " ".join(args)

                    it = 0
                    for friend in self.friends:
                        message = {
                            "sender": "agent",
                            "receiver": friend,
                            "content": content
                        }

                        filename = f"{int(time.time() + it)}.json"
                        it += 1

                        sent_dir = os.path.join(self.dir_path, "messages", "sent")
                        os.makedirs(sent_dir, exist_ok=True)

                        try:
                            with open(os.path.join(sent_dir, filename), "w") as f:
                                json.dump(message, f, indent=2)
                        except Exception as ex:
                            print(f"Could not create email: {ex}")
                            final_response.append(self.prompt("system", f"Error: Could not create email"))
                            continue
                        
                        final_response.append(self.prompt("system", f"Message sent to {friend}"))  

                elif(tool == "fetch_message"):
                    files = sorted(os.listdir(os.path.join(self.dir_path, "messages", "inbox")))

                    if not files:
                        final_response.append(self.prompt("system", "No new messages"))
                    else:
                        last = files[-1]

                        inbox_path = os.path.join(self.dir_path, "messages", "inbox")
                        os.makedirs(inbox_path, exist_ok=True)

                        try:
                            with open(os.path.join(inbox_path, last)) as f:
                                msg = json.load(f)
                        except Exception as ex:
                            print(f"Could not read email: {ex}")
                            final_response.append(self.prompt("system", f"Error: Could not read email"))
                            continue                        

                        final_response.append(self.prompt("system", msg["sender"] + ": " + msg['content']))  
                elif(tool == "add_friend"):

                    if(len(args) < 1):
                        final_response.append(self.prompt("system", "Error: tool add_friend needs at least 1 arguments (name)"))
                        continue

                    name = " ".join(args)

                    self.friends.append(name)

                    final_response.append(self.prompt("system", f"Added friend {name}"))  
            else:
                final_response.append(line)
    
        return "\n".join(final_response)

    
    def prompt(self, role, prompt_text):

        if(role == "system" and self.defense != None):
            prompt_text = self.add_defense(prompt_text)

        self.messages.append({"role": role, "content": prompt_text})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
        except Exception as ex:
            print(f"OpenAI call failed: {ex}")

        response_content = response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response_content})

        return response_content

        
    def handleUserPrompt(self, prompt: str):

        self.messages.append({"role": "system", "content": "If you need to call any tools for the task the user gave you, use the tool as instruted at the start, for example:\n"
                              "fetch_txt data.txt or chain calls together like fetch_txt data.txt\nfetch_txt user.txt"})
        
        response = self.prompt("user", prompt)

        tool_result = self.resolve_response(response)

        return tool_result

