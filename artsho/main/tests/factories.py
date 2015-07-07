import factory
from datetime import datetime
from django.contrib.auth.models import User
from artsho.main.models import (
    Show, Picture, Artist, Item, ItemArtist, NewsItem,
    ShowVideo, NewsPicture, Auction, ItemPicture,
    Bid
)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = "testuser"
    email = "test@example.com"


class ShowFactory(factory.DjangoModelFactory):
    class Meta:
        model = Show

    title = "test show"
    year = 2014
    location = "timbuktu"
    description = "a test show"


class PictureFactory(factory.DjangoModelFactory):
    class Meta:
        model = Picture

    show = factory.SubFactory(ShowFactory)
    title = "test picture"
    caption = "test caption"
    image = "pictures/test.jpg"


class ShowVideoFactory(factory.DjangoModelFactory):
    class Meta:
        model = ShowVideo

    show = factory.SubFactory(ShowFactory)
    youtube_id = "6mfvSSl9L9M"


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artist

    name = "attilla the hun"


class NewsItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = NewsItem

    title = "test news item"
    topcontent = "test top content"
    content = "test content"
    published = True


class NewsPictureFactory(factory.DjangoModelFactory):
    class Meta:
        model = NewsPicture

    newsitem = factory.SubFactory(NewsItemFactory)
    caption = "test caption"
    image = "pictures/test.jpg"


class AuctionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Auction

    show = factory.SubFactory(ShowFactory)
    start = datetime.now().date()
    end = datetime.now().date()


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = Item

    title = "test item"
    auction = factory.SubFactory(AuctionFactory)


class ItemArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = ItemArtist

    item = factory.SubFactory(ItemFactory)
    artist = factory.SubFactory(ArtistFactory)


class ItemPictureFactory(factory.DjangoModelFactory):
    class Meta:
        model = ItemPicture

    item = factory.SubFactory(ItemFactory)
    image = "itempictures/test.jpg"


class BidFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bid

    item = factory.SubFactory(ItemFactory)
    user = factory.SubFactory(UserFactory)
