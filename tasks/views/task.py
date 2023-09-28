# views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView,
    DetailView
)
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from tasks.models import Task
from tasks.forms import TaskForm, TaskFilterForm


# views.py
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Set the owner (logged-in user) before saving the task
        form.instance.owner = self.request.user
        return super().form_valid(form)



class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('home')

    def test_func(self):
        # Check if the current user is the owner of the task
        task = self.get_object()
        return self.request.user == task.owner

    def form_valid(self, form):
        # Set the owner (logged-in user) before saving the updated task
        form.instance.owner = self.request.user
        return super().form_valid(form)



# class TaskListView(LoginRequiredMixin, ListView):
#     model = Task
#     template_name = 'home.html'
    
#     def get_queryset(self):
#         # Filter tasks to show only those owned by the logged-in user
#         return Task.objects.filter(owner=self.request.user)

# Similar changes for TaskUpdateView and TaskDeleteView

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        # Check if the current user is the owner of the task
        task = self.get_object()
        return self.request.user == task.owner


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/details.html'  # Replace with the actual template name
    context_object_name = 'task'  # The variable name to use in the template

    def get_queryset(self):
        # Filter tasks based on the currently logged-in user
        return Task.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        # Use get_object_or_404 to get the specific task or return a 404 if not found
        queryset = queryset or self.get_queryset()
        pk = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=pk)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'home'
    paginate_by = 10

    def get_queryset(self):
        # Get all tasks
        queryset = super().get_queryset()

        # Get form data
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():  # Validate the form first
            # Access cleaned_data after validation
            title = form.cleaned_data.get('title')
            created_at_start = form.cleaned_data.get('created_at_start')
            created_at_end = form.cleaned_data.get('created_at_end')
            due_date_start = form.cleaned_data.get('due_date_start')
            due_date_end = form.cleaned_data.get('due_date_end')
            priority = form.cleaned_data.get('priority')
            is_complete = form.cleaned_data.get('is_complete')

            if title:
                queryset = queryset.filter(title__icontains=title)

            if created_at_start:
                queryset = queryset.filter(created_at__gte=created_at_start)

            if created_at_end:
                queryset = queryset.filter(created_at__lte=created_at_end)

            if due_date_start:
                queryset = queryset.filter(due_date__gte=due_date_start)

            if due_date_end:
                queryset = queryset.filter(due_date__lte=due_date_end)

            if priority:
                queryset = queryset.filter(priority=priority)

            if is_complete is not None:
                queryset = queryset.filter(is_complete=is_complete)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context
