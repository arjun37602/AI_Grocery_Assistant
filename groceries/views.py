from django.shortcuts import render
from .forms import GroceryInputForm
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
            return render(request, 'index.html', context)
    else:
        form = GroceryInputForm()

    return render(request, 'index.html', {'form': form})
