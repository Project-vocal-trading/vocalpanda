from django.shortcuts import redirect

def check_session(func):
    def wrapped_view(request, *args, **kwargs):
        if 'session_key' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapped_view
