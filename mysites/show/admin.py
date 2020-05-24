from django.contrib import admin
from .models import user,DoubanSubject,DoubanTask

# Register your models here.
admin.site.register(user)
admin.site.register(DoubanSubject)
admin.site.register(DoubanTask)