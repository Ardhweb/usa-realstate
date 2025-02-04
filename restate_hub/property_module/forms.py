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
               'city':forms.Select(attrs={'aria-label':"Default select example",'class':'form-select', 'id':'city-list'}),
               
            }

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
         field.widget.attrs.update({'class': 'form-control'})
