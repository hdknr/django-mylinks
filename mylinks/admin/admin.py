from django.contrib import admin
from django.urls import path
from django.utils.html import mark_safe
from django.template import engines
from django.utils.translation import ugettext_lazy as _
from .. import models
from . import forms, inlines, views


def render(src, request=None, engine_name='django', safe=True, **ctx):
    text = engines[engine_name].from_string(src).render(ctx, request=request)
    return safe and mark_safe(text) or text


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'name', ]


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'anchor', 'site', 'subclass_type']
    list_filter = ['subclass_type']
    exclude = ['created_at', 'updated_at']
    raw_id_fields = ['site', ]
    search_fields = ['title', 'url', ]
    readonly_fields = ['link_and_markdown', 'embed_html', 'site', 'subclass_type', 'visited_at']
    inlines = [
        inlines.LinkTagItemInline,
    ]

    def get_urls(self):
        # https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
        urls = [
            path('add/entry/', views.add_entry, {'admin': self}, name='mylinks_link_add_entry'),
        ]
        return urls + super().get_urls()

    def anchor(self, obj):
        title = obj.title or obj.id
        return mark_safe(f'<a href="{obj.url}" target="_admin">{title}</a>')

    def link_and_markdown(self, obj):
        return mark_safe(
            f'<a href="{obj.url}" target="_admin">'
            f'<i class="fas fa-external-link-alt"></i></a>&nbsp;'
            f'{obj.title}<a href="#" class="markdown" title="{obj.markdown}">&nbsp;'
            f'<i class="far fa-copy"></i></a>')


@admin.register(models.Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site']
    raw_id_fields = ['site', ]
    exclude = ['created_at', 'subclass_type']
    search_fields = ['title', 'url', ]
    readonly_fields = ['markdown', 'html', 'data', 'source']
    inlines = [
        inlines.LinkTagItemInline,
    ]


@admin.register(models.Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Feed._meta.fields]
    exclude = ['created_at']
    readonly_fields = ['updated_at']



@admin.register(models.FeedEntry)
class FeedEntryAdmin(admin.ModelAdmin):
    raw_id_fields = ['link', ]
    list_display = [
        f.name for f in models.FeedEntry._meta.fields
        if f.name not in ['description', 'created_at', 'updated_at']
    ]
    exclude = ['subclass_type', 'created_at', 'description', 'title', 'url', 'feeds', 'feed']
    readonly_fields = [
        'title_and_url', 'html', 'navigates', 
        'feeds', 
        # 'updated_at'
    ]
    list_filter = ['is_read']
    inlines = [
        inlines.LinkTagItemInline,
    ]
    search_fields = ['title', 'description']
    actions = ['mark_as_read', 'mark_as_trashed']

    def navigates(self, obj):
        src = '''
        {% if prev_unread %}<p><a href="{% url 'admin:mylinks_feedentry_change' prev_unread.id %}"> {{ prev_unread.id }}.{{ prev_unread }} </a> </p>{%  endif %}
        {% if next_unread %}<p><a href="{% url 'admin:mylinks_feedentry_change' next_unread.id %}"> {{ next_unread.id }}.{{ next_unread }} </a> </p>{%  endif %}
        '''
        return render(src, current=obj, next_unread=obj.next_unread, prev_unread=obj.prev_unread)

    def title_and_url(self, obj):
        try:
            return self.title_and_url_run(obj)
        except:
            import traceback
            print(traceback.format_exc())


    def title_and_url_run(self, obj):
        src = '''
            <a href="{{ current.link.url }}" target="_feed"><i class="fas fa-external-link-alt"></i></a> &nbsp;
            <span>{{ current.link.title|safe }}</span>&nbsp;
            <a href="#" class="markdown" title="{{ current.markdown_link}}"><i class="far fa-copy"></i></a>
        '''
        return render(src, current=obj)

    def html(self, obj):
        return mark_safe(obj.description)

    def mark_as_read(self, request, queryset):
        counts = queryset.update(is_read=True)
        self.message_user(request, f"{counts} successfully marked as read.")

    mark_as_read.short_description = _('Mark as Read')

    def mark_as_trashed(self, request, queryset):
        counts = queryset.update(is_read=True, trashed=True)
        self.message_user(request, f"{counts} successfully marked as trashed.")

    mark_as_trashed.short_description = _('Mark as Trashed')
