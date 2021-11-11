from django.contrib import admin
from django.urls import path

from api.views import AdminPolls, AdminPollsUpdateDestroy, AdminQuestions, AdminQuestionsUpdateDestroy, UserPolls, \
    UserPollsID, UserPollsWithAnswers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/polls', AdminPolls.as_view()),
    path('admin/polls/<int:pk>', AdminPollsUpdateDestroy.as_view()),
    path('admin/questions', AdminQuestions.as_view()),
    path('admin/questions/<int:pk>', AdminQuestionsUpdateDestroy.as_view()),
    path('polls', UserPolls.as_view()),
    path('polls/<int:id>', UserPollsID.as_view()),
    path('polls_done/<int:id>/', UserPollsWithAnswers.as_view()),

]
