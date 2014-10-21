from django.contrib import admin
from .models import Show, Picture, Artist, Item, ItemArtist

admin.site.register(Show)
admin.site.register(Picture)
admin.site.register(Artist)
admin.site.register(Item)
admin.site.register(ItemArtist)
