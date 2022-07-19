from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Goals
from .serializers import GoalSerializer

# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getGoals(request):
    goals = Goals.objects.all()
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getGoal(request, pk):
    goals = Goals.objects.get(id=pk)
    serializer = GoalSerializer(goals)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createGoal(request):
    data = request.data
    user = request.user
    goal = Goals.objects.create(
        title=data["title"],
        amount=data["amount"],
        saved=data["saved"],
        author=user,
    )
    serializer = GoalSerializer(goal, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteGoal(request, pk):
    goal = Goals.objects.get(id=pk)
    goal.delete()
    return Response("Goal was deleted!")


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateGoal(request, pk):
    data = request.data
    data["author"] = request.user.id
    goal = Goals.objects.get(id=pk)
    serializer = GoalSerializer(goal, data=data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
