from channels.generic.websocket import WebsocketConsumer
from pomodoro.models import PomodoroSession


class PomodoroSessionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def session_completed(self, event):
        session_id = event["session_id"]
        self.send(text_data=f"Pomodoro session {session_id} completed!")
