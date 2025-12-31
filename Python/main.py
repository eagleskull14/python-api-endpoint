# Imports. If you need explaning for this then you shouldn't be using ts lmao.
from flask import Flask, request, jsonify
import pydirectinput; import keyboard
import pyautogui
import threading
import time

# Makes stuff work, up to you if you feel unsafe.
pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

# Flask app setup, duh
app = Flask(__name__)

# General Vars.
presstime = 0.25 # How long to hold keys for "press" actions in games, this number is good for single presses.
keysGame = {} # Remember held keys for games.
keys = {} # Remember held keys for normal keyboard.

# Home, nothing there.
@app.route('/')
def home():
    return "Nothing here, gotta do more digging gang. Try /keyboard or /mouse. For keyboard, use /keyboard/(press|hold|type)?(params). For mouse, use /mouse/(move|click|clickat|scroll|goto)?(params)."

# Keyboard, used to click a single time.
def single(id, game):
    if id == "meta":
        id = "win" if game else "windows"
    if game:
        pydirectinput.keyDown(id)
        time.sleep(presstime)
        pydirectinput.keyUp(id)
    else:
        keyboard.press_and_release(id)

# Keyboard, used to hold / release a key, auto remembers held keys for later, no passthrough as of rn.
def hold(id, game):
    if id == "meta":
        id = "win" if game else "windows"
    if game:
        if id in keysGame and keysGame[id] == "down":
            pydirectinput.keyUp(id)
            keysGame[id] = "up"
        else:
            pydirectinput.keyDown(id)
            keysGame[id] = "down"
    else:
        if id in keys and keys[id] == "down":
            keyboard.release(id)
            keys[id] = "up"
        else:
            keyboard.press(id)
            keys[id] = "down"

# Keyboard yet again, types out whatever is passed + some time if wanted.
def type_text(text, t):
    if t is None:
        t = 0.01
    else:
        t = float(t)
    t = t / len(text)
    pydirectinput.typewrite(text, interval=t)

# Mouse, moves it relitively by a given x and y amount, and with a speed of t given. Uses tweening for smoothness cause who doesnt like smoove.
def move_mouse(x, y, t):
    pyautogui.moveRel(int(x), int(y) * -1, duration=float(t) if t else 0, tween=pyautogui.easeOutCubic)

# Mouse, clicks whatever button is given, and either one time or a dbl click :D
def click_mouse(button, times):
    if times == "double":
        pyautogui.doubleClick(button=button)
    else:
        pyautogui.click(button=button)

# Mouse mouse mouse, it does the click_mouse but moves first to given coords, could be useful i think idk
def clickat_mouse(x, y, button, times):
    pyautogui.moveRel(int(x), int(y))
    if times == "double":
        pyautogui.doubleClick(button=button)
    else:
        pyautogui.click(button=button)

# Mousey Mouse Mouse, scrolls, idk could be nice ig :/
def scroll_mouse(amount):
    pyautogui.scroll(int(amount))

# Mouse again, same as move but to specific coords instead of relative. Also uses tweening cause why not lol :))
def goto_mouse(x, y, t):
    pyautogui.moveTo(int(x), int(y), duration=float(t) if t else 0, tween=pyautogui.easeOutCubic)

# Home for keyboard when no specific action is given
@app.route('/keyboard')
def keyboard_home():
    return "Use /keyboard/(press|hold|type)?(params)."

# Home for keyboard when no specific action is given 2.0
@app.route('/keyboard/')
def keyboard_home2():
    return "Use /keyboard/(press|hold|type)?(params)."

# Home for mouse when no specific action is given
@app.route('/mouse')
def mouse_home():
    return "Use /mouse/(move|click|clickat|scroll|goto)?(params)."

# Home for mouse when no specific action is given 2.0 again
@app.route('/mouse/')
def mouse_home2():
    return "Use /mouse/(move|click|clickat|scroll|goto)?(params)."

