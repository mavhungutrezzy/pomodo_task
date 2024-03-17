from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from pomodoro.models import PomodoroSession
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class PomodoroSessionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@localhost", password='testpass')
        self.task = Task.objects.create(name='Test Task', owner=self.user)

    def test_pomodoro_session_creation(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        self.assertEqual(str(pomodoro_session), f"Pomodoro Session for {self.task.name}")

    def test_pomodoro_session_start(self):
        pomodoro_session = PomodoroSession.objects.create(task=self.task, owner=self.user)
        pomodoro_session.start()
        self.assertIsNotNone(pomodoro_session.start_time)

    def test_pomodoro_session_pause(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        pomodoro_session.pause()
        self.assertTrue(pomodoro_session.is_paused)
        self.assertIsNotNone(pomodoro_session.pause_time)

    def test_pomodoro_session_resume(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        pomodoro_session.pause()
        pomodoro_session.resume()
        self.assertFalse(pomodoro_session.is_paused)
        self.assertIsNone(pomodoro_session.pause_time)

    def test_pomodoro_session_stop(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        pomodoro_session.stop()
        self.assertTrue(pomodoro_session.is_completed)
        self.assertIsNotNone(pomodoro_session.end_time)
        self.assertGreater(pomodoro_session.duration, timedelta(seconds=0))

    def test_pomodoro_session_get_remaining_time(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
            duration=timedelta(minutes=25),
        )
        remaining_time = pomodoro_session.get_remaining_time()
        self.assertGreater(remaining_time, timedelta(seconds=0))
