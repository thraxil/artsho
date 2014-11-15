from django.db import models
from datetime import datetime
from django.conf import settings
import os.path
from django.template.defaultfilters import slugify
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.auth.models import User
import math


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

    def auction(self):
        if self.auction_set.all().count() == 0:
            return None
        else:
            return self.auction_set.all()[0]

    def has_multiple_videos(self):
        return self.showvideo_set.count() > 1

    def first_video(self):
        return self.showvideo_set.all()[0]

    def rest_videos(self):
        return self.showvideo_set.all()[1:]


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
    dirname = "pictures"

    class Meta:
        order_with_respect_to = 'show'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/artsho/%d/picture/%d/" % (self.show.id, self.id)


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


def get_or_create_artist(name):
    r = Artist.objects.filter(name=name)
    if r.exists():
        return r[0]
    else:
        return Artist.objects.create(name=name)


class Auction(models.Model):
    show = models.ForeignKey(Show)
    start = models.DateField(blank=True)
    end = models.DateField(blank=True)
    status = models.CharField(
        default="upcoming",
        max_length=32,
        choices=(
            ("upcoming", "upcoming"),
            ("ongoing", "ongoing"),
            ("completed", "completed"),
        ))

    def __unicode__(self):
        return "Auction for %s" % str(self.show)

    def is_ongoing(self):
        return self.status == 'ongoing'

    def is_completed(self):
        return self.status == 'completed'

    def send_end_of_auction_emails(self):
        pass


class Item(models.Model):
    auction = models.ForeignKey(Auction)
    title = models.TextField(blank=True, default=u"")
    description = models.TextField(blank=True, default=u"")
    medium = models.TextField(blank=True, default=u"")
    starting_bid = models.PositiveIntegerField(default=1)

    class Meta:
        order_with_respect_to = 'auction'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.auction.show.get_absolute_url() + "item/%d/" % self.id

    def add_artist_by_name(self, name):
        name = name.strip()
        if name == "":
            return
        self.add_itemartist(get_or_create_artist(name))

    def add_itemartist(self, artist):
        r = ItemArtist.objects.filter(item=self, artist=artist)
        if r.count() == 0:
            ItemArtist.objects.create(item=self, artist=artist)

    def update_picture_order(self):
        self.set_itempicture_order(self.get_itempicture_order())

    def high_bid(self):
        if self.bid_set.count() > 0:
            return self.bid_set.all().order_by('-amount')[0].amount
        else:
            return self.starting_bid

    def first_picture(self):
        if self.itempicture_set.exists():
            return self.itempicture_set.all()[0]
        else:
            return None

    def bid_suggestion(self):
        h = self.high_bid()
        return int(math.ceil(h * 1.1))


class ItemArtist(models.Model):
    item = models.ForeignKey(Item)
    artist = models.ForeignKey(Artist)

    def __unicode__(self):
        return "%s - %s" % (self.item, self.artist)


class ItemPicture(models.Model):
    item = models.ForeignKey(Item)
    image = ImageWithThumbnailsField(
        upload_to="itempictures/%Y/%m/%d",
        thumbnail={
            'size': (400, 200)
            },
        null=True,
        )
    dirname = "itempictures"

    class Meta:
        order_with_respect_to = 'item'


class Bid(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    amount = models.PositiveIntegerField(default=1)
    entered = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-amount',)

    def __unicode__(self):
        return "bid for $%d on %s by %s at %s" % (
            self.amount, self.item, self.user.email,
            self.entered)


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
    dirname = "newspics"

    class Meta:
        order_with_respect_to = 'newsitem'


def save_image(s, f):
    ext = f.name.split(".")[-1].lower()
    basename = slugify(f.name.split(".")[-2].lower())[:20]
    if ext not in ['jpg', 'jpeg', 'gif', 'png']:
        # unsupported image format
        return None
    now = datetime.now()
    path = "%s/%04d/%02d/%02d/" % (s.dirname, now.year, now.month, now.day)
    try:
        os.makedirs(settings.MEDIA_ROOT + "/" + path)
    except:
        pass
    full_filename = path + "%s.%s" % (basename, ext)
    fd = open(settings.MEDIA_ROOT + "/" + full_filename, 'wb')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()
    s.image = full_filename
    s.save()
