import google.generativeai as genai
import os


GOOGLE_API_KEY = 'AIzaSyDuw6LR8R4ilR3aCNcf08py2ybRlfVh5d8'
# os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

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
        f"Could you suggest a list of 10 new dish names that include similar flavors and ingredients, "
        f"focusing on {cuisine_str} cuisines, and are within this calorie range? Make sure you do not mix the cuisines. "+
        f"Additionally, consider similar dishes like {similar_dishes_str} for inspiration. "
        f"Give me the dish name and a one liner about the dish. "
    )
    response = model.generate_content(prompt)
    print("Gemini Reponse:")
    print(response.text)
    return response.text


if __name__ == '__main__':
    prompt_gemini()

