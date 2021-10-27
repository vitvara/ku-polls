from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q
from .models import Question, Choice
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def pie_chart(request, question_id): # pragma: no cover
    """Show pie chart on data visualize page."""
    question = get_object_or_404(Question, pk=question_id)
    labels = []
    data = []
    result = reverse('polls:polls-results', args=(question.id,))
    queryset = question.choice_set.all()
    for choice in queryset:
        labels.append(choice.text)
        data.append(choice.votes)

    return render(request, 'polls/pie_chart.html', {
        'labels': labels,
        'data': data,
        'result': result,
        'question': question,
    })


class IndexView(ListView):
    """Get the newest 5 polls question and display in ?/polls."""

    template_name = 'polls/home.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, *args, **kwargs):
        """Get a context data."""
        data = super(IndexView, self).get_context_data(*args, **kwargs)
        data['title'] = "List"
        return data

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        query_question = Question.objects.filter(Q(pub_date__lte=timezone.now()) | Q(end_date__isnull=True, pub_date__lte=timezone.now())).order_by('-pub_date')
        return query_question[:5]


class DetailView(DetailView):
    """Display the all choice of the selected question in ?/polls/<question.id>."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Return every question that are published (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(DetailView):
    """Display all vote result of the selected question"""

    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, *args, **kwargs):
        """Get context data."""
        data = super(ResultsView, self).get_context_data(*args, **kwargs)
        data['title'] = "List"
        data['back_home'] = True
        return data

@login_required(login_url='/login/') 
def vote(request, question_id):
    """Save the voting result to question object that user selected"""
    # load question object
    question = get_object_or_404(Question, pk=question_id)
    try:
        # check selected choice
        selected_choice = question.choice_set.get(pk=int(request.POST['choice']))
    except (KeyError, Choice.DoesNotExist):
        # User not select any choice
        # display warning messages
        messages.warning(request, "You didn't select a choice.")
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        # save vote

        if question.end_date != None and question.end_date < timezone.now():
            messages.error(request, "You voted failed! Polls ended")
            return HttpResponseRedirect(reverse('polls:polls-results', args=(question.id,)))
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, "You voted successfully.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:polls-results', args=(question.id,)))

def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_passwd)
            login(request, user)
            return redirect('polls:polls-home')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})