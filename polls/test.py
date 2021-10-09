import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# TEst Question
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


# Test home View
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=question_text, pub_date=time)


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
        print(response) 
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


# Test Question Home View
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
