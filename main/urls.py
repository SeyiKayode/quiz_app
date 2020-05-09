from django.urls import path, include
from .views import main, students, teacher
urlpatterns = [
    path('', main.home, name='home'),

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('courses/', students.StudentCoursesView.as_view(), name='student_courses'),
        path('quiz/<int:pk>/student/results/', students.QuizResultsView.as_view(), name='student_quiz_results'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('list/', students.StudentList.as_view(), name='student_list')
    ], 'main'), namespace='students')),

    path('teachers/', include(([
        path('', teacher.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teacher.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teacher.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teacher.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teacher.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teacher.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teacher.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teacher.QuestionDeleteView.as_view(),
             name='question_delete'),
    ], 'main'), namespace='teachers')),
]










