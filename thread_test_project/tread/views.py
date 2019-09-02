from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render


from .model_serializers import ThreadSerializer


class TreadCreateAPIView(APIView):
    view_request_serializer = ThreadSerializer


# class GoalCreateAPIView(APIView):
#     """ Goal Create API with custom method post. Function validate input data,
#         transforms is_urgent and is_important fields via match_state function to state value
#         and post changed data"""
#     view_request_serializer = GoalValidatorSerializer
#
#     def post(self, request):
#         serializer = self.view_request_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         request_data = serializer.data
#         request_data.update(user=request.user.pk)
#         pre_validated_data = match_state(request_data)
#         model_serializer = GoalSerializer(data=pre_validated_data)
#         model_serializer.is_valid(raise_exception=True)
#         created_goal = model_serializer.save()
#         return Response(GoalSerializer(instance=created_goal).data, status=status.HTTP_201_CREATED)
#
#     def get(self, request):
#         goals = Goal.objects.all()
#         serializer = GoalSerializer(goals, many=True)
#         return Response(serializer.data)

