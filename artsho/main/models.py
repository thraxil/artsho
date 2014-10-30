from django.db import models
from datetime import datetime
from django.conf import settings
import re
import os.path
from django.template.defaultfilters import slugify
from sorl.thumbnail.fields import ImageWithThumbnailsField


class Show(models.Model):
    title = models.TextField(blank=True, default=u"ARTSHO")
    year = models.IntegerField(default=2014)
    location = models.TextField(blank=True, default=u"")
    description = models.TextField(blank=True, default=u"")

    class Meta:
        ordering = ['year']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/artsho/%d/" % self.id

    def update_picture_order(self):
        self.set_picture_order(self.get_picture_order())

    def update_video_order(self):
        self.set_showvideo_order(self.get_showvideo_order())


class Picture(models.Model):
    show = models.ForeignKey(Show)
    title = models.TextField(blank=True, default=u"")
    caption = models.TextField(blank=True, default=u"")
    image = ImageWithThumbnailsField(
        upload_to="pictures/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        )

    class Meta:
        order_with_respect_to = 'show'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/artsho/%d/picture/%d/" % (self.show.id, self.id)

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "pictures/%04d/%02d/%02d/" % (now.year, now.month, now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename, ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()


class ShowVideo(models.Model):
    show = models.ForeignKey(Show)
    youtube_id = models.TextField()

    class Meta:
        order_with_respect_to = 'show'


class Artist(models.Model):
    name = models.TextField(blank=True, default=u"")
    bio = models.TextField(blank=True, default=u"")
    image = ImageWithThumbnailsField(
        upload_to="artists/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/artist/%d/" % self.id


class Item(models.Model):
    show = models.ForeignKey(Show)
    title = models.TextField(blank=True, default=u"")
    description = models.TextField(blank=True, default=u"")
    medium = models.TextField(blank=True, default=u"")

    class Meta:
        order_with_respect_to = 'show'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.show.get_absolute_url() + "item/%d/" % self.id


class ItemArtist(models.Model):
    item = models.ForeignKey(Item)
    artist = models.ForeignKey(Artist)

    def __unicode__(self):
        return "%s - %s" % (self.item, self.artist)


class NewsItem(models.Model):
    title = models.TextField(blank=True, default=u"")
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    topcontent = models.TextField(blank=True, default=u"")
    content = models.TextField(blank=True, default=u"")

    def __unicode__(self):
        return self.title


class NewsPicture(models.Model):
    newsitem = models.ForeignKey(NewsItem)
    image = ImageWithThumbnailsField(
        upload_to="newspics/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
    )
    caption = models.TextField(blank=True, default=u"")

    class Meta:
        order_with_respect_to = 'newsitem'
