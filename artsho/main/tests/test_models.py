from django.test import TestCase
from artsho.main.models import Artist
from .factories import (
    ShowFactory, PictureFactory, ArtistFactory,
    ItemFactory, ItemArtistFactory, NewsItemFactory,
    AuctionFactory, BidFactory,
    ShowVideoFactory,
)


class ShowTest(TestCase):
    def test_unicode(self):
        s = ShowFactory()
        self.assertEqual(str(s), "test show")

    def test_get_absolute_url(self):
        s = ShowFactory()
        self.assertEqual(s.get_absolute_url(), "/artsho/1/")

    def test_auction(self):
        s = ShowFactory()
        self.assertEqual(s.auction(), None)
        a = AuctionFactory(show=s)
        self.assertEqual(s.auction().id, a.id)

    def test_has_multiple_videos(self):
        s = ShowFactory()
        self.assertFalse(s.has_multiple_videos())

    def test_first_video(self):
        sv = ShowVideoFactory()
        self.assertEqual(sv.show.first_video().id, sv.id)

    def test_rest_videos(self):
        sv = ShowVideoFactory()
        sv2 = ShowVideoFactory(show=sv.show)
        self.assertEqual(sv2.show.rest_videos()[0].id, sv2.id)


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

    def test_add_artist_by_name_new(self):
        i = ItemFactory()
        i.add_artist_by_name("nonexistent")
        r = Artist.objects.filter(name="nonexistent")
        self.assertEqual(r.count(), 1)

    def test_add_artist_by_name_existing(self):
        i = ItemFactory()
        ArtistFactory(name="existing")
        i.add_artist_by_name("existing")
        r = Artist.objects.filter(name="existing")
        self.assertEqual(r.count(), 1)

    def test_high_bid_none(self):
        i = ItemFactory()
        self.assertEqual(i.high_bid(), i.starting_bid)

    def test_high_bid_bids(self):
        i = ItemFactory()
        b = BidFactory(item=i, amount=i.starting_bid + 10)
        self.assertEqual(i.high_bid(), b.amount)


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


class BidTest(TestCase):
    def test_unicode(self):
        a = BidFactory()
        self.assertTrue(str(a).startswith("bid for "))
