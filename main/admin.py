from django.contrib import admin
from .models import User, Subject, Quiz, Question, Student, Answer, TakenQuiz, StudentAnswer
# Register your models here.


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)