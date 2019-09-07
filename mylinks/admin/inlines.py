from mytaggit.admin.inlines import GenericTaggedItemInline


class LinkTagItemInline(GenericTaggedItemInline):
    exclude = ['tag', 'value', 'users']
