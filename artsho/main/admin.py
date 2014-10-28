from django.contrib import admin
from .models import (
    Show, Picture, ShowVideo, Artist, Item, ItemArtist, NewsItem,
    NewsPicture)

admin.site.register(Show)
admin.site.register(Picture)
admin.site.register(ShowVideo)
admin.site.register(Artist)
admin.site.register(Item)
admin.site.register(ItemArtist)
admin.site.register(NewsItem)
admin.site.register(NewsPicture)
