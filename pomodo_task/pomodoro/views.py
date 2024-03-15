# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services import PomodoroService
from tasks.services import TaskService

def pomodoro_timer(request):
    # Retrieve completed and ongoing Pomodoros from the service
    completed_pomodoros = PomodoroService.get_completed_pomodoros(request.user)
    ongoing_pomodoro = PomodoroService.get_ongoing_pomodoro()

    # Get all tasks for the task selection dropdown
    tasks = TaskService.get_all_tasks()

    context = {
        'completed_pomodoros': completed_pomodoros,
        'ongoing_pomodoro': ongoing_pomodoro,
        'tasks': tasks,
    }

    return render(request, 'pomodoro/pomodoro_timer.html', context)

def start_pomodoro(request):
    if request.method == 'POST':
        task_id = request.POST.get('task')
        task = TaskService.get_task_by_id(task_id)
        PomodoroService.start_pomodoro(task, request.user)
        return redirect('pomodoro-timer')  # Redirect back to the Pomodoro timer page

def stop_pomodoro(request):
    if request.method == 'POST':
        ongoing_pomodoro = PomodoroService.get_ongoing_pomodoro()
        PomodoroService.stop_pomodoro(ongoing_pomodoro)
        return JsonResponse({'success': True})  # Respond with success JSON
