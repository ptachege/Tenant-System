from django import forms
from django.forms import widgets
from .models import *
from django.contrib.auth.models import User


class TenantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['first_name', 'sur_name', 'last_name', 'id_number', 'gender', 'email', 'contact',
                  ]

    
class UserLogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class CaretakerForm(forms.ModelForm):
    class Meta:
        model = Caretaker
        fields = '__all__'


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = '__all__'

            
        widgets = {
            'apartment': forms.Select(attrs={'class': 'form-control form-control-select2', 'required':'True','name':'apartment', 'placeholder': 'Caretaker'}),
            'house': forms.Select(attrs={'class': 'form-control form-control-select2', 'placeholder': 'Caretaker'}),
            'tenant': forms.Select(attrs={'class': 'form-control form-control-select2', 'placeholder': 'Caretaker'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].queryset = House.objects.none()
        self.fields['apartment'].required = True

        if 'apartment' in self.data:
            try:
                apartment_id = int(self.data.get('apartment'))
                self.fields['house'].queryset = House.objects.filter(apartment_id=apartment_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['house'].queryset = self.instance.apartment.house_set.order_by('house_code')


class PayRentForm(forms.ModelForm):
    class Meta:
        model = PaidRent
        fields = '__all__'

            
        widgets = {
            'apartment': forms.Select(attrs={'class': 'form-control form-control-select2', 'required':'True','name':'apartment', 'placeholder': 'Caretaker'}),
            'house': forms.Select(attrs={'class': 'form-control form-control-select2', 'placeholder': 'Caretaker'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['house'].queryset = House.objects.none()
        self.fields['apartment'].required = True

        if 'apartment' in self.data:
            try:
                apartment_id = int(self.data.get('apartment'))
                self.fields['house'].queryset = House.objects.filter(apartment_id=apartment_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['house'].queryset = self.instance.apartment.house_set.order_by('house_code')


class ApartmentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'

        widgets = {
            'caretaker': forms.Select(attrs={'class': 'form-control form-control-select2', 'placeholder': 'Caretaker'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date_generated']
