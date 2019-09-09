from django.contrib.admin.views.decorators import staff_member_required
# https://docs.djangoproject.com/ja/2.2/ref/contrib/admin/#django.contrib.admin.views.decorators.staff_member_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _, ngettext
from mylinks import models
from . import forms


def admin_context(admin, request, opts, form,  **extra_context):
    # https://github.com/django/django/blob/master/django/contrib/admin/options.py#L1597
    media = admin.media
    title = extra_context.get('title', '')

    context = {
        **admin.admin_site.each_context(request),
        'title': title,
        'adminform': form,
        'object_id': None,
        'original': None,
        'is_popup': False,
        'to_field': None,
        'media': media,
        'inline_admin_formsets': None,
        'errors': form.errors,
        'preserved_filters': admin.get_preserved_filters(request),
    }
    # https://github.com/django/django/blob/master/django/contrib/admin/options.py#L1122
    app_label = opts.app_label
    context.update({
        'add': True,
        'change': False,
        'has_view_permission': True,
        'has_add_permission': True,
        'has_change_permission': True,
        'has_delete_permission': True,
        'has_editable_inline_admin_formsets': False,
        'has_file_field': False,
        'has_absolute_url': None,
        'absolute_url': None,
        'form_url': None,
        'opts': opts,
        'content_type_id': None,    # TODO
        'save_as': admin.save_as,
        'save_on_top': admin.save_on_top,
        'to_field_var': None,
        'is_popup_var': None,
        'app_label': app_label,
    })

    return context


@staff_member_required
def add_entry(request, admin):
    form = forms.Entry(request.POST or None)

    if form.is_valid():
        instance = form.save()
        if instance:
            name = f"admin:{instance._meta.app_label}_link_change"
            return redirect(name, instance.id)

    context = {
        'title': _('Add Entry'),
    }
    context = admin_context(admin, request, models.Link._meta, form, **context)
    return render(request, 'admin/mylinks/link/add_entry.html', context)