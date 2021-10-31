import datetime

from django.test import TestCase
from django.utils import timezone
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



class ChoiceTests(TestCase):
    """Test Choice String"""

    def test_choice_str(self):
        """Choice __str__ return name of the answer follow this format<Choice: 'choice_name'>"""
        past_question = create_question(question_text="Past question 1.", days=-30)
        past_question.choice_set.create(text="ans:1")
        self.assertEqual("<QuerySet [<Choice: ans:1>]>", str(past_question.choice_set.all()))


