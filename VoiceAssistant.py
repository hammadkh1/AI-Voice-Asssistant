# Import necessary modules
import sys  # For system-specific parameters and functions
import speech_recognition as sr  # For speech recognition
import pyttsx3  # For text-to-speech conversion
import os  # For operating system related functions
import webbrowser  # For web browsing
import datetime  # For working with dates and times
import calendar  # For working with calendars
import subprocess  # For running subprocesses
from collections import deque  # For implementing queues

# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Define a function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Define a function to recognize user speech input using the microphone
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio input
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize speech using Google Speech Recognition
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()  # Convert input to lowercase
    except Exception as e:
        print("Sorry, I couldn't understand. Can you please repeat?")
        return "None"


# Define a function to detect and open a file based on user query
def detect_and_open_file(query, root_directory):
    # Define file extensions and initialize variables
    extensions = {"txt": ".txt", "doc": ".doc", "docx": ".docx", "pdf": ".pdf", "ppt": ".ppt", "pptx": ".pptx"}
    query_lower = query.lower()
    base_filename = query_lower
    extension = None

    # Determine file extension based on user query
    for keyword, ext in extensions.items():
        if keyword in query_lower:
            base_filename = query_lower.replace(keyword, "").strip()
            extension = ext
            break

    if base_filename:
        matching_files = []

        # Search for matching files in the root directory and its subdirectories
        for root, dirs, files in os.walk(root_directory):
            for file in files:
                # Check if the file name matches the query and extension (if specified)
                if file.lower().startswith(base_filename.lower()) and (not extension or file.lower().endswith(extension.lower())):
                    file_path = os.path.join(root, file)
                    try:
                        # Open the file using the default application
                        subprocess.Popen(["start", "", file_path], shell=True)
                        matching_files.append(file_path)
                        print(f"Opening {file} at {file_path}")
                        speak(f"Opening {base_filename}.")
                    except Exception as e:
                        print(f"Error opening {file_path}: {e}")
                    return matching_files

        if matching_files:
            return matching_files
        else:
            print(f"No files matching '{query}' found.")
            return []

    return False


# Define a function to close a file
def close_file(file_name):
    try:
        # Terminate the process associated with the file
        os.system(f"taskkill /im {file_name}.exe /f")
        print(f"Closing {file_name}.")
        speak(f"Closing {file_name}.")
    except Exception as e:
        print(f"Error closing {file_name}: {e}")


# Define a function to create a state space representation of the directory structure
def createstatespace(directory):
    state_space = {}

    # Traverse the directory structure
    for root, dirs, files in os.walk(directory):
        node = state_space
        path_parts = os.path.relpath(root, directory).split(os.path.sep)

        # Create nested dictionaries representing directories and files
        for part in path_parts:
            node = node.setdefault(part, {})

        for file in files:
            node[file] = {}

    return state_space


# Define a function to perform Breadth-First Search (BFS) to search for files
def bfs(query, state_space, root_directory):
    query_lower = query.lower()
    matching_files = []

    queue = deque()
    queue.append((root_directory, state_space))

    while queue:
        current_directory, current_state = queue.popleft()

        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            # Check if the item is a file and matches the query
            if os.path.isfile(item_path) and query_lower in item.lower():
                try:
                    # Open the file using the default application
                    subprocess.Popen(["start", "", item_path], shell=True)
                    matching_files.append(item_path)
                    print(f"Opening {item} at {item_path}")
                except Exception as e:
                    print(f"Error opening {item_path}: {e}")

            # Check if the item is a directory and is in the current state space
            elif os.path.isdir(item_path) and item in current_state:
                queue.append((item_path, current_state[item]))

    if matching_files:
        return matching_files
    else:
        print(f"No files matching '{query}' found.")
        return []


# Define a function to perform Depth-First Search (DFS) to search for files
def dfs(query, state_space, current_directory):
    query_lower = query.lower()
    matching_files = []

    stack = [(current_directory, state_space)]

    while stack:
        current_directory, current_state = stack.pop()

        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)

            # Check if the item is a file and matches the query
            if os.path.isfile(item_path) and query_lower in item.lower():
                try:
                    # Open the file using the default application
                    subprocess.Popen(["start", "", item_path], shell=True)
                    matching_files.append(item_path)
                    print(f"Opening {item} at {item_path}")
                except Exception as e:
                    print(f"Error opening {item_path}: {e}")

            # Check if the item is a directory and is in the current state space
            elif os.path.isdir(item_path) and item in current_state:
                stack.append((item_path, current_state[item]))

    if matching_files:
        return matching_files
    else:
        print(f"No files matching '{query}' found.")
        return []


# Define special characters and commands for text processing
special_characters = {"dot": ".", "comma": ",", "number": "#", "dash": "-", " ": ""}
commands = ["search", "search file", "open file", "file open", "view", "open"]


# Define a function to replace special symbols with their corresponding characters
def replace_symbols(text):
    words = text.split()
    replaced_words = []

    for word in words:
        if word in special_characters:
            replaced_word = special_characters[word]
            replaced_words.append(replaced_word)
        else:
            replaced_words.append(word)

    return " ".join(replaced_words)


# Define a function to search the web using a browser
def search_browser(query):
    if "." in query:
        # If the query contains a dot, assume it's a URL and open it directly
        webbrowser.open(query)
    else:
        # Otherwise, perform a Google search
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)


# Define functions to get the current time, date, and open the calendar
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")


def get_date():
    current_date = datetime.date.today()
    speak(f"Today's date is {current_date}.")


def open_calendar():
    speak("Opening calendar.")
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    cal = calendar.month(year, month)
    print(cal)
    speak(cal)


# Main program starts here
if __name__ == '__main__':
    print('Welcome.')
    speak("Hello, I am an AI voice assistant. How may I help you?")
    # Define the root directory for file search
    directo = os.path.expanduser('E:\\')

    while True:
        # Get user command
        query = take_command()

        # Perform actions based on user commands
        if "using BFS" in query:
            # Search using Breadth-First Search algorithm
            base_filename = query.replace("using BFS", "").strip()
            ss = createstatespace(directo)
            bfs(base_filename, ss, directo)
            print(f"Opening {base_filename} with breadth first search algorithm.")

        elif "using DFS" in query:
            # Search using Depth-First Search algorithm
            base_filename = query.replace("using DFS", "").strip()
            ss = createstatespace(directo)
            dfs(base_filename, ss, directo)
            print(f"Opening {base_filename} with depth first search algorithm.")

        # Check for file-related commands
        for command_phrase in commands:
            if command_phrase in query:
                base_filename = query.replace(command_phrase, "").strip().replace(".", "dot")
                if "symbol" in base_filename:
                    # Replace special symbols before file search
                    replaced_query = replace_symbols(base_filename)
                    base_filename = replaced_query.replace("symbol", "").strip().replace(" ", "")
                    detect_and_open_file(base_filename, directo)
                else:
                    detect_and_open_file(base_filename, directo)
            base_filename = None

        # Check for commands related to closing files, browsing, time, date, and calendar
        if "close" in query.lower():
            base_filename = query.replace("close", "").strip()
            print(f"Closing {base_filename}.")
            speak(f"Closing {base_filename}.")
            close_file(base_filename)
            base_filename = None

        elif "browse" in query:
            query = query.replace("browse", "").strip()
            search_browser(query)

        elif "time" in query:
            get_time()

        elif "date" in query:
            get_date()

        elif "calendar" in query:
            open_calendar()

        # Exit the program if requested
        elif "exit" in query or "bye" in query:
            speak("Goodbye!")
            sys.exit()