from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from api.services import StandardPaginator
from api.models import Poll, Question, Option, Answer, PollWithInfo
from api.serializers import PollSerializer, QuestionSerializer, PollWithInfoSerializer, OptionSerializerAdmin


class AdminPolls(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    Получение всех записей опросов + добавленеие записей

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()
    pagination_class = StandardPaginator
    serializer_class = PollSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'start_day']

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class AdminPollsUpdateDestroy(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    """
    get - получение записи по id
    delete - удаление записи
    patch - обновление полей записи

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AdminQuestions(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    Получение всех записей вопросов + добавленеие записей

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    pagination_class = StandardPaginator
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poll', 'type']

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class AdminQuestionsUpdateDestroy(GenericAPIView, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    """
    get - получение записи по id
    delete - удаление записи
    patch - обновление полей записи

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AdminOptions(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    Получение всех записей вопросов + добавленеие записей

    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    pagination_class = StandardPaginator
    serializer_class = OptionSerializerAdmin
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question']

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class UserPolls(APIView):
    """
    Получение всех возможных опросов на сегодняшний день

    """

    def get(self, request):
        today = date.today()
        polls = Poll.objects.filter(start_day=today)
        serialized_data = PollSerializer(polls, many=True).data
        return Response(serialized_data)


class UserPollsID(APIView):
    """
    Получение опроса по ID и прохождение его

    """

    def get(self, request, id):
        poll = Poll.objects.get(id=id)
        serialized_data = PollSerializer(poll).data
        serialized_data['questions'] = []
        questions = poll.question_set.all()
        for question in questions:
            question_serialized_data = QuestionSerializer(question).data
            serialized_data['questions'].append(question_serialized_data)
        return Response(serialized_data)

    def post(self, request, id):
        """

        user_id - int
        answers - dict
        """
        poll = Poll.objects.get(id=id)
        user_id = request.data['user_id']
        answers = request.data['answers']
        answer_list = []
        for question_id in answers:
            answer = Answer(
                question=question_id,
                questionType=question_id.type,
                questionText=question_id.text)
            answer_list.append(answer)

        poll_info = PollWithInfo(user_id=user_id, poll=poll)
        poll_info.save()
        for answer in answer_list:
            answer.poll_with_info = poll_info
            answer.save()
        return Response('Done')


class UserPollsWithAnswers(APIView):
    """
    Получение всех пройденых опросв юзера

    """

    def get(self, request, user_id):
        polls = PollWithInfo.objects.filter(user_id=user_id)
        serialized_data = PollWithInfoSerializer(polls, many=True).data
        return Response(serialized_data)
