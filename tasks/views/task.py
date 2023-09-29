# views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView,
    DetailView, View
)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from tasks.models import Task, Photos
from tasks.forms import TaskForm, TaskFilterForm, PhotoForm


class TaskCreateView(LoginRequiredMixin, View):
    template_name = 'task/create.html'

    def get(self, request, *args, **kwargs):
        task_form = TaskForm()
        photo_form = PhotoForm()
        context = {
            'form': task_form,
            'photo_form': photo_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if task_form.is_valid() and photo_form.is_valid():
            # Save the Task
            task = task_form.save(commit=False)
            task.owner = request.user
            task.save()

            # Create the associated Photo
            photo = photo_form.save(commit=False)
            photo.task = task
            photo.save()

            return redirect('home')

        context = {
            'form': task_form,
            'photo_form': photo_form,
        }
        return render(request, self.template_name, context)



class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('home')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/details.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}
        context['photos'] = Photos.objects.filter(
            task=self.object
        )
        context.update(self.get_context_data(
            object=self.object)
        )
        return self.render_to_response(context)


    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        pk = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=pk)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'home'

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
