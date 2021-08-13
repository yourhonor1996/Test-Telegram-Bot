from django.db import models
from django.utils import timezone

# create your models here
class User(models.Model):
    """Model definition for User."""
    chat_id = models.BigIntegerField(unique= True)
    first_name = models.CharField(max_length=50, null= True, blank= True)
    last_name = models.CharField(max_length=50, null= True, blank= True)    


    # def __str__(self):
    #     """Unicode representation of User."""
    #     pass

    
class Quiz(models.Model):
    """Model definition for Quiz."""
    title = models.CharField(max_length=50, unique= True)


    class Meta:
        """Meta definition for Quiz."""
        verbose_name_plural = 'quizes'

    # def __str__(self):
    #     return self.title


class Subject(models.Model):
    name = models.CharField(max_length=50)


class Question(models.Model):
    subjet = models.ForeignKey(Subject, on_delete= models.CASCADE)

    text = models.CharField(max_length=1000)
    op1 = models.CharField(max_length=500)
    op2 = models.CharField(max_length=500)
    op3 = models.CharField(max_length=500)
    op4 = models.CharField(max_length=500)
    test_answer = models.PositiveSmallIntegerField(max_length= 1)


# ------------------------------------------------------------------------------
# Middle Tables for models
class TakeQuiz(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)

    date_taken = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # if the item is being created 
        if not self.id:
            self.date_taken = timezone.now()
        
        # self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)
    
    
class TakeAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    take_quiz = models.ForeignKey(TakeQuiz, on_delete= models.CASCADE)

    test_answer_taken = models.PositiveSmallIntegerField()
    date_answered = models.DateTimeField()
    correct_answer = models.BooleanField()
    
    
class TakeQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)

    