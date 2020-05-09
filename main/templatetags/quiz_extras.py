from django import template
from django.db.models import Sum
from ..models import StudentAnswer

register = template.Library()


@register.simple_tag
def marked_answer(user, opt):
    student_answer = StudentAnswer.objects.filter(student=user.student, answer=opt)
    if student_answer:
        if opt.is_correct:
            return 'correct'
        return 'wrong'
    return ''


@register.filter
def top_subject(taken_quizzes):
    subjects = taken_quizzes.values('quiz__subject__name').annotate(score=Sum('score')).order_by('-score')
    if subjects:
        name = subjects[0]['quiz__subject__name']
        score = subjects[0]['score']
        return f"{name} score:  {score}"
    return ""

















