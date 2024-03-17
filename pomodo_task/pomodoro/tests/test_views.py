from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from pomodoro.models import PomodoroSession
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class PomodoroSessionViewSetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="test@localhost", password='testpass')
        self.client.login(email="test@localhost", password='testpass')
        self.task = Task.objects.create(name='Test Task', owner=self.user)

    def test_create_pomodoro_session(self):
        url = reverse('pomodorosession-list')
        data = {
            'task': self.task.id,
            'is_break': False,
            'duration': timezone.timedelta(minutes=25).total_seconds(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PomodoroSession.objects.count(), 1)

    def test_pause_pomodoro_session(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        url = reverse('pomodorosession-detail', args=[pomodoro_session.id])
        data = {'action': 'pause'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        pomodoro_session.refresh_from_db()
        self.assertTrue(pomodoro_session.is_paused)

    def test_resume_pomodoro_session(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
            is_paused=True,
            pause_time=timezone.now(),
        )
        url = reverse('pomodorosession-detail', args=[pomodoro_session.id])
        data = {'action': 'resume'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        pomodoro_session.refresh_from_db()
        self.assertFalse(pomodoro_session.is_paused)
        self.assertIsNone(pomodoro_session.pause_time)

    def test_stop_pomodoro_session(self):
        pomodoro_session = PomodoroSession.objects.create(
            start_time=timezone.now(),
            task=self.task,
            owner=self.user,
        )
        url = reverse('pomodorosession-detail', args=[pomodoro_session.id])
        data = {'action': 'stop'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        pomodoro_session.refresh_from_db()
        self.assertTrue(pomodoro_session.is_completed)
        self.assertIsNotNone(pomodoro_session.end_time)
        self.assertGreater(pomodoro_session.duration, timezone.timedelta(seconds=0))
