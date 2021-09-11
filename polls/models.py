from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    """
    Stores a set of Question and Question's choice

    Property
    --------
    text: str
        Question text, max max_length 200

    pub_date: datetime
        Time that the question has been created.
    """
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def was_published_recently(self):
        """Make sure that the question object is not come from the future"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    Store Choice object that related to :model: `polls.Question`

    Property
    --------
    question: Question
        Question object where the Choice is.
    text: str
        Choice text, max length 200.

    vote: int
        Number of vote for that choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
