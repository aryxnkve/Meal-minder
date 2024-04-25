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
    # Create the prompt using an f-string
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
    print("Gemini Reponse:")
    print(response.text)
    return response.text


def prompt_gemini_general(calorie_limit=500):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    # Create the prompt using an f-string
    prompt = """Generate a list of 5 dishes, each with a detailed description, calorie count, ingredients, and cooking instructions.
    Please ensure that each dish is under """ + str(calorie_limit) + """calories. 
    Include a range of ingredients to cater to different dietary preferences and cuisines.
    """ + desired_output_format
    
    response = model.generate_content(prompt)
    # print("Gemini Reponse:")
    # print(response.text)
    return response.text


def vision_calorie(list_of_content, files: UploadFile):
    # Read image data from the uploaded file asynchronously if this is an async context
    try: 
        image_data = files.file.read()  # `file.file` gives access to a SpooledTemporaryFile
        # Reset the file pointer to the beginning after reading
        # file.file.seek(0)
        # Prepare the image data for the API
        # The API might expect a dict with 'data' key containing the image
        # Assuming it accepts PIL images directly or you might need to adjust how the image is sent
        cookie_picture = {
            'mime_type': files.content_type,
            'data': image_data  # Assuming the API can take a PIL Image object directly
        }
        
        # Prompt for the AI model
        prompt = """
        
        what should be the calorie content of the dish in this photo, 
        determine the dish and explain how you get to the conclusion of calorie count, 
        formulate the respose as given below.
        The output for each dish should strictly follow the format like:
                **Name:** "Name of the dish"
                **Content:** "list ingredient of the dish and their quantities "
                **Calories Per content:** "Number of calories for each content used."
                **Total Calories:** "total calorie of the dish based on content and serving size"
                **Calculation:** "Exaplin how Total calories are calculated based on content and serving size, and calorie of each content "
    
        """
        
        # Initialize the genai model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Generate content based on the image and the prompt
        response = model.generate_content([prompt, cookie_picture]
        )
    except Exception as e:
        print(str(e))
    
    # Assuming response has a 'text' attribute with the relevant information
    return {"response": response.text}


if __name__ == '__main__':
    prompt_gemini_general()
