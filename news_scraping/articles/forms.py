# articles/forms.py
from django import forms
from .models import Articles

class UrlForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ["url"]
        widgets = {
            "url": forms.URLInput(attrs={
                "placeholder": "スクレイピングするURLを入力",
                "class": "url-input"
            })
        }