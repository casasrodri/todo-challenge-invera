from django.test import TestCase
from .models import Task
from .serializers import TaskSerializer


class TaskModelTestCase(TestCase):
    def __create_task(
        self,
        title="Test task 1",
        description="This is the description for the test task",
    ):
        Task.objects.create(title=title, description=description)

    def test_get_one_task(self):
        self.__create_task()

        task = Task.objects.get(title="Test task 1")

        self.assertEqual(task.title, "Test task 1")
        self.assertEqual(task.description, "This is the description for the test task")
        self.assertFalse(task.complete)
        self.assertIsNotNone(task.created)

    def test_get_all_tasks(self):
        self.__create_task()
        self.__create_task("Test task 2", "This is the description for the test task 2")

        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 2)

    def test_update_task(self):
        self.__create_task()

        task = Task.objects.get(title="Test task 1")

        task.title = "Updated task"
        task.description = "This is the updated description"
        task.complete = True

        task.save()

        updated_task = Task.objects.get(title="Updated task")

        self.assertEqual(updated_task.title, "Updated task")
        self.assertEqual(updated_task.description, "This is the updated description")
        self.assertTrue(updated_task.complete)

    def test_delete_task(self):
        self.__create_task()

        task = Task.objects.get(title="Test task 1")

        task.delete()

        tasks = Task.objects.all()

        self.assertEqual(len(tasks), 0)


class TaskSerializerTestCase(TestCase):
    def test_serializer_with_data(self):
        task = Task.objects.create(title="Task 1", description="Description.")

        serializer = TaskSerializer(task)
        data = serializer.data

        self.assertEqual(data["title"], "Task 1")
        self.assertEqual(data["description"], "Description.")
        self.assertFalse(data["complete"])
        self.assertIsNotNone(data["created"])

    def test_serializer_without_data(self):
        serializer = TaskSerializer()

        self.assertEqual(
            serializer.data, {"title": "", "description": "", "complete": False}
        )

    def test_read_only_fields(self):
        serializer = TaskSerializer()

        self.assertEqual(serializer.Meta.read_only_fields, ("id", "created"))
