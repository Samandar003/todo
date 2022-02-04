from django.urls import path
from .views import (
  TaskDetail,
  TaskListView,
  TaskUpdate,
  TaskCreate,
  TaskDelete,
  CustomLoginView,
  Register,
  LogoutView
)

urlpatterns = [
  path('', TaskListView.as_view(), name='tasks'),
  path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
  path('task/<int:pk>/update', TaskUpdate.as_view(), name='task-update'),
  path('task/new', TaskCreate.as_view(), name='task-create'),
  path('task/<int:pk>/delete', TaskDelete.as_view(), name='task-delete'),
  path('login/', CustomLoginView.as_view(), name='login'),
  path('register/', Register.as_view(), name='register'),
  path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 

]

