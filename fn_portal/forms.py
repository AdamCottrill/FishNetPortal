

from django import forms
from .models import Gear

#class GearForm(forms.Form):
#
#    gr_label = forms.CharField(label='Gear', max_length=50)
#    gr_code = forms.CharField(label='Gear Code', max_length=4)
#    effcnt = forms.IntegerField(label='Effort Count')
#    effdst = forms.FloatField(label='Effort Distance')
#
#    gr_des_html = forms.CharField(label='Gear Descrition',
#                                  widget=forms.Textarea)
#    #has this gear been confirmed - accurate and correct.
#    confirmed = forms.BooleanField(label='Confirmed')
#    depreciated = forms.BooleanField(label='Depreciated')
#


class GearForm(forms.ModelForm):

    class Meta:
        model = Gear
        fields = (
            'gr_label',
            'gr_des',
            'family',
            'effcnt',
            'effdst',
            'assigned_to',
            'confirmed',
            'depreciated')

    def __init__(self, *args, **kwargs):
        super(GearForm, self).__init__(*args, **kwargs)
        self.fields['gr_label'].label = "Short Description"
        self.fields['gr_des'].label = "Detailed Description"
        self.fields['effcnt'].label = "Effort Count"
        self.fields['effdst'].label = "Effort Distance"
