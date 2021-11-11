from rest_framework import serializers
from api.models import Poll, Question, Option, PollWithInfo


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'start_day', 'finish_day']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'poll', 'type', 'text']


class OptionSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'index', 'text']


class PollWithInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollWithInfo
        fields = ['userId', 'poll', 'fulfillment_time']
