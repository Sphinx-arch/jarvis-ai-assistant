import asyncio  
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"  # Path to the folder containing the images
    prompt = prompt.replace(" ", "_")  # Replace spaces with underscores in the prompt

    # Generate the filenames for images 
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening Image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before closing the image

        except IOError:
            print(f"Unable to open {image_path}")

# API details for hugging face stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"          
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async Function to send a Query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async Function to generate images based on a prompt
async def generate_images(prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra high Details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    # save the generated image to file
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

# Wrapper Function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the asyncio image generation
    open_images(prompt)  # open the generated images

# Main Loop to monitor for image generation requests
while True:

    try:
        # Read the Status and prompt file from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        # If the Status indicates an image generation request
        if Status == "True":
            print("Generating Images ...")
            ImageStatus = GenerateImages(prompt=Prompt)

            # reset the Status in the file after generating images
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")   
                break  # Exit the loop after processing the request

        else:
            sleep(1)  # wait for 1 second before checking again

    except:
        pass