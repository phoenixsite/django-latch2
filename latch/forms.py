from django.forms import ModelForm
from django import forms

from latch.models import LatchSetup


class LatchPairForm(forms.Form):
    latch_pin = forms.CharField()


class LatchSetupForm(ModelForm):
    exclude = []
    class Meta:
        model = LatchSetup
        fields = '__all__'


class LatchUnpairForm(forms.Form):
    latch_confirm = forms.BooleanField()
