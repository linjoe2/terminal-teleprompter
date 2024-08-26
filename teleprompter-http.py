from flask import Flask, request, jsonify, send_from_directory
from threading import Thread, Event
import time
import shutil
import os
import logging
import socket
app = Flask(__name__)


# Suppress Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only show errors, suppressing lower-level logs


# Global variables to control the teleprompter
teleprompter_text = ["Welcome to the teleprompter software, please update the text"]
teleprompter_speed = 2.0
teleprompter_running = False
teleprompter_event = Event()
teleprompter_index = 0

def clear_screen():
    """Clears the screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text, width):
    """Centers the text within the given width."""
    return text.strip().center(width)

def split_line(line, max_words=5, max_chars=30):
    """
    Splits a line into multiple lines based on max words or max characters.
    Adds an extra blank line after sentences ending with a period.
    """
    words = line.split()
    new_lines = []
    current_line = []

    for word in words:
        if len(current_line) + len(word.split()) > max_words or len(' '.join(current_line) + ' ' + word) > max_chars:
            new_lines.append(' '.join(current_line))
            current_line = []
        current_line.append(word)
    
    if current_line:
        new_lines.append(' '.join(current_line))

    # Add an extra line if a line ends with a period
    formatted_lines = []
    for line in new_lines:
        formatted_lines.append(line)
        if line.endswith('.'):
            formatted_lines.append("")  # Add an empty line

    return formning, teleprompter_speed

    terminal_size = shutil.get_terminalculate the vertical padding to center the text vertically
        visible_lines = min(5, len(teleprompter_text))
        padding_top = (terminal_height - visible_lines) // 2

        # Print vertical padding
        print("\n" * padding_top)

        # Display a window of lines centered around the current line
        for j in range(teleprompter_index - 2, teleprompter_index + 3):
            if 0 <= j < len(teleprompter_text):
                centered_line = center_text(teleprompter_text[j], terminal_width)
                if j == teleprompter_index:
                    print(centered_line)
                else:
                    print(f"\033[90m{centered_line}\033[0m")

        teleprompter_index = (teleprompter_index + 1) % len(teleprompter_text)
        time.sleep(teleprompter_speed)



@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/play', methods=['POST'])
def play():
    """Start the teleprompter."""
    global teleprompter_running
    teleprompter_running = True
    teleprompter_event.set()
  d"})

@app.route('/pause', methods=['POST'])
def pause():
    """Pause the teleprompter."""
    teleprompter_event.clear()
    return jsonify({"status": "Teleprompter paused"})

@app.route('/set_speed', methods=['POST'])
def set_speed():
    """Set the teleprompter speed."""
    global teleprompter_speed
    data = request.get_json()
    teleprompter_speed = max(float(data.get('speed', 1.5)), 0.1)
    return jsonify({"status": "Speed updated", "speed": teleprompter_speed})

@app.route('/update_text', methods=['POST'])
def update_text():
    """Update the teleprompter text."""
    global teleprompter_text, teleprompter_index
    data = request.get_json()
    raw_text = data.get('text', "").splitlines()
    
    # Split lines according to the word and character limits
    teleprompter_text = []
    for line in raw_text:
        teleprompter_text.extend(split_line(line))

    teleprompter_index = 0
    return jsonify({"status": "Text updated"})


@app.route('/reset', methods=['POST'])
def reset():
    """Reset the teleprompter to its initial state."""
    global teleprompter_text, teleprompter_speed, teleprompter_running, teleprompter_index
    teleprompter_text = []
    teleprompter_speed = 1.5
    teleprompter_running = False
    teleprompteex = max(0, teleprompter_index - 5)
    return jsonify({"status": "Jumped back 5 lines", "index": teleprompter_index})

if __name__ == "__main__":
    # Start the teleprompter thread
    teleprompter_thread = Thread(target=display_teleprompter)
    teleprompter_thread.start()



    # Run the Flask API on port 3000
    app.run(host='0.0.0.0', port=3000)




