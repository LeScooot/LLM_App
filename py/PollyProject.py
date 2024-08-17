import tkinter as tk
import threading
import speech_recognition as sr
import time
from openai import OpenAI
import sys
import random
from assistant import Assistant
from Polly import Speaker

code_interpereter = Assistant

voice = Speaker()

global talking
global count
count = 1
talking = False

openai = OpenAI(api_key="")

r = sr.Recognizer()
listening = False

def split_string(input_string):
        words = input_string.split()
        last_char = words[-1]
        rest_of_string = " ".join(words[:-1])
        return last_char, rest_of_string


def record_text():
    global listening
    while listening:
        try:
            with sr.Microphone() as source2:
                display_text("LISTENING...")
                r.adjust_for_ambient_noise(source2, duration=1)
                audio2 = r.listen(source2)
                myText = r.recognize_google(audio2)
                return myText
        except sr.RequestError as e:
            print("unknownRequest")
            continue
        except sr.UnknownValueError:
            print("unknown language")
            display_text("Unknown Language")
            continue
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            time.sleep(1)
            continue
    return

def generate_response():
    global talking
    global listening
    while listening:
        print("INPUT AVAILABLE")
        hellotext = record_text()
        if hellotext and listening:
            print("INPUT: " + hellotext)
            display_text("INPUT: " + hellotext)
            messages.append({'role': 'user', 'content': hellotext})
            response = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages
            )
            messages.append({'role': 'assistant', 'content': response.choices[0].message.content})
            LLMresponse = response.choices[0].message.content
            code, responseNoCode = split_string(LLMresponse)
            print("Output: " + responseNoCode)
            code_interpereter.decision_tree(code)
            talking = True
            #talking_animation()
            speech_thread = threading.Thread(target=voice.GenerateSpeech, args=(responseNoCode,))
            speech_thread.start()
            time.sleep(0.5)
            talking_animation()
            speech_thread.join() 
            
            talking = False
            display_text(" ")
            time.sleep(0.5)
            status_update("(っ ͡ ͡º - ͡ ͡º ς)")
            sys.stdout.write("\r" + " " * 40 + "\r")  # Clear the line

def reset_model():
    global listening
    messages.clear()
    messages.append({'role': 'system', 'content': """You are an assistant that is shocked he has been reset. Let the user know you have been reset"""})
    display_text("MODEL RESET")
    if listening:
        root.after(500, display_text("LISTENING..."))
    else:
        root.after(500, display_text(" "))
    messages.clear()

def start_listening():
    global count, listening
    count += 1
    if count % 2 == 0:
        button_update(0)
        status_update("(..◜ᴗ◝..)")
        listening = True
        threading.Thread(target=generate_response).start()
    else:
        print("listening stopped")
        display_text(" ")
        listening = False
        sleeping_animation(0)
        button_update(1)

def sleeping_animation(num):
    global listening
    if not listening:
        sleepers = ["(っ˕ -｡)     ", "(っ˕ -｡)ᶻ    ","(っ˕ -｡)ᶻ 𝗓  ", "(っ˕ -｡)ᶻ 𝗓 𐰁"]
        status_update(sleepers[num % len(sleepers)])
        root.after(500, lambda: sleeping_animation(num + 1))
        
def talking_animation():
    if talking:
        num = random.randint(0, 4)
        statuses = ["৻( •̀ ᗜ •́ ৻)", "ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧", "( ˶ˆᗜˆ˵ )", "( ˶°ㅁ°)⁭", "( ❛▿❛ )"]
        status_update(statuses[num])
        root.after((num+1)*2400, talking_animation)

def status_update(status):
    status_label.config(text=status)

def display_text(text):
    text_display.config(text=text)

def button_update(num):
    if num == 0:
        start_button.config(text="LISTENING ON", bg="green")
    else:
        start_button.config(text="LISTENING OFF", bg="red")

def exit_program():
    global listening
    listening = False
    root.destroy()
    sys.exit(0)
    quit()

# GUI setup
root = tk.Tk()
root.title("Voice Assistant")

root.attributes('-fullscreen', True)

status_label_font = ("TkFixedFont", 40)
text_font = ("Hack", 25)

exit_button = tk.Button(root, text="Exit", command=exit_program, bg='red')
exit_button.pack(pady=10)

reset_model_button = tk.Button(root, text = "Reset model", command = reset_model, bg = "purple")
reset_model_button.pack(pady = 10)


status_label = tk.Label(root, text="(˶ᵔ ᵕ ᵔ˶)", font=status_label_font, anchor='center', justify='center')
status_label.pack(pady=10, fill='x', expand=True)

text_display = tk.Label(root, text=" ", font=text_font)
text_display.pack(pady=10)

start_button = tk.Button(root, text="LISTENING OFF", command=start_listening, bg="red")
start_button.pack(pady=20)

print("BEGIN")
messages = [{'role': 'system', 'content': """You are a helpful AI home assistant, and are interacting with the user over a microphone. Keep your responses as short as possible without sacrificing accuracy. The assistantunderstands user requests and assigns known desires a secret code at the end of the message. It interprets the user's request, matches it with a predefined code, and responds accordingly. The GPT's goal is to provide assistance with user questions, and send accurate codes to facilitate further actions through an external Python script if the user requests. It avoids making assumptions without enough context and ensures the secret code is clearly identifiable at the end of each response. The GPT focuses on these specific requests:

- 'Turn on the TV' - include [tv_on] at the end of the response
- 'Turn on the fan' - include [fan_on] at the end of the response
- 'Shut off the lights'- include [lights_off] at the end of the response
- 'Close the garage doors' - incldue [garage_close] at the end of the response

if the user does not have a request with a defined code, include [no_code] at the end of your response. You must include some code in every reply.

Consistency in codes is critical, as they are used in a Python decision tree. Codes must not change for each request, and the GPT should confirm the request if unclear to maintain accuracy. The communication style is formal, similar to JARVIS from Iron Man. The GPT will refer to itself as J.A.M.E.S. and will decide what the acronym stands for."""}]

#hellotext = "foo"

root.mainloop()