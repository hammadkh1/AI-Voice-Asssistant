# VOICE ASSISTANT WITH SPEECH RECOGNITION

This Python script implements a voice assistant using speech recognition and text-to-speech conversion libraries. It allows users to interact with their computer through voice commands for tasks like opening files, searching the web, checking the time and date, and more.

### FEATURES

- **Speech Recognition**: Utilizes the `speech_recognition` library to recognize user speech input via the microphone.
- **Text-to-Speech Conversion**: Implements text-to-speech conversion using the `pyttsx3` library to provide spoken responses to user queries.
- **File Management**: Allows users to open files by specifying their names through voice commands. It supports searching for files using both Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms.
- **Web Browsing**: Enables users to perform web searches by specifying keywords or URLs.
- **Date and Time**: Provides current date and time upon user request.
- **Calendar**: Opens the system calendar to display the current month.
- **Exit Command**: Allows users to exit the program by saying "exit" or "bye".

### USAGE

1. **Setup Environment**: Ensure that you have Python installed along with the necessary libraries specified in the `import` statements at the beginning of the script.
2. **Run the Script**: Execute the Python script in a terminal or command prompt environment.
3. **Interaction**: Follow the instructions provided by the voice assistant. Speak commands clearly for the assistant to recognize and respond appropriately.
4. **Exit**: To exit the program, say "exit" or "bye".

### DEPENDENCIES

- `speech_recognition`
- `pyttsx3`
- `webbrowser`
- `datetime`
- `calendar`
- `subprocess`

### NOTES

- Ensure that the microphone is properly configured and functional for speech recognition to work effectively.
- The script may need adjustments based on the specific directory structure and file types on your system.
- Additional customization can be done to extend the functionality of the voice assistant according to specific user requirements.
