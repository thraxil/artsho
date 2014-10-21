import factory
from artsho.main.models import Show, Picture, Artist, Item, ItemArtist


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
