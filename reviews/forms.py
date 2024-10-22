from django import forms
from django.core.exceptions import ValidationError
from .models import Publisher, Review

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

# def validate_email_domain(value):
#   if value.split("@")[-1].lower() != "example.com":
#     raise ValidationError("The email address must be on the domain example.com.")
  
# class OrderForm(forms.Form):
#   magazine_count = forms.IntegerField(min_value=0, max_value=80, widget=forms.NumberInput(attrs={"placeholder":"Number of Magazines"}))
#   book_count = forms.IntegerField(min_value=0, max_value=50, widget=forms.NumberInput(attrs={"placeholder":"Number of Books"}))
#   send_confirmation = forms.BooleanField(required=False)
#   email = forms.EmailField(required=False, validators=[validate_email_domain], widget=forms.EmailInput(attrs={"placeholder":"Your company email address"}))
  
#   def clean_email(self):
#     return self.cleaned_data['email'].lower()
  
#   def clean(self):
#     cleaned_data = super().clean()
#     if cleaned_data["send_confirmation"] and not cleaned_data.get("email"):
#       self.add_error("email", "Please enter an email address to receive the confirmation message.")
#     elif cleaned_data.get("email") and not cleaned_data["send_confirmation"]: 
#       self.add_error("send_confirmation", "Please check this if you want to receive a confirmation email.")