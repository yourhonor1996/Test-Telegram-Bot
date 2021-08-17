import random
from django.core.checks.messages import Error
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# TODO create an Answer model for saving the answers.
# TODO limit the test answer to 1 to 4 
# TODO create forms for validating data 
# FIXME cerate limitation for education
# TODO delete the "quiz" table and replace it with session
# TODO make it so that if we have a null answer to a question we would have another state for the correctanswer
# -------------------------------------------------
# Managers
class QuestionManager(models.Manager):
    def select_random(self, n, subjec_id):
        """Selects n records from the model and returns a queryset

        Args:
            n (int): number of recorsd to return
        """
        # TODO this algorithm may have some room for improvements. see this link: https://stackoverflow.com/questions/1731346/how-to-get-two-random-records-with-django/6405601#6405601
        questions = self.filter(subject= subjec_id)
        ids = list(questions.values_list('id', flat=True))
        rand_ids = random.sample(ids, n)
        return questions.filter(id__in= rand_ids)


# -------------------------------------------------
# Models
class User(AbstractUser):
    
    chat_id = models.BigIntegerField(null= True)
    user_id = models.BigIntegerField(unique= True, null= True)
    first_name = models.CharField(max_length=50, null= True, blank= True)
    last_name = models.CharField(max_length=50, null= True, blank= True)    
    phone_number = models.CharField(max_length= 13, null= True)
    education = models.CharField(max_length= 50, null= True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """Unicode representation of User."""
        return self.full_name

    
class Quiz(models.Model):
    """This is the table for quizes. Each quiz needs to be created and then taken."""
    
    title = models.CharField(max_length=50)

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
    
    objects = QuestionManager()
    
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
    
    users_to_start = models.IntegerField(default= 2, null= True)
    date_created = models.DateTimeField()
    date_taken = models.DateTimeField(null= True)
    
    @property
    def title(self):
        return f'Session - {self.id}'
    
    def __str__(self):
        return self.title
    
    @property
    def session_report(self):
        session_users = self.user.all()
        results = []
        for user in session_users:
            user_result  = {'session_answers':[]}
            user_serssion_answers = SessionAnswer.objects.filter(session= self, user= user)
            # count the correct and wrong answers and put them in the user_result dictionary
            n_correct_answers = user_serssion_answers.filter(correct_answer = True).count()
            n_wrong_answers = user_serssion_answers.filter(correct_answer = False).count()
            user_result.update({
                'user_id': user.user_id,
                'full_name': user.full_name,
                'correct_answers': n_correct_answers,
                'wrong_answers': n_wrong_answers
            })
            for session_answer in user_serssion_answers:
                user_result['session_answers'].append({
                    'id': session_answer.id, 
                    'text': session_answer.question.text,
                    'correct_answer': session_answer.question.test_answer,
                    'submitted_answer': session_answer.submitted_test_answer,
                    'was_correct': session_answer.correct_answer
                    }
                )
            results.append(user_result)
        return results


class SessionAnswer(models.Model):
    '''This table stores the answers that has been recorded in a specific session.'''

    session = models.ForeignKey(Session, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    submitted_test_answer = models.PositiveSmallIntegerField()
    date_answered = models.DateTimeField(null= True)
    correct_answer = models.BooleanField(default= False)
    
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
    session = models.ForeignKey(Session, on_delete= models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    date_created = models.DateTimeField()

    