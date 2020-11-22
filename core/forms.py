from django import forms
from .models import Seller

class DocumentForm(forms.Form):
    choice = (
        # ("Electronics","Electronics"),
        ("Literature and Stationary","Literature and Stationary"),
        # ("Groceries","Groceries"),
    )

    bs_name = forms.CharField(label="Business Name", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    bs_category = forms.ChoiceField(label="Business Category", choices=choice)

    gst_no = forms.CharField(label="GST Number", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))

    pan_no = forms.CharField(label="Pan Number", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))

    bank_ac = forms.CharField(label="Bank AC No", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))

    pan_card = forms.FileField(label='Select File to Upload', help_text="Max Size 10MB")
    addr1 = forms.CharField(label="Address Line 1", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box',
                                    'autocomplete':'address-line1'
                                    }))
    addr2 = forms.CharField(label="Address Line 2", widget=forms.TextInput(
                                attrs={
                                    'class':'text-box',
                                    'autocomplete':'address-line2'
                                    }))
    district = forms.CharField(label="District", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    state = forms.CharField(label="State", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    country = forms.CharField(label="Country", widget=forms.TextInput(
                                attrs={
                                    'required':'True',
                                    'class':'text-box',
                                    'autocomplete':'country'
                                    }))
    pincode = forms.CharField(label="Pincode", widget=forms.TextInput(
                                attrs={
                                    'type':'number',
                                    'required':'True',
                                    'class':'text-box'
                                    }))
    class Meta:
        model= Seller
        fields = ('bs_name', 'bs_category', 'gst_no','pan_no', 'bank_ac', 'pan_card','addr1','addr2','district','country','state','pincode')
    

class DocFileForm(forms.Form):
    docfile = forms.FileField(label='Upload the Excel Sheet', help_text="Max Size 10MB")
    
    
