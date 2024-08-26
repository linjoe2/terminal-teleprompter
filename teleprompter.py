import time
import os
import shutil

def clear_screen():
    """Clears the screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_md_file(file_path):
    """Reads a Markdown file and returns its content as a list of lines."""
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def center_text(text, width):
    """
    Centers the text within the given width.
    
    :param text: String, the line of text to center.
    :param width: Integer, the width to center the text within.
    :return: String, the centered text.
    """
    return text.strip().center(width)

def split_lines_to_max_words(lines, max_words_per_line=5):
    """
    Splits each line into multiple lines with a maximum number of words per line.
    
    :param lines: List of strings, original lines from the file.
    :param max_words_per_line: Integer, maximum number of words allowed per line.
    :return: List of strings, lines split into segments with the specified word limit.
    """
    wrapped_lines = []
    for line in lines:
        words = line.split()
        while len(words) > max_words_per_line:
            wrapped_lines.append(' '.join(words[:max_words_per_line]))
            words = words[max_words_per_line:]
        wrapped_lines.append(' '.join(words))
    return wrapped_lines

def display_teleprompter(lines, delay=1.5, window_size=5):
    """
    Displays lines in a scrolling manner, simulating a teleprompter with centered text and color coding.
    
    :param lines: List of strings, each string representing a line of the teleprompter text.
    :param delay: Time to wait between lines in seconds.
    :param window_size: Number of lines to display at a time.
    """
    num_lines = len(lines)
    terminal_size = shutil.get_terminal_size((80, 20))  # default to 80x20 if size can't be determined
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    for i in range(num_lines):
        clear_screen()
        
        # Calculate the vertical padding to center the text vertically
        visible_lines = min(window_size, num_lines)
        padding_top = (terminal_height - visible_lines) // 2
        
        # Print vertical padding
        print("\n" * padding_top)

        # Display a window of lines centered around the current line
        for j in range(i - window_size // 2, i + window_size // 2 + 1):
            if j < 0 or j >= num_lines:
                continue
            centered_line = center_text(lines[j], terminal_width)
            if j == i:  # Current line in normal color
                print(centered_line)
            else:  # Previous and upcoming lines in light grey
                print(f"\033[90m{centered_line}\033[0m")
        
        time.sleep(delay)

def main():
    file_path = './test.md' #input("Enter the path to your Markdown (.md) file: ")
    
    # Set the default delay to 1.5 seconds
    delay = 1.5

    # Read the file
    lines = read_md_file(file_path)
    if lines is not None:
        # Split lines to have a maximum of 5 words each
        wrapped_lines = split_lines_to_max_words(lines, max_words_per_line=5)
        # Display the teleprompter with scrolling and centered text
        display_teleprompter(wrapped_lines, delay)

if __name__ == "__main__":
    main()

