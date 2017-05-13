"""dressedup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from dresscodeapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^home/$', views.index),
    url(r'^filterquestions/$', views.filter_questions_page, name='filter_questions_page'),
    url(r'^filteredresults/$', views.return_filtered_results, name='return_filtered_results'),
    url(r'^question/(?P<q_pk>\d+)/$', views.question_page, name='question_page'),
    url(r'^post-answer/$', views.post_answer, name='post_answer'),
    url(r'^post-question/$', views.post_question, name='post_question'),
    url(r'^question/post/$', views.post_question_page, name='post_question_page'),
    url(r'^questionsfeed/$', views.get_questions_feed, name='get_questions_feed'),
    url(r'^myresults/$', views.get_results, name='get_results'),
    url(r'^view-result/$', views.view_result, name='view_result'),
    url(r'^view-result-filter/(?P<q_pk>\d+)/(?P<gender>[f|m|u])/(?P<minage>\d+)/(?P<maxage>\d+)/$', views.view_question_with_filters, name='view_question_with_filters'),
    url(r'^question-result/(?P<q_pk>\d+)/$', views.view_question, name='view_question'),
    url(r'^login-user/$', views.login_user, name='login_user'),
    url(r'^signup-user/$', views.signup_user, name='signup_user'),
    url(r'^logout-user/$', views.logout_user, name='logout_user'),
    url(r'^userprofile/$', views.get_profile, name='get_profile')
    # url(r'^ask/$', views.post_question, name='post_question'),

]
