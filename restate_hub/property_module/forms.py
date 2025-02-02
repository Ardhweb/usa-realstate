from django import forms
from property_module.models import PropertiesInfo
class SearchPropertyForm(forms.Form):
   pass

class AddPropertiesInfoForm(forms.ModelForm):

   class Meta:
      model = PropertiesInfo
      fields = '__all__'

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
         field.widget.attrs.update({'class': 'form-control'})
