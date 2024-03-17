from django.test import TestCase
from django.utils import timezone
from pomodoro.models import PomodoroSession
from pomodoro.services import PomodoroService
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class PomodoroServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@localhost", password='testpass')
        self.task = Task.objects.create(name='Test Task', owner=self.user)

    def test_start_pomodoro(self):
        pomodoro_session = PomodoroService.start_pomodoro(
            task=self.task,
            is_break=False,
            owner=self.user,
            duration=timezone.timedelta(minutes=25),
        )
        self.assertEqual(pomodoro_session.task, self.task)
        self.assertEqual(pomodoro_session.owner, self.user)
        self.assertFalse(pomodoro_session.is_break)
        self.assertEqual(pomodoro_session.duration, timezone.timedelta(minutes=25))

    def test_pause_pomodoro(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        paused_session = PomodoroService.pause_pomodoro(pomodoro_session)
        self.assertTrue(paused_session.is_paused)
        self.assertIsNotNone(paused_session.pause_time)

    def test_resume_pomodoro(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        paused_session = PomodoroService.pause_pomodoro(pomodoro_session)
        resumed_session = PomodoroService.resume_pomodoro(paused_session)
        self.assertFalse(resumed_session.is_paused)
        self.assertIsNone(resumed_session.pause_time)

    def test_stop_pomodoro(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        stopped_session = PomodoroService.stop_pomodoro(pomodoro_session)
        self.assertTrue(stopped_session.is_completed)
        self.assertIsNotNone(stopped_session.end_time)
        self.assertGreater(stopped_session.duration, timezone.timedelta(seconds=0))
