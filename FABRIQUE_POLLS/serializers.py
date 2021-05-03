
from rest_framework import serializers
from rest_framework.serializers import ValidationError

#Ниже представлены сериалайзеры, который используются приложением


# вариации ответа
class OptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    index = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=200)


# вариации ответа пользователя
class UOptionSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    text = serializers.CharField(max_length=200)


# заполненый опрос
class Finished_poll_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    submit_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')



def QuestionValidator(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


#вопросник
class QuestionSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    type = serializers.CharField(max_length=50, validators=[QuestionValidator])
    text = serializers.CharField(max_length=500)



# непосредственно опросник
class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
