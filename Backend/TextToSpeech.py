import pygame 
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load the environment
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Get the AssistanceVoice from environment variable

# Asynchronous to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"  # define the path where the speech file will be saved

    if os.path.exists(file_path):  # Check if the file already exists
        os.remove(file_path)  # If it does, delete it

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r'Data\speech.mp3')  # Save the generated speech as MP3 File

# Function to manage text-to-speech(TTS) functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()

            # Load generated speech file into pygame mixer
            pygame.mixer.music.load(r'Data\speech.mp3')
            pygame.mixer.music.play()

            # Loop until the audio file is finished playing
            while pygame.mixer.music.get_busy():
                if func() == False:  # Check if the external function returns false
                    break
                pygame.time.Clock().tick(10)  # Limit the loop to 10 iterations per second

            return True  # return true if the audio played successfully

        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                # Call the provided function with false to signal the end of TTS
                func(False) 
                pygame.mixer.music.stop()  # Stop the audio playback
                pygame.mixer.quit()  # Quit the pygame mixer

            except Exception as e:  # Include any exceptions during cleanup
                print(f"Error in finally block: {e}")

# Function to manage text-to-speech(TTS) with additional responses with long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")  # Split the text by periods into a list of sentences

    # List of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If text is very long (more than 4 sentences and 250 characters), add a response message
    if len(Data) > 4 and len(Text) > 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func) 

    # Otherwise just play the whole text
    else:
        TTS(Text, func)

# Main Execution loop
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech Function
        TextToSpeech(input("Enter the text: "))
