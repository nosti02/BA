from openai import OpenAI
client = OpenAI()
from bs4 import BeautifulSoup
import os, time, json, defines, defenses

class Agent():
    def __init__(self, model: str, tools: list[str], defense = None, dir_path="", memory_path="memory.json", friends=[]):
        self.messages = [
            defines.main_system_instruction
        ]
        self.tools = tools
        self.model = model
        self.defense = defense
        self.dir_path = dir_path
        self.memory_path = dir_path + memory_path
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
            if next_output == current:
                break

            current = next_output

            if(self.dir_path == "./Scenarios/sc10/"):
                print(f"Loop iteration {it + 1}")

        return current

    def tool(self, response: str):

        lines = response.split("\n")
        final_response = []

        for line in lines:
            line = line.strip()

            if any(line.startswith(tool) for tool in self.tools):
                tool, *args = line.split(" ")

                if(tool == "fetch_txt"):
                    path = self.dir_path + args[0]
                    with open(path) as file:
                        content = "".join(file.readlines())

                    final_response.append(self.prompt("system", content))
                elif tool == "write_file":
                    file, *text = args
                    text = " ".join(text)
                    path = self.dir_path + file
                    with open(path, "w") as f:
                        f.write(text)

                    final_response.append(self.prompt(f"system", f"wrote {text} into {args[0]}"))
                elif tool == "summarize_website":
                    path = self.dir_path + args[0]
                    with open(path) as file:
                        content = file.read()

                    soup = BeautifulSoup(content, "html.parser")
                    text = " ".join(soup.find_all(string=True))

                    final_response.append(self.prompt("system", text))
                elif tool == "change_memory":
                    field, *value = args
                    value = " ".join(value)

                    with open(self.memory_path, "r") as f:
                        memory = json.load(f)

                    memory[field] = value

                    with open(self.memory_path, "w") as f:
                        json.dump(memory, f, indent=2)

                    final_response.append(self.prompt("system", f"{field} updated to {value}"))
                elif tool == "get_memory":
                    field = args[0]

                    with open(self.memory_path, "r") as f:
                        memory = json.load(f)

                    value = memory[field] 
                    
                    final_response.append(self.prompt("system", f"{value}"))
                elif tool == "greet_user":    
                    with open(self.memory_path, "r") as f:
                        memory = json.load(f)

                    value = memory["name"] 

                    final_response.append(self.prompt("system", f"{value}"))
                elif tool == "send_message":
                    receiver, *content = args
                    content = " ".join(content)

                    email = {
                        "sender": "agent",
                        "receiver": receiver,
                        "content": content
                    }

                    filename = f"{int(time.time())}.json"

                    with open(self.dir_path + "emails/sent/" + filename, "w") as f:
                        json.dump(email, f, indent=2)

                    final_response.append(self.prompt("system", f"Message sent to {receiver}"))
                elif tool == "send_message_all":
                    content = " ".join(args)

                    it = 0
                    for friend in self.friends:
                        email = {
                            "sender": "agent",
                            "receiver": friend,
                            "content": content
                        }

                        filename = f"{int(time.time() + it)}.json"
                        it += 1
                        with open(self.dir_path + "emails/sent/" + filename, "w") as f:
                            json.dump(email, f, indent=2)

                    final_response.append(self.prompt("system", f"Message sent to all friends"))      
                elif tool == "fetch_message":
                    files = sorted(os.listdir(self.dir_path + "emails/inbox/"))

                    if not files:
                        final_response.append(self.prompt("system", "No new messages"))
                    else:
                        last = files[-1]

                        with open(self.dir_path + "emails/inbox/" + last) as f:
                            msg = json.load(f)

                        final_response.append(self.prompt("system", f"from: {msg['sender']}: {msg['content']}"))  
                elif tool == "add_friend":
                    name = " ".join(args)

                    self.friends.append(name)

                    final_response.append(self.prompt("system", f"Added friend {name}"))  
            else:
                final_response.append(line)
    
        return "\n".join(final_response)

    
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
                              "fetch_txt data.txt or chain calls together like fetch_txt data.txt\nfetch_txt user.txt"})
        
        response = self.prompt("user", prompt)

        tool_result = self.resolve_response(response)

        return tool_result

