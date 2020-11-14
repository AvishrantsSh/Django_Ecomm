from django import forms
from .models import Seller

class DocumentForm(forms.Form):
    choice = (
        ("-","-"),
        ("Electronics","Electronics"),
        ("Stationary","Stationary"),
        ("Art and Craft","Art and Craft"),
        ("Grocery","Grocery"),
    )

    bs_name = forms.CharField(label="Business Name", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    bs_category = forms.ChoiceField(label="Business Category", choices=choice)

    reg_no = forms.CharField(label="Registration Number", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    
    bank_ac = forms.CharField(label="Bank AC No", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))

    id_card = forms.FileField(label='Select File to Upload', help_text="Max Size 10MB")

    class Meta:
        model= Seller
        fields = ('bs_name', 'bs_category', 'reg_no','bank_ac', 'id_card')

