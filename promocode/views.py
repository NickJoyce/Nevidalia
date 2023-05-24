from django.shortcuts import render, redirect

# Create your views here.
from .tasks import test_task

def celery_task_inside(request):
    test_task.delay()
    return redirect('index')