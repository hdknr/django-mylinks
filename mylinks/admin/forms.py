from django import forms
from django.utils.translation import ugettext_lazy as _
from mylinks import models


class Entry(forms.Form):
    url = forms.URLField(required=True)

    def save(self):
        return models.create_entry(self.cleaned_data['url'])
