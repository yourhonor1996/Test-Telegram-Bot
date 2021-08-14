from django.contrib import admin
from src import models
# TODO make it so that when we want to 

# -------------------------------------------------------
# Inlines

class SessionQuestionInline(admin.TabularInline):
    model = models.SessionQuestion
    verbose_name = "Question"
    verbose_name_plural = "Questions For This Quiz"
    extra = 1

class SessionInline(admin.StackedInline):
    model = models.Session.user.through
    verbose_name = "Session"
    verbose_name_plural = "Sessions This User Has Been In"
    extra = 1
    def has_change_permission(self, request, obj) -> bool:
        return False

class QuestionInline(admin.TabularInline):
    model = models.Question
    verbose_name_plural = "Questions For This Subject"
    extra = 0
    def has_change_permission(self, request, obj) -> bool:
        return False


class SessionAnswerInline(admin.TabularInline):
    model = models.SessionAnswer
    extra = 0
    verbose_name = 'Answer'
    verbose_name_plural = "This Session's Answers"
    # TODO make it so that we don't have to write all readonly fields manually
    # TODO 
    readonly_fields = ['correct_answer']
    can_delete = False

    
    
# TODO create an inline for the session so we can see all the questions that were answered for this (add a one-many relationship from Session to SessionAnswer)
# class SessionQuestionInline2(admin.TabularInline):
#     model = models.Quiz
#     def get_queryset(self, request):
#         # qs = super(SessionQuestionInline2, self).get_queryset(request)
        
#         return models.SessionAnswer.objects.all()
    
# -------------------------------------------------------
# Admins

@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    inlines = [QuestionInline]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'username', 'chat_id']
    list_display_links = ['id', 'full_name']
    inlines = [SessionInline]
    
    fieldsets = (
        (None, {'fields': ('username', 'password', 'chat_id')}),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
            )
        }),
        ('Permissions', {
            'classes': ('collapse', ),
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {
            'classes': ('collapse', ),
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'test_answer']
    list_filter = ['subject']
    list_display_links = ['id', 'title']


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'questions_count']
    list_display_links = ['id', 'title']
    inlines = [SessionQuestionInline]


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'quiz', 'date_taken']
    list_display_links = ['id', 'title']
    inlines = [SessionAnswerInline]
    
@admin.register(models.SessionAnswer)
class SessionAnswerAdmin(admin.ModelAdmin):
    list_display = ['title', 'session', 'question', 'correct_answer', 'date_answered']
    list_display_links = ['title']
    readonly_fields = ['correct_answer']
    
    