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
    end_date = models.DateTimeField(null=True, blank=True)

    def is_polls_ended(self):
        """check that poll is ended"""
        now = timezone.now()
        return self.end_date <= now

    def was_published_recently(self):
        """Make sure that the question object is not come from the future"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_pub_date(self):
        """Return the passing time"""
        time = timezone.now()
        if time.year > self.pub_date.year:
            return str(time.year - self.pub_date.year) + " year ago"
        elif time.month > self.pub_date.month:
            return str(time.month - self.pub_date.month) + " month ago"
        elif time.day > self.pub_date.day:
            return str(time.day- self.pub_date.day) + " day ago"
        elif time.hour > self.pub_date.hour:
            return str(time.hour - self.pub_date.hour) + " hour ago"
        elif time.minute > self.pub_date.minute:
            return str(time.minute - self.pub_date.minute) + " minute ago"
        elif time.second > self.pub_date.second:
            return str(time.second - self.pub_date.second) + " second ago"
        return self.pub_date
    
    def get_end_date(self):
        """Return remaining time"""
        time = timezone.now()
        if self.end_date.day - time.day <= 1 and self.end_date.month == time.month and self.end_date.year == time.year :
            if self.end_date.day - time.day == 1:
                return "by tomorrow"
            elif self.end_date.hour > time.hour:
                return "within " + str(self.end_date.hour - time.hour) + " hours"
            elif self.end_date.minute > time.minute:
                return "within " + str(self.end_date.minute - time.minute) + " minutes"
            if self.end_date.second > time.second:
                return "within " + str(self.end_date.second - time.second) + " seconds"
        return self.end_date
        
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
