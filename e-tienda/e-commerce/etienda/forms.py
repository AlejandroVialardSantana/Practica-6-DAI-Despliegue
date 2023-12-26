from django import forms
from django.core.exceptions import ValidationError

class ProductForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    price = forms.FloatField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    category = forms.CharField(max_length=255, required=True)
    image = forms.FileField(required=False, label="Image")

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError('The price must be greater than zero.')
        return price

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title[0].isupper():
            raise ValidationError('The title must start with an uppercase letter.')
        return title