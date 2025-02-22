from membership_module.models import DefaultFeeStructure
from django import forms

class FeeForm(forms.ModelForm):
    class Meta:
        model = DefaultFeeStructure
        fields = '__all__'
        widgets ={
                'member_type':forms.Select(attrs={'class':'form-control form-select w-100'}),
                'setup_fee':forms.NumberInput(attrs={'class':'form-control  w-100'}),\
                'membership_fee':forms.NumberInput(attrs={'class':'form-control  w-100'}),
              
            }
        