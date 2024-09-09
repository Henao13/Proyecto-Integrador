from django.shortcuts import redirect

def usuario_login_requerido(func):
    def wrap(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrap
