import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models import Question

def create_question(question_text, days, edays=None):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    if edays is not None:
        etime = timezone.now() + datetime.timedelta(days=edays)
    else:
        etime = None
    ptime = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=question_text, pub_date=ptime, end_date=etime)


class QuestionDetailViewTests(TestCase):
    """Test for question detail page."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:polls-detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:polls-detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.text)

    def test_six_past_question(self):
        """Unlisted question must be accessible."""
        past_question = create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-25)
        create_question(question_text="Past question 3.", days=-20)
        create_question(question_text="Past question 4.", days=-10)
        create_question(question_text="Past question 5.", days=-5)
        create_question(question_text="Past question 6.", days=-1)
        url = reverse('polls:polls-detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.text)