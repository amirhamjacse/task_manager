# views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.db.models import Q
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



class TaskUpdateView(LoginRequiredMixin, View):
    template_name = 'task/create.html'

    def get(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, pk=task_id)
        
        photo_obj = Photos.objects.filter(task=task).first()
        task_form = TaskForm(instance=task)
        
        if photo_obj:
            photo_form = PhotoForm(instance=photo_obj)
        else:
            photo_form = PhotoForm()
        
        context = {
            'form': task_form,
            'photo_form': photo_form,
            'task_id': task_id,
        }
        return render(request, self.template_name, context)


    def post(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, pk=task_id)
        photo_obj = Photos.objects.filter(task=task).first()
        task_form = TaskForm(request.POST, instance=task)
        photo_form = PhotoForm(
            request.POST, request.FILES, instance=photo_obj
        )
        if task_form.is_valid() and photo_form.is_valid():
            task = task_form.save(commit=False)
            task.owner = request.user
            task.save()

            photo = photo_form.save(commit=False)
            photo.task = task
            photo.save()

            return redirect('home')
        context = {
            'form': task_form,
            'photo_form': photo_form,
            'task_id': task_id,
        }
        return render(request, self.template_name, context)


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
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


class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    # context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            title = form.cleaned_data.get(
                'title'
            )
            created_at_start = form.cleaned_data.get(
                'created_at_start'
            )
            created_at_end = form.cleaned_data.get(
                'created_at_end'
            )
            due_date_start = form.cleaned_data.get(
                'due_date_start'
            )
            due_date_end = form.cleaned_data.get(
                'due_date_end'
            )
            priority = form.cleaned_data.get(
                'priority'
            )
            is_complete = form.cleaned_data.get(
                'is_complete'
            )

            # Create an initial Q object to start the query
            query = Q()

            if title:
                # Perform case-insensitive search on title
                query &= Q(title__icontains=title)

            if created_at_start:
                query &= Q(created_at__gte=created_at_start)

            if created_at_end:
                query &= Q(created_at__lte=created_at_end)

            if due_date_start:
                query &= Q(due_date__gte=due_date_start)

            if due_date_end:
                query &= Q(due_date__lte=due_date_end)

            if priority:
                query &= Q(priority=priority)

            if is_complete is not None:
                query &= Q(is_complete=is_complete)

            # Apply the final query to the queryset
            queryset = queryset.filter(query)

        order_by = self.request.GET.get('order_by', '-created_at')
        queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context
