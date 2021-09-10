from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='polls-home'),
    path('<int:pk>/', views.DetailView.as_view(), name='polls-detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='polls-results'),
    path('<int:question_id>/vote', views.vote, name='polls-vote'),
    path('<int:question_id>/pie-chart/', views.pie_chart, name='polls-pie-chart'),
]
