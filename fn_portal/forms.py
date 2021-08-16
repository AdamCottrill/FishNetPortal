from django import forms
from .models import Gear

# class GearForm(forms.Form):
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
            "gr_label",
            "gr_des",
            "family",
            "effcnt",
            "effdst",
            "assigned_to",
            "confirmed",
            "depreciated",
        )

    def __init__(self, *args, **kwargs):
        super(GearForm, self).__init__(*args, **kwargs)
        self.fields["gr_label"].label = "Short Description"
        self.fields["gr_des"].label = "Detailed Description"
        self.fields["effcnt"].label = "Effort Count"
        self.fields["effdst"].label = "Effort Distance"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# class DataUploadForm(forms.Form):
#     """A simple little form for uploading our tempalte databases one at a time."""

#     file_path = forms.FileField(label="File", required=False)

#     def __init__(self, *args, **kwargs):
#         self.project = kwargs.pop("project")
#         self.user = kwargs.pop("user")
#         super(DataUploadForm, self).__init__(*args, **kwargs)
#         self.fields["file_path"].widget.attrs["size"] = "40"
#         self.fields["file_path"].widget.attrs["class"] = "fileinput"

#     def save(self):
#         """fill in the project, user, uploaded time and file hash when we save
#         it."""

#         fname = str(self.cleaned_data["file_path"])
