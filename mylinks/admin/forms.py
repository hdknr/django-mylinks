from django import forms
from django.utils.translation import ugettext_lazy as _
from mylinks import models


class Entry(forms.Form):
    url = forms.URLField(required=True)

    def save(self):
        return models.create_entry(self.cleaned_data['url'])


class FeedEntryForm(forms.ModelForm):

    tags = forms.CharField(required=False)

    class Meta:
        model = models.FeedEntry
        exclude = []

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        tags = [i.strip() for i in self.cleaned_data.get('tags', '').split(',')]
        res.link and res.link.tags.add(*tags)
        return res
