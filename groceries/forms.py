# home/forms.py
from django import forms


class GroceryInputForm(forms.Form):
    budget = forms.DecimalField(
        label='Grocery Budget',
        max_digits=10,
        decimal_places=2,
        help_text='Enter your budget for groceries'
    )
    dietary_restrictions = forms.CharField(
        label='Dietary Restrictions',
        max_length=255,
        required=False,
        help_text="e.g., vegan, gluten-free"
    )
    favorite_foods = forms.CharField(
        label='Favorite Foods',
        widget=forms.Textarea,
        help_text="List your favorite foods, separated by commas"
    )
