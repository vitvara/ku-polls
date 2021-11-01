import datetime

from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ..views import vote
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


class ResultViewTest(TestCase):
    """Test result view page"""

    def setUp(self):
        self.fake_request = RequestFactory().request()
        self.login_url = reverse('login')
        self.user_login_data = {
            'username':'test1',
            'password':'test1'
        }
        self.user = User.objects.create(username='test1',email='test1@gmail.com',password='test1')
        self.user.save()
        self.client = Client()


    def test_result_view_page(self):
        """Result page contain list of choice set"""
        past_question = create_question(question_text="Past question 1.", days=-30)
        past_question.choice_set.create(text="ans: 1")
        past_question.choice_set.create(text="ans: 2")
        past_question.choice_set.create(text="ans: 3")
        self.fake_request.POST = {'choice': past_question.id}
        self.fake_request.user = self.user
        vote(self.fake_request, past_question.id)
        self.assertEqual(1, past_question.choice_set.first().votes)
        response = self.client.get(reverse('polls:polls-results', args=[past_question.id]))
        self.assertContains(response, past_question.choice_set.first().text)

