from django import forms
from property_module.models import PropertiesInfo
class SearchPropertyForm(forms.Form):
   pass

class AddPropertiesInfoForm(forms.ModelForm):

   class Meta:
      model = PropertiesInfo
      fields = '__all__'
      widgets ={
               'country':forms.Select(attrs={'aria-label':"Default select example",'class':'form-select', 'id':'country-list','onchange':"get_States(this.value)"}),
               'state':forms.Select(attrs={'aria-label':"Default select example",'class':'form-select form-select', 'id':'state-list','onchange':"get_Cities(this.value)"}),
               'city':forms.Select(attrs={'aria-label':"Default select example",'class':'form-select form-control', 'id':'city-list'}),
               'image':forms.FileInput(attrs={'aria-label':"Default select example",'class':'form-select d-none', 'id':'img-single', 'name':'image'}),
               
            }

   # def __init__(self, *args, **kwargs):
   #    super().__init__(*args, **kwargs)
   #    for field in self.fields.values():
   #       field.widget.attrs.update({'class': 'form-control'})
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      required_fields = ['country','city', 'state']
      for field_name, field in self.fields.items():
         if field_name not in ['country','city', 'state']:  # Exclude city and state fields
            field.widget.attrs.update({'class': 'form-control'})
         if field_name in required_fields:
            field.widget.attrs.update({'required': 'required'})
            field.required = True



class ContactPartiesForm(forms.Form):
   property_id = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class':'form-control',}))

