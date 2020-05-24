# coding=utf-8
from mysites.celery import app
from . import movie
from .models import user,DoubanTask

# celery_app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')
# this is celery settings

# this is a function about need many time
@app.task
def movietop250(taskid):
    movie.doubanTopMovie(taskid)
    print("已完成")
    DoubanTask.objects.filter(id=taskid).update(status="已完成")

@app.task
def searchNewMovie(taskid):
    movie.searchNewMovie(taskid)
    DoubanTask.objects.filter(id=taskid).update(status="已完成")
    print("已完成")

@app.task
def searchHotMovie(taskid):
    movie.searchNewMovie(taskid)
    DoubanTask.objects.filter(id=taskid).update(status="已完成")
    print("已完成")

@app.task
def searchMoviewithkey(taskid,key,pagenum):
    movie.searchMoviewithkey(taskid,key,pagenum)
    DoubanTask.objects.filter(id=taskid).update(status="已完成")
    print("已完成")