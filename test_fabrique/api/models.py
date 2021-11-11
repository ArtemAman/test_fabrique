from django.db import models


class Poll(models.Model):
    """
    Модель опроса
    """
    name = models.CharField(max_length=144)
    description = models.CharField(max_length=500)
    start_day = models.DateField()
    finish_day = models.DateField()


class Question(models.Model):
    """
    Модель вопроса
    """

    TYPES = [
        ('TEXT', 'text'),
        ('CHOICE', 'choice'),
        ('MULTIPLE_CHOICE', 'multiple_choice')]

    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=TYPES)
    text = models.CharField(max_length=500)


class Option(models.Model):
    """
    Модель вариантов ответа для вопросов с выбором
    """
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    index = models.PositiveIntegerField(unique=True)
    text = models.CharField(max_length=100)


class PollWithInfo(models.Model):
    """
    Модель для записи заполненного опроса
    """
    user_id = models.PositiveIntegerField(unique=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    fulfillment_time = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    """
    Модель для записи ответа на опрос
    """
    poll_with_info = models.ForeignKey('PollWithInfo', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
