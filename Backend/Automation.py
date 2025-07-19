#import required librabries
from AppOpener import close, open as appopen # import functions to open and close apps
from webbrowser import open as webopen # Import web browser functionality
from pywhatkit import search, playonyt # Import function for Google search and youtuber playback
from dotenv import dotenv_values # Import function to load environment variables from .env file
from bs4 import BeautifulSoup # Import function to parse HTML and XML documents
from rich import print # import rich for styled console output
from groq import Groq # import froq for AI chat functionalities
import webbrowser # import webbrowser for opening URLs.
import subprocess # import subprocess for interacting with system
import requests # import requests for making HTTP requests
import keyboard # import keyboard for keyboard related actions
import asyncio # import asyncio for asynchronous programming
import os # import os for interacting with operating system

# load environment variables from .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # load Groq API key from .env file

# Define CSS classes for parsing specifec elements in HTMl Content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", 
           "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", 
           "dDoNo ikb4bB gsrt", "sXLaOe",
            "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# initialize Groq Client with API key
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interaction
professional_statement = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need.",
]

# List to store chatbot messages
messages = []

# System message to provide context to chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform a google search
def GoogleSearch(Topic):
    search(Topic) # use pywhatkit's search function to perform a Google search
    return True # Indicate Success

# Function to generate content using Ai and save it to a file
def Content(Topic):

    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe' # Default text editor
        subprocess.Popen([default_text_editor, File]) # Open the file in the default text editor

    # Nested function to generate content using the Ai chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add user's prompt to messages
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # SPECIFY THE AI MODEL
            messages=SystemChatBot + messages, # Include System instructions and chat history
            max_tokens=2048, # limit number of tokens in response
            temperature=0.7, # adjust the temperature of the response
            top_p=1, # Use nucleus sampling for response diersity
            stream=True, # Enable streaming Response
            stop=None # Allow the model to determine stopping conditions.
        )

        Answer = "" # Initialize an empty string for the response

        # Process Streamed response Chunk
        for chunk in completion:
            if chunk.choices[0].delta.content: # Check for content in the current chunk
                Answer += chunk.choices[0].delta.content # Append the content to the Answer

        Answer = Answer.replace("</s>", "") # Remove unwanted token from the response
        messages.append({"role": "assistant", "content": Answer}) # Add the Ai response to messages
        return Answer

    Topic: str = Topic.replace("Content ", "") # remove content from the topic
    ContentByAI = ContentWriterAI(Topic) # Generate Content using Ai        

    # Save the generated content to text file
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # write the content to the file
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt") # open the file in notepad    
    return True # Indicate Success

# Function to search for a topic on youtube
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the Youtube search URL
    webbrowser.open(Url4Search) # Open the URL in the default browser
    return True

# Function to play a video on Youtube
def PlayYouTube(query):
    playonyt(query) # use pywhatkit playonyt
    return True 

# Function to Open an Application or a relevant webpage.
def OpenApp(app, sess=requests.session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # Attempt to open the app.
        return True
    
    except:
        # Nested Function to extract links from HTML Content
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') # Parse the HTML Content
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # Find the relevant links
            return [link.get('href') for link in links] # Return the links
        
        # Nested function to perform a Google Search and retrieve HTML
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # Construct the Google Search URL
            headers = {'User-Agent': useragent} # Set pre defined the User-Agent 
            response = sess.get(url, headers=headers) # Send a GET request to the URL

            if response.status_code == 200:
                return response.text # Return the HTML content
            else:
                print("Failed to retrieve search results.") # Print an error message
            return None

        search_query = app.strip().replace(" ", "+")  # Focus search on app websites
        search_url = f"https://www.google.com/search?q={search_query}"
        print(f"[bold yellow]App not found. Opening search: {search_url}[/bold yellow]")
        webopen(search_url)

        return True    

# Function to close an application
def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app.
            return True # Indicate Success
        except:
            return False # Indicate Failure
    
# Function to Execute System level command
def System(command):

    # Nested Function to mute the System Volume
    def mute():
        keyboard.press_and_release("volume mute") # Simulate the mute key press

    # Nested Function to unmute the System Volume
    def unmute():
        keyboard.press_and_release("volume mute") # Simulate the unmute key press (note: "volume unmute" doesn't exist)

    # Nested Function to increase the System Volume
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the volume up key press    

    # Nested Function to decrease the System Volume
    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the volume down key press    

    # Execute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True # indicate Success

# Asynchronous Function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):

    funcs = [] # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "): # handle "Open" Commands

            if "open it" in command: # Ignore "open it" commands.
                pass

            if "open file" == command: # Ignore "open files" commands
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule the app opening
                funcs.append(fun)

        elif command.startswith("general "): # Placeholder for general command
            pass

        elif command.startswith("realtime "): # Placeholder for real-time commands
            pass

        elif command.startswith("close "): # Handle "close " commands
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule the app closing
            funcs.append(fun)

        elif command.startswith("play "): # Handle the play command
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play ")) # Schedule youtube playback
            funcs.append(fun)

        elif command.startswith("content "): # Handle the content command
            fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content creation
            funcs.append(fun)

        elif command.startswith("google search "): # Handle google search command
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule google search
            funcs.append(fun)

        elif command.startswith("youtube search "): # Handle youtube search command
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # Schedule youtube search.
            funcs.append(fun)

        elif command.startswith("system "): # Handle the system command
            fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule system command execution
            funcs.append(fun)

        else:
            print(f"No Function Found: For {command}") # Print an error message if no function is found.

    results = await asyncio.gather(*funcs) # Execute all tasks concurrently

    for result in results: # Process the results
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands): # Translate and execute commands
        pass

    return True # Indicate Success
