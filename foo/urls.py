from django.contrib import admin
from django.urls import path
from asgiref.sync import sync_to_async
from django.views.generic.base import View
from django.http import HttpResponse
import threading
import time


def f():
    print("enter f()")
    print(f"sync_to_async()-wrapped f() in thread: {threading.get_ident()}")
    print(threading.get_ident())
    time.sleep(10)
    print("exit f()")


class MyView(View):
    async def get(self, *a, **kw):
        print(f"request handled in thread: {threading.get_ident()}")
        await sync_to_async(f, thread_sensitive=True)()
        return HttpResponse("")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("myview/", MyView.as_view()),
]
