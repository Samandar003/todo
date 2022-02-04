from datetime import datetime
from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.views import LogoutView

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
  template_name = 'todo/login.html'

class Register(FormView):
  template_name = 'todo/register.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('tasks')
  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(Register, self).form_valid(form)

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      redirect('tasks')
    return super(Register, self).get(*args, **kwargs)

class TaskListView(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'
  template_name = 'todo/task_list.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tasks'] = context['tasks'].filter(user=self.request.user)
      context['count'] = context['tasks'].filter(complete=False).count()
      
      search_input = self.request.GET.get('search_area') or ''
      if search_input:
        context['tasks'] = context['tasks'].filter(title__contains=search_input)
      # context['tasks'] = Task.objects.filter(user=self.request.user)
      context['search_input'] = search_input
      return context 
  
      
class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Task
  context_object_name = 'task'
  template_name = 'todo/task_detail.html'
  def test_func(self):
    task = self.get_object()
    if self.request.user == task.user:
      return True
    return False
    
class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Task
  fields = ['title', 'description', 'complete']
  template_name = 'todo/task_form.html'
  def form_valid(self, form):
      form.instance.user = self.request.user
      return super(TaskUpdate, self).form_valid(form)
  def test_func(self):
    task = self.get_object()
    if self.request.user == task.user:
      return True
    return False

class TaskCreate(LoginRequiredMixin, CreateView):
  model = Task
  fields = ['title', 'description', 'complete']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(TaskCreate, self).form_valid(form)
  
  # success_url = reverse_lazy('tasks')
  template_name = 'todo/task_create.html'
  
class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Task
  template_name = 'todo/task_confirm_delete.html'
  context_object_name = 'task'
  success_url = reverse_lazy('tasks')
  def test_func(self):
    task = self.get_object()
    if self.request.user == task.user:
      return True
    return False

  