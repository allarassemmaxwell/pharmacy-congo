from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404



# ==================================================
#                     DECORATOR VIEWS
# ==================================================
def admin_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == 'Admin':
                pass
            else:
                return redirect('dashboard')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator







# ==================================================
#                     DECORATOR VIEWS
# ==================================================
def admin_depart_gestion_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == "Admin" or request.user.role == "Département" or request.user.role == "Gestionnaire":
                pass
            else:
                return redirect('dashboard')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator




# ==================================================
#                     DECORATOR VIEWS
# ==================================================
def admin_depart_gestion_centre_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == "Admin" or request.user.role == "Département" or request.user.role == "Gestionnaire" or request.user.role == "Centre":
                pass
            else:
                return redirect('dashboard')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator




# ==================================================
#                     DECORATOR VIEWS
# ==================================================
def centre_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == 'Centre':
                pass
            else:
                return redirect('dashboard')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator




# ==================================================
#                     DECORATOR VIEWS
# ==================================================
def admin_centre_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == 'Centre' or request.user.role == 'Admin':
                pass
            else:
                return redirect('dashboard')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
