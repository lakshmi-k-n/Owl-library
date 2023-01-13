"""owl_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from api_v1 import urls as api_v1_urls
from . import settings
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin/', admin.site.urls),
]
# import pdb
# pdb.set_trace()
urlpatterns += [
    url(r"api/v1/", include(api_v1_urls)),
]
schema_view = get_swagger_view(title='OWLIB API')

urlpatterns += [
    url(r'^$', schema_view)
]

# if settings.DEBUG:

#     # import debug_toolbar
#     # urlpatterns += [
#     #     url(r'^__debug__/', include(debug_toolbar.urls)),
#     # ]

#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
