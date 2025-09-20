from django.contrib import admin
from .models import Assignment, TestFunction

admin.site.register(Assignment)
admin.site.register(TestFunction)


def foo(a):
    return a+1