from django import forms
from . models import Video, UserProfile

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']



from django import forms

class UpgradeForm(forms.Form):
    CARD_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express')
    ]
    
    card_type = forms.ChoiceField(choices=CARD_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(max_length=19, label="Card Number")
    expiry_date = forms.CharField(max_length=7, help_text="MM / YYYY")
    cvc = forms.CharField(max_length=4, widget=forms.PasswordInput)