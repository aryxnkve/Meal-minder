import google.generativeai as genai
import os

from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from fastapi import UploadFile
from PIL import Image
import io

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

desired_output_format = """ The output for each dish should strictly follow the format below:
    **Name:** "Name of the dish"
    **Description:** "A brief one-liner about the dish, emphasizing its main features or what makes it unique."
    **Calories per serving:** "Number of calories per serving."
    **Recipe Ingredients:** "List of main ingredients used in the dish, separated by commas, including any preferred ingredients mentioned."
    **How to Cook:** "Step-by-step cooking instructions on how to prepare the dish."
"""

def prompt_gemini(calorie_limit, cuisine_str, preferred_dishes_str, similar_dishes_list, ingredients_list):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    # Convert lists to comma-separated strings
    preferred_ingredients_str = ", ".join(ingredients_list)
    similar_dishes_str = ", ".join(similar_dishes_list)

    prompt = (
        f"Based on my preference for {cuisine_str} cuisines and enjoyment of dishes like {preferred_dishes_str}, "
        f"which incorporate ingredients such as {preferred_ingredients_str}, and considering a calorie limit of {calorie_limit} calories per dish, "
        f"Generate a list of 5 dishes, each with a detailed description, calorie count, ingredients, and cooking instructions, "
        f"focusing on {cuisine_str} cuisines, and are within this calorie range. Make sure you do not mix the cuisines. "+
        f"Additionally, consider similar dishes like {similar_dishes_str} for inspiration. "+
        desired_output_format
        )
    response = model.generate_content(prompt)
    return response.text


def prompt_gemini_general(calorie_limit=500):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = """Generate a list of 5 dishes, each with a detailed description, calorie count, ingredients, and cooking instructions.
    Please ensure that each dish is under """ + str(calorie_limit) + """calories. 
    Include a range of ingredients to cater to different dietary preferences and cuisines.
    """ + desired_output_format
    
    response = model.generate_content(prompt)
    return response.text


def vision_calorie(files: UploadFile):
    try: 
        image_data = files.file.read()  
        
        cookie_picture = {
            'mime_type': files.content_type,
            'data': image_data  # Assuming the API can take a PIL Image object directly
        }

        output_format = """The output for each dish should strictly follow the format like:
                **Name:** "Name of the dish"\n
                **Calories Per Ingredient:** "Number of calories for each ingredient of the dish and their quantities."\n
                **Total Calories:** "total calories of the dish based on content and for one serving size"\n
                **Calculation:** "Mathematical calulation of Total calories of the dish based on content for one serving size, and calories of each ingredient.\n "
        """
        
        prompt = """Given an image of a dish, please perform the following tasks:

        Identify the Dish: Start by identifying the name of the dish shown in the image.
        List the Ingredients: Detail all visible ingredients that are likely part of the dish for one serving size. Please consider common recipes and ingredients typically used in this dish based on its identification.
        Calculate Calories:
        Individual Ingredients: For each listed ingredient, provide an estimated calorie count per serving size. Utilize standard nutritional values from common food databases or nutritional labels.
        Total Calories: Sum the calories of each ingredient to calculate the total caloric content of one serving of the dish.
        Verification: After calculating, please double-check your mathematical calculations and verify that the sum of the individual ingredient calories accurately matches the total calories reported.
        Objective: The aim is to provide a detailed breakdown of the dish's components and their respective caloric contributions, leading to an accurate total caloric intake for one serving.

        """+ output_format+"""
        Additional Notes:

        Accuracy is key, so please ensure all calculations are precise and double-checked.
        Consider variations in ingredient sizes and preparation methods that may affect the calorie count."""
        
        # Initialize the genai model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Generate content based on the image and the prompt
        response = model.generate_content([prompt, cookie_picture])
    except Exception as e:
        print(str(e))

    return response.text
    
    # return {"response": response.text}


