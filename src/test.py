# import os
from src.utility.util import config_django
config_django()

from src import models

print(models.Question.objects.select_random(5))


# import random

# print(random.sample([1,3,4,5,7,8,6,5,4,3], 2))