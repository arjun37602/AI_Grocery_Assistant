from django.shortcuts import render
from django.conf import settings
from .forms import GroceryInputForm
import google.generativeai as genai
import os
genai.configure(api_key=settings.API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro')

# Create your views here.


def home_view(request):
    if request.method == 'POST':
        form = GroceryInputForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            dietary_restrictions = form.cleaned_data['dietary_restrictions']
            favorite_foods = form.cleaned_data['favorite_foods'].split(',')
            context = {
                'form': form,
                'submitted': True,
                'budget': budget,
                'dietary_restrictions': dietary_restrictions,
                'favorite_foods': [food.strip() for food in favorite_foods],
            }
            ai_response = generate_shopping_list(context)
            context['ai_response'] = ai_response
            return render(request, 'index.html', context)
    else:
        form = GroceryInputForm()

    return render(request, 'index.html', {'form': form})


def generate_shopping_list(input_fields):
    # prompt = (
    #     f"Assume you are an AI assistant that recommends "
    #     f"User has a budget of ${input_fields['budget']}. "
    #     f"Dietary restrictions: {input_fields['dietary_restrictions']}. "
    #     f"Favorite foods: {', '.join(input_fields['favorite_foods'])}. "
    #     f"Suggest a grocery shopping list and alternatives within the budget."
    # )
    prompt = (
        f"Assume you are an AI assistant that recommends grocery items and recipes based on user preferences. Also at the end give a single nutrition score out of 10. Limit to 5 items for each category.\n\n"
        f"User has a budget of ${input_fields['budget']}.\n"
        f"Dietary restrictions: {input_fields['dietary_restrictions']}.\n"
        f"Favorite foods: {', '.join(input_fields['favorite_foods'])}.\n\n"
        f"Provide a response in the following format\n\n"
        f"1. **Sample Recipes**:\n"
        f"   - Recipe 1: [Recipe Name]\n"
        f"   - Recipe 2: [Recipe Name]\n"
        f"   - ...\n\n"
        f"2. **Grocery List**:\n"
        f"   - 1. [Item 1], [Cost 1]\n"
        f"   - 2. [Item 2], [Cost 2]\n"
        f"   - ...\n\n"
        f"3. Nutrition Score [nutrition score]"
        f"Ensure that the recipes and grocery list fit within the provided budget and adhere to the dietary restrictions. "
        f"In your response, don't add any unnecessary things for section 1,2,3 other than subsections numbered A, B, C."
        f"Suggest alternatives if necessary to stay within budget."
    )



    response = model.generate_content(prompt)

    ai_response = response.text

    ai_response = ai_response.replace(
        "## Halal-Friendly Grocery List & Recipes for Pizza & Salad Lovers:", "")
    ai_response = ai_response.replace(" - ", "")  # Removing hyphens

    formatted_response = ai_response.replace("\n", "<br>").replace(
        "**", "<strong>").replace("__", "<em>").replace("##", "<strong>")

    print(formatted_response)
    return formatted_response



















###############

    # Extract response text
   # ai_response = response.text
    # print(ai_response)
   # return ai_response
