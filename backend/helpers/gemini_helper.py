import google.generativeai as genai
import os


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

if __name__ == '__main__':
    prompt_gemini_general()
