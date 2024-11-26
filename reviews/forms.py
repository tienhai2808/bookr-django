from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PublisherForm(forms.ModelForm):
  class Meta:
    model = Publisher
    fields = '__all__'
    

class ReviewForm(forms.ModelForm):
  rating = forms.IntegerField(max_value=5, min_value=0)
  class Meta:
    model = Review
    exclude = ('date_edited', 'book')
    
    
SEARCH_TYPES = (
  ("Title", "Title"),
  ("Contributor", "Contributor")
)
class SearchForm(forms.Form):
  search = forms.CharField(min_length=3, required=False)
  search_in = forms.ChoiceField(choices=SEARCH_TYPES, required=False,widget=forms.Select)
  

class BookMediaForm(forms.ModelForm):
  class Meta:
    model = Book 
    fields = ['cover', 'sample']