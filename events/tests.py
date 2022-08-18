from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Choice, Event, EventUser, Modes
from .views import MODES_CHOICES_FORMS


class TestEvent(TestCase):
    """Test case docstring."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="lojza", email="asdf@asd.f", password="password")
        self.otheruser = User.objects.create_user(username="lojzafan", email="asdf@asd.f", password="password")
        self.event = Event.objects.create(name="foobar", creator=self.user, mode="DC")
        self.event.save()
        self.event_url = f"/events/{self.event.id}/"
        self.client.login(username="lojza", password="password")

    def test_get_event(self):
        res = self.client.get(self.event_url)
        self.assertEqual(res.status_code, 200)

    def test_event_create(self):
        response = self.client.post("/events/create", {"name": "foo", "mode": "DR"})
        self.assertEqual(response.status_code, 302)
        events = Event.objects.filter(name="foo", creator=self.user)
        self.assertTrue(events)

    def test_event_render_with_choices_and_user_selections(self):
        choice = Choice(event=self.event, dt_from=datetime.now(), dt_to=datetime.now())
        choice.save()
        choice.user.create(user=self.user, display_name="asdf", event=self.event).save()
        res = self.client.get(self.event_url)
        self.assertEqual(res.status_code, 200)

    def test_edit_unauth(self):
        self.client.logout()
        self.client.login(username="lojzafan", password="password")
        res = self.client.get(self.event_url + "edit")
        self.assertEqual(res.status_code, 403)

    def test_edit_auth(self):
        res = self.client.get(self.event_url + "edit")
        self.assertEqual(res.status_code, 200)

    def test_all_choices_have_a_form(self):
        for mode in Event.modes:
            with self.subTest(mode=mode):
                self.assertIn(mode[0], MODES_CHOICES_FORMS.keys())

    def test_choices_adding(self):
        self.assertFalse(Choice.objects.all())
        res = self.client.post(
            self.event_url + "choices",
            {
                "event": self.event.id,
                "dt_from": datetime.now(),
                "dt_to": datetime.now() + timedelta(days=3)
            },
            follow=True
        )
        self.assertTemplateUsed(res, "events/choices.html")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Choice.objects.all())

    def test_choices_adding_dr(self):
        self.assertFalse(Choice.objects.all())
        self.event.mode = str(Modes.DATERANGE)
        self.event.save()
        self.assertFalse(self.event.choices_single_editable)
        res = self.client.post(
            self.event_url + "choices",
            {
                "event": self.event.id,
                "dt_from": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
                "dt_to": (datetime.today() + timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
            },
            follow=True
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "events/event_detail.html")
        self.assertEqual(len(Choice.objects.all()), 4, msg=Choice.objects.all())

    def test_choices_add_wrong_user(self):
        self.client.logout()
        self.client.login(username="lojzafan", password="password")
        res = self.client.post(
            self.event_url + "choices",
            {
                "event": self.event.id,
                "dt_from": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
                "dt_to": (datetime.today() + timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
            }
        )
        self.assertEqual(res.status_code, 403)
        self.assertFalse(Choice.objects.all())

    def test_choices_deleting(self):
        Choice(
            dt_from=datetime.now(),
            dt_to=datetime.now() + timedelta(days=3),
            event=self.event
        ).save()
        self.assertTrue(Choice.objects.all())
        res = self.client.post(
            self.event_url + "choices",
            {
                "_method": "delete",
                "choice_id": Choice.objects.all()[0].id,
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Choice.objects.all())

    def test_choices_deleting_wrong_event(self):
        event = Event(name="asdf", creator=self.user, mode="DR")
        event.save()
        Choice(
            dt_from=datetime.now(),
            dt_to=datetime.now() + timedelta(days=3),
            event=event
        ).save()
        res = self.client.post(
            self.event_url + "choices",
            {
                "_method": "delete",
                "choice_id": Choice.objects.all()[0].id,
            }
        )
        self.assertEqual(res.status_code, 404)
        self.assertTrue(Choice.objects.all())

    def test_add_user_logged(self):
        res = self.client.post(self.event_url + "add_user", {"name": "asdf"})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(EventUser.objects.all())
        self.assertEqual(EventUser.objects.all()[0].user, self.user)

    def test_user_add_anonymous(self):
        self.client.logout()
        res = self.client.post(self.event_url + "add_user", {"name": "asdf"})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(EventUser.objects.all())
        self.assertIsNone(EventUser.objects.all()[0].user)

    # PROBABLY NOT INTEDNED BEHAVIOR
    # def test_user_add_existing(self):
    #     self.client.post(self.event_url + "add_user", {"name": "asdf"})
    #     res = self.client.post(self.event_url + "add_user", {"name": "asdf"})
    #     self.assertEqual(len(EventUser.objects.all()), 1)

    def test_event_choices_date_range(self):
        dt_f = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        dt_t = (dt_f + timedelta(days=3))
        Choice(
            dt_from=dt_f,
            dt_to=dt_t,
            event=self.event
        ).save()
        self.assertEqual(
            self.event.get_date_range(),
            (dt_f, dt_t)
        )

    def test_choices_date_range_multiple(self):
        dt_f = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        dt_m = (dt_f + timedelta(days=1))
        dt_t = (dt_f + timedelta(days=3))
        Choice(
            dt_from=dt_f,
            dt_to=dt_m,
            event=self.event
        ).save()
        Choice(
            dt_from=dt_m,
            dt_to=dt_t,
            event=self.event
        ).save()
        self.assertEqual(
            self.event.get_date_range(),
            (dt_f, dt_t)
        )

    def test_event_choices_date_range_none(self):
        self.assertEqual(
            self.event.get_date_range(),
            (None, None)
        )

    def test_set_date_range(self):
        dt_f = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        dt_m = (dt_f + timedelta(days=1))
        dt_t = (dt_f + timedelta(days=3))
        old = Choice(
            dt_from=dt_f,
            dt_to=dt_m,
            event=self.event
        )
        old.save()
        new = Choice(
            dt_from=dt_m,
            dt_to=dt_t,
            event=self.event
        )
        new.save()
        self.event.set_date_range(dt_f, dt_m)
        self.assertIn(
            old,
            Choice.objects.all()
        )
        self.assertNotIn(
            new,
            Choice.objects.all()
        )


class TestChoiceCreation(TestCase):

    def setUp(self):
        self.client = Client()
        self.otheruser = User.objects.create_user(username="lojzafan", email="asdf@asd.f", password="password")
        self.user = User.objects.create_user(username="lojza", email="asdf@asd.f", password="password")
        self.event = Event.objects.create(name="foobar", creator=self.user, mode="DR")
        self.event.save()
        self.event_url = self.event.get_absolute_url()
        self.client.login(username="lojza", password="password")

        self.dt_a = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        self.dt_b = self.dt_a + timedelta(days=1)
        self.dt_c = self.dt_a + timedelta(days=2)
        self.dt_d = self.dt_a + timedelta(days=3)
        self.dt_e = self.dt_a + timedelta(days=4)
        self.setChoices(self.dt_b, self.dt_d)

    def setChoices(self, datef, datet):
        res = self.client.post(
            self.event_url + "choices",
            {
                "event": self.event.id,
                "dt_from": datef,
                "dt_to": datet
            },
            follow=True
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            self.event.get_date_range(),
            (datef, datet)
        )
        self.assertValidChoices()

    def assertValidChoices(self):
        choices_dates = [x.dt_from for x in self.event.choice_set.all()]
        start, end = self.event.get_date_range()

        count = 0
        while start <= end:
            count += 1
            with self.subTest(start=start, choices_dates=choices_dates):
                self.assertIn(start, choices_dates)
            start += timedelta(days=1)

        self.assertEqual(len(choices_dates), count)

    def test_form_get_mixins_test(self):
        self.client.logout()
        response = self.client.get(f"/events/{self.event.id}/choices")
        self.assertEqual(response.status_code, 302)

    def test_form_get_impostor(self):
        self.client.logout()
        self.client.login(username="lojzafan", password="password")
        response = self.client.get(f"/events/{self.event.id}/choices")
        self.assertEqual(response.status_code, 403)

    def test_form_get_correct(self):
        response = self.client.get(f"/events/{self.event.id}/choices")
        self.assertEqual(response.status_code, 200)

    def test_choices_shrink(self):
        self.setChoices(self.dt_c, self.dt_c)

    def test_choices_same(self):
        self.setChoices(self.dt_b, self.dt_d)

    def test_choices_move(self):
        self.setChoices(self.dt_e, self.dt_e)

    def test_choices_move_touching(self):
        self.setChoices(self.dt_d, self.dt_e)

    def test_choices_move_overlap(self):
        self.setChoices(self.dt_c, self.dt_e)

    def test_choices_expand(self):
        self.setChoices(self.dt_a, self.dt_e)


class TestUserAnswer(TestCase):

    def setUp(self):
        self.otheruser = User.objects.create_user(username="lojzafan", email="asdf@asd.f", password="password")
        self.client = Client()
        self.user = User.objects.create_user(username="lojza", email="asdf@asd.f", password="password")
        self.event = Event.objects.create(name="foobar", creator=self.user, mode="DC")
        self.event.save()
        self.event_url = f"/events/{self.event.id}/"
        self.event_user = EventUser(display_name="asdf", event=self.event, user=self.user)
        self.event_user.save()
        self.user_url = f"/events/{self.event_user.id}/"
        self.dtf = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        self.dtt = self.dtf + timedelta(days=3)
        self.client.login(username="lojza", password="password")
        self.setChoices(self.dtf, self.dtt)

    def setChoices(self, datef, datet):
        res = self.client.post(
            self.event_url + "choices",
            {
                "event": self.event.id,
                "dt_from": datef,
                "dt_to": datet
            },
            follow=True
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            self.event.get_date_range(),
            (datef, datet)
        )

    def test_create_form(self):
        res = self.client.get(
            self.user_url + "edit_answer",
        )
        self.assertEqual(res.status_code, 200, msg=self.user_url + "edit_answer")
        for choice in self.event.choice_set.all():
            with self.subTest(res=res, choice=choice):
                self.assertContains(res, choice.id)

    def test_submit_form(self):
        chosen_choices = Choice.objects.all()[:2]
        res = self.client.post(
            self.user_url + "edit_answer",
            {"choice_set": (x.id for x in chosen_choices)}
        )
        self.assertEqual(res.status_code, 302, msg=self.user_url + "edit_answer")
        self.assertEqual(set(self.event_user.choice_set.all()), set(chosen_choices))
