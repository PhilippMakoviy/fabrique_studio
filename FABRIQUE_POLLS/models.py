from django.db import models
from django.core.exceptions import ValidationError


# Класс опросник
class Poll(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()


# заполненый опросник
class Finished_poll(models.Model):
    userId = models.IntegerField(db_index=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    submit_time = models.DateTimeField(auto_now_add=True)


# варинаты ответа
class Answer_option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.CharField(max_length=100)


# проверка ответов
def QuestionValidator(value):
    if value not in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


# класс ответов
class Answer(models.Model):
    finished_poll = models.ForeignKey('Finished_poll', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=30, validators=[QuestionValidator])
    question_text = models.CharField(max_length=300)
    answer_text = models.CharField(max_length=300)


# Класс вопрос
class Question(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, validators=[QuestionValidator])
    text = models.CharField(max_length=300)

    @property
    def OptionType(self):
        return self.type in OPTION_TYPES
