# Minimal example: `sync_to_async` threading bug (?)

This is a minimal Django application generated with `django-admin startproject`
where only one view with an async method was added in `urls.py`.

Django's
[`sync_to_async`](https://docs.djangoproject.com/en/4.1/topics/async/#sync-to-async)
docs claim that it should schedule the given function to run in a single,
shared thread no matter what, which can either be the main thread or another
one (but in any case it's one and the same for different invocations):

>Thread-sensitive mode is quite special, and does a lot of work to run all
>functions in the same thread. Note, though, that it relies on usage of
>`async_to_sync()` above it in the stack to correctly run things on the main
>thread. If you use asyncio.run() or similar, it will fall back to running
>thread-sensitive functions in a single, shared thread, but this will not be
>the main thread.

However, as this repository shows, in a really trivial case, invocations via
`sync_to_async(..., thread_sensitive=True)` are scheduled in separate threads.

## Steps to reproduce

1. Serve app using `uvicorn --reload foo.asgi:application`
2. Make a request to `http://127.0.0.1:8000/myview/`.
3. Make another one to the same URL within 10 seconds.
4. In the server logs, notice that the thread ID is different for each
   invocation of `sync_to_async(f(), thread_sensitive=True)()`.
