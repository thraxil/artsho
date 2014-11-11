import factory
from datetime import datetime
from django.contrib.auth.models import User
from artsho.main.models import (
    Show, Picture, Artist, Item, ItemArtist, NewsItem,
    ShowVideo, NewsPicture, Auction, AuctionItem,
    Bid
)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = "testuser"
    email = "test@example.com"


class ShowFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Show
    title = "test show"
    year = 2014
    location = "timbuktu"
    description = "a test show"


class PictureFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Picture
    show = factory.SubFactory(ShowFactory)
    title = "test picture"
    caption = "test caption"
    image = "pictures/test.jpg"


class ShowVideoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ShowVideo
    show = factory.SubFactory(ShowFactory)
    youtube_id = "6mfvSSl9L9M"


class ArtistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Artist
    name = "attilla the hun"


class ItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Item
    title = "test item"
    show = factory.SubFactory(ShowFactory)


class ItemArtistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ItemArtist
    item = factory.SubFactory(ItemFactory)
    artist = factory.SubFactory(ArtistFactory)


class NewsItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = NewsItem
    title = "test news item"
    topcontent = "test top content"
    content = "test content"
    published = True


class NewsPictureFactory(factory.DjangoModelFactory):
    FACTORY_FOR = NewsPicture
    newsitem = factory.SubFactory(NewsItemFactory)
    caption = "test caption"
    image = "pictures/test.jpg"


class AuctionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Auction
    show = factory.SubFactory(ShowFactory)
    start = datetime.now()
    end = datetime.now()


class AuctionItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AuctionItem
    auction = factory.SubFactory(AuctionFactory)
    item = factory.SubFactory(ItemFactory)


class BidFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Bid
    item = factory.SubFactory(ItemFactory)
    user = factory.SubFactory(UserFactory)
