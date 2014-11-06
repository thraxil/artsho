from django.test import TestCase
from .factories import (
    ShowFactory, PictureFactory, ArtistFactory,
    ItemFactory, ItemArtistFactory, NewsItemFactory,
    AuctionFactory, AuctionItemFactory, BidFactory,
)


class ShowTest(TestCase):
    def test_unicode(self):
        s = ShowFactory()
        self.assertEqual(str(s), "test show")

    def test_get_absolute_url(self):
        s = ShowFactory()
        self.assertEqual(s.get_absolute_url(), "/artsho/1/")


class PictureTest(TestCase):
    def test_unicode(self):
        p = PictureFactory()
        self.assertEqual(str(p), "test picture")

    def test_get_absolute_url(self):
        p = PictureFactory()
        self.assertEqual(p.get_absolute_url(), "/artsho/1/picture/1/")


class ArtistTest(TestCase):
    def test_unicode(self):
        a = ArtistFactory()
        self.assertEqual(str(a), "attilla the hun")

    def test_get_absolute_url(self):
        a = ArtistFactory()
        self.assertEqual(a.get_absolute_url(), "/artist/1/")


class ItemTest(TestCase):
    def test_unicode(self):
        i = ItemFactory()
        self.assertEqual(str(i), "test item")

    def test_get_absolute_url(self):
        i = ItemFactory()
        self.assertEqual(i.get_absolute_url(), "/artsho/1/item/1/")


class ItemArtistTest(TestCase):
    def test_unicode(self):
        ia = ItemArtistFactory()
        self.assertEqual(str(ia), "test item - attilla the hun")


class NewsItemTest(TestCase):
    def test_unicode(self):
        ni = NewsItemFactory()
        self.assertEqual(str(ni), "test news item")


class AuctionTest(TestCase):
    def test_unicode(self):
        a = AuctionFactory()
        self.assertEqual(str(a), "Auction for test show")


class AuctionItemTest(TestCase):
    def test_unicode(self):
        a = AuctionItemFactory()
        self.assertEqual(str(a), "Auction for test show - test item")


class BidTest(TestCase):
    def test_unicode(self):
        a = BidFactory()
        self.assertTrue(str(a).startswith("bid for "))
