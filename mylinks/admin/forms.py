from django import forms
from mylinks import models
from django.utils.translation import ugettext_lazy as _


class LinkForm(forms.ModelForm):
    check_embed = forms.BooleanField(
        label=_('Check Embed'), required=False)

    class Meta:
        model = models.Link
        exclude = ['']

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        check_embed = self.cleaned_data.pop('check_embed')
        if check_embed:
            models.create_entry(self.cleaned_data['url'])
        return instance
