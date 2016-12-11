import django.dispatch

push_package_sent = django.dispatch.Signal(providing_args=["userinfo"])
permission_granted = django.dispatch.Signal(providing_args=["token", "userinfo", "isnew"])
permission_denied = django.dispatch.Signal(providing_args=["token", "userinfo"])
