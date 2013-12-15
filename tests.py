import doctest

from django.test import TestCase
from django.utils import timezone

from . import models
from .models import Topic, Challenge, Portion


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(models))
    return tests


class TopicTest(TestCase):

    def test_updated_date(self):
        topic = Topic.objects.create(title="Concurrency")
        self.assertEqual(topic.created_date, topic.updated_date())
        challenge = Challenge.objects.create(name="Go language demo",
                description="Implement the web crawler from the Go language demo",
                topic=topic)
        self.assertNotEqual(topic.created_date, topic.updated_date())


class PortionTest(TestCase):

    def test_relative_size(self):
        topic = Topic.objects.create(title="Perl")
        challenge = Challenge(name="Programming Perl",
                description="Read the camel book", topic=topic)
        # TODO Finish writing test_relative_size()

    def test_done_date(self):
        topic = Topic.objects.create(title="Web dev")
        challenge = Challenge.objects.create(name="Javascript drag-and-drop",
                description="Implement basic drag-and-drop widget",
                topic=topic)
        portion = challenge.portions.create(description="Concept finished")
        self.assertIsNone(portion.done_date)

        portion.status = Portion.DONE
        t_before = timezone.now()
        portion.save()
        t_after = timezone.now()
        self.assertLess(t_before, portion.done_date)
        self.assertGreater(t_after, portion.done_date)

        portion.description = "Concept draft finished"
        portion.save()
        self.assertGreater(t_after, portion.done_date)

    def test_challenge_done(self):
        topic = Topic.objects.create(title="Vim")
        challenge = Challenge.objects.create(name="Practical Vim",
                description="Read the book", topic=topic)
        self.assertFalse(Challenge.objects.get(pk=challenge.pk).done)

        chapter1 = challenge.portions.create(description="Chapter 1")
        chapter2 = challenge.portions.create(description="Chapter 2", status=Portion.DONE)
        self.assertFalse(Challenge.objects.get(pk=challenge.pk).done)

        chapter1.status = Portion.DONE
        chapter1.save()
        self.assertTrue(Challenge.objects.get(pk=challenge.pk).done)

        challenge.portions.create(description="Chapter X", status=Portion.DONE)
        chapter2.status = Portion.OPEN
        chapter2.save()
        self.assertFalse(Challenge.objects.get(pk=challenge.pk).done)

        chapter2.delete()
        self.assertTrue(Challenge.objects.get(pk=challenge.pk).done)

    def test_skipped_status(self):
        pass  # TODO
