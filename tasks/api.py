from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from app.utils import get_date

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_task(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.complete = True
        task.save()
        return Response({"status": "ok", "message": "Task mark as completed."})

    # TODO http://127.0.0.1:8000/api/tasks/?created_from=2024-12-02&created_to=2024-12-08&description=rodri%20casas
    def get_queryset(self):
        params = self.request.query_params
        created_from = params.get("created_from", None)
        created_to = params.get("created_to", None)
        description = params.get("description", None)

        # Initial queryset
        queryset = Task.objects.all()

        if created_from:
            queryset = queryset.filter(created__gte=get_date(created_from))

        if created_to:
            print(created_to)
            queryset = queryset.filter(created__lte=get_date(created_to))

        if description:
            queryset = queryset.filter(description__icontains=description)

        return queryset