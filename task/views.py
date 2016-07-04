from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from task.models import task
from task.forms import TaskForm





def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/task_list/all',)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/task_list/all')
            else:
                  return render(request,'home.html', {'message':'Your account is disabled'})
        else:
            return render(request,'home.html', {'message':"Invalid login details supplied."} )
    else:
        return render(request,'home.html')


class TaskListView(LoginRequiredMixin,ListView):
    login_url = '/home/'
    redirect_field_name = 'redirect_to'
    model = task
    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        if self.kwargs['filter_param']=='uncompleted':
            context['tasks'] = task.objects.filter(author = self.request.user,task_is_done = False)
        else:
            context['tasks'] = task.objects.filter(author = self.request.user)
        return context


def update_status(request,status, pk):
    task_done = task.objects.filter( pk = pk)
    task_done = task_done[0]
    if not task_done.author == request.user:
        raise Http404

    task_done.task_is_done = False if status == 'False' else True
    task_done.save()
    return HttpResponseRedirect('/task_list/all')



class TaskDelete(LoginRequiredMixin,DeleteView):
    login_url = '/home/'
    redirect_field_name = 'redirect_to'
    success_message = "Thing was deleted successfully."
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TaskDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(TaskDelete, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


class TaskUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/home/'
    redirect_field_name = 'redirect_to'
    fields = ['task_name', 'task_description']
    def get_object(self, queryset=None):
        obj = task.objects.get(id=self.kwargs['pk'])
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get(self, request, **kwargs):
        self.object = task.objects.get(id=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class TaskCreate(LoginRequiredMixin,CreateView):
    login_url = '/home/'
    redirect_field_name = 'redirect_to'
    model = task
    form_class = TaskForm
    def get_initial(self):
        return {
            'author':self.request.user.id,
        }




