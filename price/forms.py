from django import forms
import time

class SNCF(forms.Form):
    origin = forms.CharField(label='出发点', max_length=100,required=False, initial='Belfort-Montbeliard')
    destination = forms.CharField (label='目的地', max_length=100, required=False,initial='Paris')
    departureDate = forms.DateField(label='出发时间',required=False, widget = forms.DateInput(attrs={'id':'datepicker'}),initial=str(time.strftime ('%Y-%m-%d', time.localtime (time.time ()))))

class UploadFileForm(forms.Form):
    file = forms.FileField()


