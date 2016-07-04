from django.conf.urls import url
from django.contrib import admin
from task.views import home, logout_view , TaskUpdate, TaskDelete, TaskCreate, TaskListView
from task import views
from task.models import task

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),
    url(r'^home/', home),
    url(r'^logout/', logout_view),
    url(r'^task_list/(?P<filter_param>\w+)/$', TaskListView.as_view(model = task), name='task_list'),
    url(r'^add_task/$', TaskCreate.as_view(model=task,success_url='/task_list/all' ), name='add_task'),
    url(r'^delete_task/(?P<pk>\d+)/$', TaskDelete.as_view(model=task,success_url='/task_list/all' ), name='delete_task'),
    url(r'^edit_task/(?P<pk>\d+)/$', TaskUpdate.as_view(model=task,success_url='/task_list/all' ), name='edit_task'),
    url(r'^update_status/(?P<status>\w+)/(?P<pk>\d+)/$', views.update_status, name ='update_status'),


]
