from django.urls import path
from link_aggregator import views


urlpatterns = [
    path('links', views.handleLink),
    path('links/<int:id>/upvote', views.increaseVote),
    path('links/<int:id>/downvote', views.decreaseVote),
]
