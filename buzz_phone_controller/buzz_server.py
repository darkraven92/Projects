from flask import Flask, render_template_string
from pynput.keyboard import Key, Controller
import time

app = Flask(__name__)
keyboard = Controller()

key_maps = {
    '1': {'buzz': 'space', 'blue': '1', 'orange': '2', 'green': '3', 'yellow': '4'},
    '2': {'buzz': 'q',     'blue': 'w', 'orange': 'e', 'green': 'r', 'yellow': 't'},
    '3': {'buzz': 'a',     'blue': 's', 'orange': 'd', 'green': 'f', 'yellow': 'g'},
    '4': {'buzz': 'z',     'blue': 'x', 'orange': 'c', 'green': 'v', 'yellow': 'b'}
}

html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Spelare {{ player_id }}</title>
    <style>
        body { display: flex; flex-direction: column; align-items: center; background-color: #222; margin: 0; height: 100vh; justify-content: space-evenly; font-family: sans-serif; color: white;}
        h1 { margin: 0; font-size: 2rem; color: #ccc; }
        .btn { width: 80%; border-radius: 15px; border: none; font-size: 24px; font-weight: bold; padding: 20px; box-shadow: 0 8px 0 #111; user-select: none; touch-action: manipulation; cursor: pointer;}
        .btn:active { transform: translateY(8px); box-shadow: none; }
        #buzz { background-color: #ff2a2a; color: white; height: 25%; border-radius: 50%; width: 60%; box-shadow: 0 12px 0 #880000;}
        #buzz:active { transform: translateY(12px); box-shadow: none; }
        #blue { background-color: #0088ff; color: white; }
        #orange { background-color: #ff8800; color: white; }
        #green { background-color: #00cc00; color: white; }
        #yellow { background-color: #ffff00; color: black; }
    </style>
</head>
<body>
    <h1>Spelare {{ player_id }}</h1>
    <button id="buzz" class="btn" onclick="sendPress('buzz')">BUZZ!</button>
    <button id="blue" class="btn" onclick="sendPress('blue')">BLÅ</button>
    <button id="orange" class="btn" onclick="sendPress('orange')">ORANGE</button>
    <button id="green" class="btn" onclick="sendPress('green')">GRÖN</button>
    <button id="yellow" class="btn" onclick="sendPress('yellow')">GUL</button>

    <script>
        function sendPress(color) {
            fetch('/press/{{ player_id }}/' + color);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return "<h1 style='font-family:sans-serif; text-align:center; margin-top:50px;'>Skriv /1, /2, /3 eller /4 efter IP-adressen i adressfältet för att välja spelare!</h1>"

@app.route('/<player_id>')
def player(player_id):
    if player_id in key_maps:
        return render_template_string(html_template, player_id=player_id)
    return "Ogiltig spelare. Välj 1, 2, 3 eller 4.", 404

@app.route('/press/<player_id>/<color>')
def press(player_id, color):
    try:
        if player_id in key_maps and color in key_maps[player_id]:
            key_to_press = key_maps[player_id][color]
            if key_to_press == 'space':
                k = Key.space
            else:
                k = key_to_press
                
            keyboard.press(k)
            time.sleep(0.05)
            keyboard.release(k)
            return "OK", 200
        return "Ogiltig knapp", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    print("Servern är igång! Leta upp din dators IP-adress via ipconfig.")
    app.run(host='0.0.0.0', port=5000)