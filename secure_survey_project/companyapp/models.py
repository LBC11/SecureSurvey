from django.db import models


class Survey(models.Model):
    email = models.EmailField(max_length=254)


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_count_1 = models.IntegerField(default=0)
    answer_count_2 = models.IntegerField(default=0)
    answer_count_3 = models.IntegerField(default=0)
    answer_count_4 = models.IntegerField(default=0)
    answer_count_5 = models.IntegerField(default=0)
