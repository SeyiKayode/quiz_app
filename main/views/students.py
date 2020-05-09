from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django.views import View
from ..decorators import student_required
from ..forms import StudentSignUpForm, StudentCoursesForm, TakeQuizForm
from ..models import Student, Quiz, Question, TakenQuiz

User = get_user_model()


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentCoursesView(UpdateView):
    model = Student
    form_class = StudentCoursesForm
    template_name = 'main/students/courses_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self, queryset=None):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Courses have been updated')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ['name']
    context_object_name = 'quizzes'
    template_name = 'main/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.exclude(pk__in=taken_quizzes).annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_subjects'] = self.request.user.student.courses.values_list('pk', flat=True)
        return context


@method_decorator([login_required, student_required], name='dispatch')
class QuizResultsView(View):
    template_name = 'main/students/quiz_result.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(id=kwargs['pk'])
        taken_quiz = TakenQuiz.objects.filter(student=request.user.student, quiz=quiz)
        if not taken_quiz:
            return render(request, 'main/404.html')
        questions = Question.objects.filter(quiz=quiz)
        context = {
            'questions': questions,
            'quiz': quiz,
            'percentage': taken_quiz[0].percentage
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'main/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student
    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'main/students/taken_quiz_list.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(
                        answer__question__quiz=quiz, answer__is_correct=True).count()
                    percentage = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=correct_answers, percentage=percentage)
                    student.score = TakenQuiz.objects.filter(student=student).aggregate(Sum('score'))['score__sum']
                    student.save()
                    messages.success(request, 'Your score for the quiz %s is %s' % (quiz.name, percentage))
                    return redirect('students:student_quiz_results', pk)
    else:
        form = TakeQuizForm(question=question)
    context = {
        'form': form,
        'quiz': quiz,
        'question': question,
        'progress': progress,
        'answered_questions': total_questions - total_unanswered_questions,
        'total_questions': total_questions
    }
    return render(request, 'main/students/take_quiz_form.html', context)


@method_decorator([login_required, student_required], name='dispatch')
class StudentList(ListView):
    model = Student
    template_name = 'main/students/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Student.objects.order_by('-score')
        if query:
            queryset = queryset.filter(user__username__icontains=query)
        return queryset














































































































































