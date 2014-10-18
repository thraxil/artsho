from django.db import models
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
