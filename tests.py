from django.test import TestCase
from django.utils import timezone
from progress.models import Topic, Challenge, Portion


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
        portion.done = True
        t_before = timezone.now()
        portion.save()
        t_after = timezone.now()
        self.assertLess(t_before, portion.done_date)
        self.assertGreater(t_after, portion.done_date)
        portion.description = "Concept draft finished"
        portion.save()
        self.assertGreater(t_after, portion.done_date)
