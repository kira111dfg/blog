from django import forms
from django.contrib.auth.models import User
from .models import Comment,Plant

class CommentForm(forms.ModelForm):  
    comment = forms.CharField(  
        widget=forms.Textarea(  
            attrs={  
                "class": "form-control",  
                "placeholder": "Введите текст комментария",  
                "rows": 5  
            }  
        ),  
    )  

    class Meta:  
        model = Comment
        fields = ("comment",)


class PlantForm(forms.ModelForm):
    class Meta:
        model=Plant
        fields=('title','description','image','category','tag')