from django.test import TestCase
from django.test.client import Client
from artsho.main.models import NewsItem
from .factories import (
    NewsItemFactory, ShowFactory,
    PictureFactory, ShowVideoFactory,
    NewsPictureFactory, AuctionFactory,
    ItemFactory,
    ItemArtistFactory, ArtistFactory
)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class IndexTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_empty(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_news_item(self):
        NewsItemFactory()
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("test news item" in response.content)


class EditTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username='test', is_staff=True)
        self.u.set_password('test')
        self.u.save()
        self.c.login(username='test', password='test')

    def test_edit_index(self):
        r = self.c.get("/edit/")
        self.assertEqual(r.status_code, 200)

    def test_anonymous(self):
        c = Client()
        r = c.get("/edit/")
        self.assertEqual(r.status_code, 302)

    def test_non_staff(self):
        u2 = User.objects.create(username='test2', is_staff=False)
        u2.set_password('test')
        u2.save()
        self.c.login(username='test2', password='test')
        r = self.c.get("/edit/")
        self.assertEqual(r.status_code, 403)

    def test_edit_show_form(self):
        s = ShowFactory()
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)

    def test_edit_show(self):
        s = ShowFactory()
        r = self.c.post(
            "/edit/show/%d/" % s.id,
            dict(title="new title", year="1999")
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue("new title" in r.content)

    def test_reorder_show_pictures(self):
        s = ShowFactory()
        p1 = PictureFactory(show=s)
        p2 = PictureFactory(show=s)
        r = self.c.post(
            reverse('reorder_show_pictures', args=[s.id]),
            dict(pic_1=p2.id, pic_2=p1.id))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, "ok")

    def test_reorder_show_videos(self):
        s = ShowFactory()
        p1 = ShowVideoFactory(show=s)
        p2 = ShowVideoFactory(show=s)
        r = self.c.post(
            reverse('reorder_show_videos', args=[s.id]),
            dict(video_1=p2.id, video_2=p1.id))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, "ok")

    def test_add_video(self):
        s = ShowFactory()
        r = self.c.post(
            "/edit/show/%d/add_video/" % s.id,
            dict(youtube_id="foobar")
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue("iframe" in r.content)

    def test_delete_picture(self):
        p = PictureFactory()
        r = self.c.post(
            "/edit/picture/%d/delete/" % p.id,
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_add_auction(self):
        s = ShowFactory()
        r = self.c.post(
            reverse('add_auction', args=[s.id]),
            dict(start='2014-11-01', end='2014-11-07'))
        self.assertEqual(r.status_code, 302)

    def test_delete_newspicture(self):
        p = NewsPictureFactory()
        r = self.c.post(
            reverse('delete_newspicture', args=[p.id]),
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_delete_video(self):
        p = ShowVideoFactory()
        r = self.c.post(
            "/edit/showvideo/%d/delete/" % p.id,
            dict()
        )
        self.assertEqual(r.status_code, 302)

    @override_settings(MEDIA_ROOT="/tmp/")
    def test_add_picture(self):
        s = ShowFactory()
        with open('media/img/artsho5_poster.png') as img:
            r = self.c.post(
                "/edit/show/%d/add_picture/" % s.id,
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    @override_settings(MEDIA_ROOT="/tmp/")
    def test_add_newspicture(self):
        s = NewsItemFactory()
        with open('media/img/artsho5_poster.png') as img:
            r = self.c.post(
                reverse('add_news_picture', args=[s.id]),
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    def test_add_picture_unsupported_extension(self):
        s = ShowFactory()
        with open('media/robots.txt') as img:
            r = self.c.post(
                "/edit/show/%d/add_picture/" % s.id,
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    def test_add_newspicture_unsupported_extension(self):
        s = NewsItemFactory()
        with open('media/robots.txt') as img:
            r = self.c.post(
                reverse('add_news_picture', args=[s.id]),
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    def test_add_news_form(self):
        r = self.c.get("/edit/add_news/")
        self.assertEqual(r.status_code, 200)

    def test_add_news_item(self):
        r = self.c.post("/edit/add_news/",
                        dict(
                            title="foo",
                            content="bar",
                            topcontent="baz"))
        self.assertEqual(r.status_code, 302)
        r = NewsItem.objects.filter(title="foo", content="bar",
                                    topcontent="baz", published=False)
        self.assertEqual(r.count(), 1)

    def test_news_drafts_index(self):
        r = self.c.get("/edit/news/drafts/")
        self.assertEqual(r.status_code, 200)

    def test_news_archive_index(self):
        r = self.c.get("/edit/news/")
        self.assertEqual(r.status_code, 200)

    def test_edit_news_item_form(self):
        ni = NewsItemFactory()
        r = self.c.get("/edit/news/%d/" % ni.id)
        self.assertEqual(r.status_code, 200)

    def test_preview_news_item(self):
        ni = NewsItemFactory()
        r = self.c.get("/edit/news/%d/preview/" % ni.id)
        self.assertEqual(r.status_code, 200)

    def test_edit_news_item(self):
        ni = NewsItemFactory()
        r = self.c.post(
            "/edit/news/%d/" % ni.id,
            dict(title="new title"))
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/edit/news/%d/" % ni.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue("new title" in r.content)

    def test_edit_news_item_publish(self):
        ni = NewsItemFactory()
        r = self.c.post(
            "/edit/news/%d/publish/" % ni.id,
            dict())
        self.assertEqual(r.status_code, 302)

    def test_edit_news_item_revert(self):
        ni = NewsItemFactory()
        r = self.c.post(
            "/edit/news/%d/revert/" % ni.id,
            dict())
        self.assertEqual(r.status_code, 302)

    def test_edit_auction_form(self):
        s = AuctionFactory()
        r = self.c.get(reverse('edit_auction', args=[s.id]))
        self.assertEqual(r.status_code, 200)

    def test_edit_auction(self):
        s = AuctionFactory()
        r = self.c.post(
            reverse('edit_auction', args=[s.id]),
            dict(start='2000-01-01', end='3000-01-01')
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get(reverse('edit_auction', args=[s.id]))
        self.assertEqual(r.status_code, 200)
        self.assertTrue("3000" in r.content)

    def test_end_auction(self):
        a = AuctionFactory()
        r = self.c.post(
            reverse('end_auction', args=[a.id]),
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_start_auction(self):
        a = AuctionFactory()
        r = self.c.post(
            reverse('start_auction', args=[a.id]),
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_add_item_to_auction(self):
        a = AuctionFactory()
        r = self.c.post(
            reverse('add_item_to_auction', args=[a.id]),
            dict(
                title="some title",
                artist="foo",
                starting_bid="10",
            )
        )
        self.assertEqual(r.status_code, 302)

    def test_edit_auction_item_form(self):
        ai = ItemFactory()
        r = self.c.get(reverse("edit_auction_item", args=(ai.id,)))
        self.assertEqual(r.status_code, 200)

    def test_edit_auction_item(self):
        ai = ItemFactory()
        r = self.c.post(
            reverse("edit_auction_item", args=(ai.id,)),
            dict(title="new title"))
        self.assertEqual(r.status_code, 302)
        r = self.c.get(reverse("edit_auction_item", args=(ai.id,)))
        self.assertTrue("new title" in r.content)

    def test_delete_auction_item(self):
        ai = ItemFactory()
        r = self.c.post(
            reverse("delete_item", args=(ai.id,)))
        self.assertEqual(r.status_code, 302)

    def test_delete_item(self):
        i = ItemFactory()
        r = self.c.post(
            reverse("delete_item", args=(i.id,)))
        self.assertEqual(r.status_code, 302)

    def test_add_artist_to_item(self):
        ai = ItemFactory()
        r = self.c.post(
            reverse("add_artist_to_item", args=[ai.id]),
            dict(name="new artist"))
        self.assertEqual(r.status_code, 302)
        a = ArtistFactory()
        r = self.c.post(
            reverse("add_artist_to_item", args=[ai.id]),
            dict(artist_id=a.id))
        self.assertEqual(r.status_code, 302)

    def test_delete_itemartist(self):
        ia = ItemArtistFactory()
        r = self.c.post(reverse('remove_artist_from_item', args=[ia.id]))
        self.assertEqual(r.status_code, 302)
        ia = ItemArtistFactory()
        r = self.c.post(reverse('remove_artist_from_item', args=[ia.id]))
        self.assertEqual(r.status_code, 302)

    def test_remove_item_from_auction(self):
        ai = ItemFactory()
        r = self.c.post(
            reverse('remove_item_from_auction', args=[ai.id]))
        self.assertEqual(r.status_code, 302)

    @override_settings(MEDIA_ROOT="/tmp/")
    def test_add_picture_to_item(self):
        i = ItemFactory()
        with open('media/img/artsho5_poster.png') as img:
            r = self.c.post(
                reverse('add_picture_to_item', args=[i.id]),
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    def test_send_broadcast_message(self):
        a = AuctionFactory()
        r = self.c.post(
            reverse('auction_broadcast', args=[a.id]),
            dict(subject='test subject', body='test body')
        )
        self.assertEqual(r.status_code, 302)


class TestAuctionLoggedOut(TestCase):
    def setUp(self):
        self.c = Client()

    def test_details_page(self):
        a = AuctionFactory()
        r = self.c.get(reverse('auction_details', args=[a.id]))
        self.assertEquals(r.status_code, 200)

    def test_simple_bid(self):
        i = ItemFactory(starting_bid=10)
        r = self.c.post(
            reverse('bid_on_item', args=[i.id]),
            dict(bid=11)
        )
        self.assertEqual(r.status_code, 200)
        # make sure the bid didn't get through
        self.assertEqual(i.high_bid(), 10)


class BiddingTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username='test', is_staff=True)
        self.u.set_password('test')
        self.u.save()
        self.c.login(username='test', password='test')

    def test_simple_bid(self):
        i = ItemFactory(starting_bid=10)
        r = self.c.post(
            reverse('bid_on_item', args=[i.id]),
            dict(bid=11)
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(i.high_bid(), 11)

    def test_lower_bid(self):
        i = ItemFactory(starting_bid=10)
        r = self.c.post(
            reverse('bid_on_item', args=[i.id]),
            dict(bid=9)
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(i.high_bid(), 10)

    def test_float_bid(self):
        i = ItemFactory(starting_bid=10)
        r = self.c.post(
            reverse('bid_on_item', args=[i.id]),
            dict(bid=11.2)
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(i.high_bid(), 11)

    def test_invalid_bid(self):
        i = ItemFactory(starting_bid=10)
        r = self.c.post(
            reverse('bid_on_item', args=[i.id]),
            dict(bid='g')
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(i.high_bid(), 10)
