from langchain.agents import Tool
from openai import OpenAI
from bs4 import BeautifulSoup
# from Selenium import ...
from io import BytesIO
import base64
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_stabilityai = os.getenv("stabilityai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

#SDXL
#DALLE3
#Bsoup
#Method->Tool

def generate_image_with_dalle(prompt):
    AI_Response = client.images.generate(
        model = "dall-e-3",
        size = "1024x1024",
        quality = "hd",
        n = 1,
        response_format = "url",
        prompt = prompt
    )
    
    image_url = AI_Response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"./img/generated_image_{timestamp}.png"

    if not os.path.exists("./img"):
        os.makedirs("./img")
    
    with open(filepath, "wb") as file:
        file.write(image_bytes.getbuffer())

    return f'<a href="{filepath}">HERE IS YOUR IMG!</a>'

def generate_with_SD(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_key_stabilityai}",
    }

    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    data = response.json()

    for image in data["artifacts"]:
        image_bytes = base64.b64decode(image["base64"])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"./img/generated_image_{timestamp}.png"

        if not os.path.exists("./img"):
            os.makedirs("./img")
        
        with open(filepath, "wb") as file:
            file.write(image_bytes)

    return f'<a href="{filepath}">HERE IS YOUR IMG!</a>'

# Coverage Function To Use image generation functions
def get_tool(selected_image_generator):

    if selected_image_generator == "DALL-E 3":
        return Tool (
            name="Generate Image",
            func= generate_image_with_dalle,
            description="""Useful for when you need to generate an image based on given textual instructions or prompts. 
            It returns the filepath where the image saved. This filepath must be given back to the user.
            The filepath is given between HTML tags for turning the address of the image into a link.
            The user must be provided with this HTML style statement that includes the filepath for the saved image.
            """
        )

    elif selected_image_generator == "Stable Diffusion XL":
            return Tool (
            name="Generate Image",
            func= generate_with_SD,
            description="""Useful for when you need to generate an image based on given textual instructions or prompts. 
            It returns the filepath where the image saved. This filepath must be given back to the user.
            The filepath is given between HTML tags for turning the address of the image into a link.
            The user must be provided with this HTML style statement that includes the filepath for the saved image.
            """
        )
# -----------------------------------------------------------------------
def analyze_webpage_BS(target_url):

    response = requests.get(target_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    stripped_content = soup.get_text()

    if len(stripped_content) > 4000:
        stripped_content = stripped_content[:4000]

    return stripped_content

def analyze_webpage_Sel(target_url):
    response = requests.get(target_url)
    html_content = response.text

    # TODO
    # stripped_content=""

    # if len(stripped_content) > 4000:
    #     stripped_content = stripped_content[:4000]

    # return stripped_content

# Coverage Function To Use web-scraping functions
def get_web_tool(selected_web_scraper):
    if selected_web_scraper == "BeautifulSoup":
        return Tool(
            name="Get Webpage",
            func=analyze_webpage_BS,
            description="Useful for when you need to get the http from a specific webpage"
        )

    elif selected_web_scraper == "Selenium":
        return Tool(
            name="Get Webpage",
            func=analyze_webpage_Sel,
            description="Useful for when you need to get the http from a specific webpage"
        )