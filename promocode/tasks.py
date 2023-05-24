from project.celery import app
import time

@app.task
def test_task():
    time.sleep(2)