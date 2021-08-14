from django.core.checks.messages import Error
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# TODO create an Answer model for saving the answers.
# TODO limit the test answer to 1 to 4 

# create your models here
class User(AbstractUser):
    chat_id = models.BigIntegerField(unique= True, null= True)
    first_name = models.CharField(max_length=50, null= True, blank= True)
    last_name = models.CharField(max_length=50, null= True, blank= True)    

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """Unicode representation of User."""
        return self.full_name

    
class Quiz(models.Model):
    """This is the table for quizes. Each quiz needs to be created and then taken."""
    
    title = models.CharField(max_length=50, unique= True)

    class Meta:
        """Meta definition for Quiz."""
        verbose_name_plural = 'quizes'

    @property
    def questions_count(self):
        return SessionQuestion.objects.filter(quiz= self.id).count()

    def __str__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Question(models.Model):
    '''Each question belongs to a subject but may present in mutilple quiz session '''
    
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)

    text = models.CharField(max_length=1000)
    op1 = models.CharField(max_length=500)
    op2 = models.CharField(max_length=500)
    op3 = models.CharField(max_length=500)
    op4 = models.CharField(max_length=500)
    test_answer = models.PositiveSmallIntegerField()
    
    @property
    def title(self):
        return f'{self.text} - {self.subject}'
    
    def __str__(self):
        return self.title
# ------------------------------------------------------------------------------
# Middle Tables for models
class Session(models.Model):
    '''This table could be interpreted as the "session" that the quiz has been taken.'''
    
    user = models.ManyToManyField(User)
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)


    date_taken = models.DateTimeField()
    @property
    def title(self):
        return f'Session - {self.id}'
    
    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     # if the item is being created 
    #     if not self.id:
    #         self.date_taken = timezone.now()
        
    #     # self.modified = timezone.now()
    #     return super(User, self).save(*args, **kwargs)
    
    
    
class SessionAnswer(models.Model):
    '''This table stores the answers that has been recorded in a specific session.'''

    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    session = models.ForeignKey(Session, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)

    submitted_test_answer = models.PositiveSmallIntegerField()
    date_answered = models.DateTimeField()
    correct_answer = models.BooleanField(default= False)
    
    # @property
    # def correct_answer(self):
    #     try:
    #         return self.test_answer == self.question__test_answer
    #     except Exception as e:
    #         print(e)
    #         return 'null'

    def save(self, *args, **kwargs):
        # if the user submitted the correct answer, when saving the object make the modifications.
        if self.submitted_test_answer == self.question.test_answer:
            self.correct_answer = True
        else:
            self.correct_answer = False
        return super(SessionAnswer, self).save(*args, **kwargs)
            

    @property
    def title(self):
        return f'Answer - {self.id}'



class SessionQuestion(models.Model):
    '''This table stores the data for the questions that has been selected for the session.'''
    
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)

    