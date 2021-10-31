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


class QuestionHomeViewTests(TestCase):
    """Question on home page"""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:polls-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        home page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:polls-home'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the home page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:polls-home'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:polls-home'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions home page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:polls-home'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_six_past_questions(self):
        """The questions must show only 5 newest question."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-25)
        create_question(question_text="Past question 3.", days=-20)
        create_question(question_text="Past question 4.", days=-10)
        create_question(question_text="Past question 5.", days=-5)
        create_question(question_text="Past question 6.", days=-1)
        response = self.client.get(reverse('polls:polls-home'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [
                '<Question: Past question 6.>',
                '<Question: Past question 5.>',
                '<Question: Past question 4.>',
                '<Question: Past question 3.>',
                '<Question: Past question 2.>',
            ]
        )
