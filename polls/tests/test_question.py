import datetime

from django.test import TestCase
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from ..models import Question


class QuestionModelTests(TestCase):
    """Test for Question polls."""

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())

    def test_can_vote(self):
        """can_vote() return true for question enddate is a future time"""
        etime = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=etime)
        self.assertTrue(recent_question.can_vote())

    def test_can_not_vote(self):
        """can_vote() return false for question pubdate is a past time"""
        etime = timezone.now() - datetime.timedelta(hours=3)
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, end_date=etime)
        self.assertFalse(recent_question.can_vote())

    def test_get_pub_date(self):
        """get_pub_date() return string of the pubtime"""
        ptime = timezone.now() - relativedelta(years=3)
        recent_question = Question(pub_date=ptime)
        self.assertEqual(recent_question.pub_date.strftime("%d %b %y [%H:%M]"), recent_question.get_pub_date())

    def test_get_end_date(self):
        """get_pub_date() return string of the endtime"""
        ptime = timezone.now() - datetime.timedelta(days=3)
        etime = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=ptime, end_date=etime)
        self.assertEqual(question.end_date.strftime("%d %b %y [%H:%M]"), question.get_end_date())
