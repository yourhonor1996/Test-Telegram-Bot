from django.contrib import admin
from src import models


# -------------------------------------------------------
# Inlines

class TakeQuestionInline(admin.TabularInline):
    model = models.TakeQuestion
    verbose_name = "Question"
    verbose_name_plural = "Questions For This Quiz"
    extra = 1

class TakeQuizInline(admin.StackedInline):
    model = models.TakeQuiz
    verbose_name = "Quiz"
    verbose_name_plural = "Quizes This User Has Taken"
    extra = 0
    def has_change_permission(self, request, obj) -> bool:
        return False

class QuestionInline(admin.TabularInline):
    model = models.Question
    verbose_name_plural = "Questions For This Subject"
    extra = 0
    def has_change_permission(self, request, obj) -> bool:
        return False


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
    inlines = [TakeQuizInline]
    
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
    list_display = ['id', 'title']
    list_filter = ['subject']


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'questions_count']
    inlines = [TakeQuestionInline]
