from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_no', 'stop', 'pickup_time', 'drop_time', 'status']  # consistent order

        widgets = {
            'bus_no': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Bus Number',
                'required': True
            }),
            'stop': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Stop',
                'required': True
            }),
            'pickup_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full p-2 border rounded',
            }),
            'drop_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full p-2 border rounded',
            }),
            'status': forms.Select(choices=[
                ('Active', 'Active'),
                ('Inactive', 'Inactive'),
            ], attrs={'class': 'w-full p-2 border rounded'}),
        }