# Juicy time, this does all dat mouse stuff :D (move, click, clickat, scroll, goto)
@app.route('/mouse/<type>')
def mouse(type):
    # All of these are self-explanatory based on their names and params, just read the code above. Uses threading to not block the server while doing stuff.
    if(type == "move"):
        x = request.args.get('x')
        y = request.args.get('y')
        t = request.args.get('t')
        if x != None and y != None:
            threading.Thread(target=move_mouse, args=(x, y, t)).start()
            return "Moved Mouse by X:" + str(x) + " Y:" + str(y) + " in " + str(t) + "s."
        else:
            return "Invalid X or Y value, pass along ?x=(x here)&y=(y here)", 400
    elif(type == "click"):
        button = request.args.get('button')
        times = request.args.get('type')
        if button != None and button in ["left", "right", "middle"]:
            threading.Thread(target=click_mouse, args=(button, times)).start()
            if times == "double":
                return "Double Clicked the " + button + " mouse button."
            else:
                return "Clicked the " + button + " mouse button."
        else:
            return "Invalid button, use ?button=(left|right|middle)", 400
    elif(type == "clickat"):
        x = request.args.get('x')
        y = request.args.get('y')
        if x != None and y != None:
            button = request.args.get('button')
            times = request.args.get('type')
            if button != None and button in ["left", "right", "middle"]:
                threading.Thread(target=clickat_mouse, args=(x, y, button, times)).start()
                if times == "double":
                    return "Double Clicked the " + button + " mouse button at X:" + str(x) + " Y:" + str(y) + "." 
                else:
                    return "Clicked the " + button + " mouse button at X:" + str(x) + " Y:" + str(y) + "."
            else:
                return "Invalid button, use ?button=(left|right|middle)", 400
        else:
            return "Invalid X or Y value, use ?x=(x here)&y=(y here)", 400
    elif (type == "scroll"):
        amount = request.args.get('amount')
        if amount != None:
            threading.Thread(target=scroll_mouse, args=(amount,)).start()
            return "Scrolled the mouse by " + str(amount)
        else:
            return "Invalid amount value, give an amount like this: ?amount=(amount here)", 400
    elif (type == "goto"):
        x = request.args.get('x')
        y = request.args.get('y')
        t = request.args.get('t')
        if x != None and y != None:
            threading.Thread(target=goto_mouse, args=(x, y, t)).start()
            return "Moved Mouse to X:" + str(x) + " Y:" + str(y) + " in " + str(t) + "s."
        else:
            return "Invalid X or Y value, give x and y using ?x=(x here)&y=(y here)", 400
    else:
        return "This does not exist on this server.", 404

# Keyboard stuff, does all the stuff. (press, hold, type)
@app.route('/keyboard/<type>')
def button(type):
    # All of these are self-explanatory as well. Also uses threading to not block the server while doing things :D
    if(type == "press"):
        id = request.args.get('id')
        game = request.args.get('game')
        if id != None and (len(id) == 1 or id in ["enter", "shift", "space", "backspace", "tab", "capslock", "delete", "esc", "up", "down", "left", "right", "meta", "ctrl", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]):
            threading.Thread(target=single, args=(id, game, )).start()
            if game:
                return "Pressed " + id + " using pydirectinput."
            else:
                return "Pressed " + id + " using keyboard."
        else:
            return "Invalid Key ID, plz give ?id=(key here)", 400
    elif(type == "hold"):
        id = request.args.get('id')
        game = request.args.get('game')
        reset = request.args.get('reset')
        if reset == True or reset == "True" or reset == "true":
            for key in keys:
                if keys[key] == "down":
                    keyboard.release(key)
                    keys[key] = "up"
            for key in keysGame:
                if keysGame[key] == "down":
                    pydirectinput.keyUp(key)
                    keysGame[key] = "up"
            return "Reset all held keys."
        if id != None and (len(id) == 1 or id in ["enter", "shift", "space", "backspace", "tab", "capslock", "delete", "esc", "up", "down", "left", "right", "meta", "ctrl", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]):
            threading.Thread(target=hold, args=(id, game,)).start()
            if game:
                return "Changed Press State of " + id + " using pydirectinput."
            else:
                return "Changed Press State of " + id + " using keyboard."
        else:
            return "Invalid Key ID, give ?id=(key here) or ?reset=True to reset all held buttons", 400
    elif(type == "type"):
        text = request.args.get('text')
        t = request.args.get('t')
        if text != None:
            threading.Thread(target=type_text, args=(text, t)).start()
            return "Typed out " + text + " in " + str(t) + " seconds."
        else:
            return 'No Text Provided, give ?text="(text here)", and if you want add t=(time to type out message).', 400
    else:
        return "This does not exist on this server.", 404

# run and do it right idk its kinda simple
if __name__ == '__main__':
    app.run(host='0.0.0.0')