from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy

from dashboard.forms import IssueForm
from dashboard.models import Issue
from project.lib.views.views import CreateView, UpdateView, DetailView, ListView
from user.models import User


class IssueCreateView(CreateView):
    permission_required = "issue.add_issue"
    template_name = 'edit_issue.html'
    model = Issue
    form_class = IssueForm
    success_url = reverse_lazy('dashboard:list_boards')
    title = 'Новая задача'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = self._get_number()
        context['breadcrumbs'] = self._get_breadcrumbs()
        return context

    def _get_number(self):
        try:
            last_issue = self.model.objects.latest('number')
            last_issue_number = last_issue.number
        except self.model.DoesNotExist:
            last_issue_number = 0
        return last_issue_number + 1

    def _get_breadcrumbs(self):
        return (
            ("Главная", reverse_lazy("index")),
            ("Доски", reverse_lazy("dashboard:list_boards")),
            (self.title, "")
        )


class IssueUpdateView(UpdateView):
    permission_required = "issue.edit_issue"
    template_name = 'edit_issue.html'
    model = Issue
    form_class = IssueForm
    success_url = reverse_lazy('dashboard:list_boards')
    title = 'Редактирование задачи'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        permitted_users = [self.object.assignee, self.object.assigner]
        if any(permitted_users) and self.request.user not in permitted_users:
            messages.add_message(request, messages.INFO, 'Вы не можете редактировать эту задачу')
            return redirect(reverse_lazy('dashboard:detail_issue', kwargs=self.kwargs))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        permitted_users = [self.object.assignee, self.object.assigner]
        if any(permitted_users) and self.request.user not in permitted_users:
            messages.add_message(request, messages.INFO, 'Вы не можете редактировать эту задачу')
            return redirect(reverse_lazy('dashboard:detail_issue', kwargs=self.kwargs))
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        return (
            ("Главная", reverse_lazy("index")),
            ("Доски", reverse_lazy("dashboard:list_boards")),
            (self.title, "")
        )


class IssueDetailView(DetailView):
    permission_required = "issue.view_issue"
    template_name = 'issue.html'
    model = Issue
    context_object_name = 'issue'
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.title = context['issue'].name
        context['breadcrumbs'] = self._get_breadcrumbs()
        return context

    def _get_breadcrumbs(self):
        return (
            ("Главная", reverse_lazy("index")),
            ("Доски", reverse_lazy("dashboard:list_boards")),
            (self.title, "")
        )


class IssueListView(ListView):
    permission_required = "issue.view_issue"
    template_name = 'issues.html'
    model = Issue
    context_object_name = 'issues'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self._get_breadcrumbs()
        return context

    def get_queryset(self):
        user = self.request.user
        user_id = self.kwargs.get('user_id')
        qs = self.model.objects.filter(active=True).select_related('assignee').prefetch_related('labels')

        if user_id:
            qs = qs.filter(assignee=user_id)

        if not user.is_superuser:
            users_ids = User.objects.exclude(id=user.id).values_list('id', flat=True)
            qs = qs.exclude(Q(private=True) & (Q(assignee__in=users_ids) & Q(assigner__in=users_ids)))

        return qs

    def _get_breadcrumbs(self):
        if self.request.user.id == self.kwargs.get('user_id'):
            breadcrumbs = (
                ("Главная", reverse_lazy("index")),
                ("Задачи", reverse_lazy("dashboard:list_issues")),
                ("Мои задачи", "")
            )
        else:
            breadcrumbs = (
                ("Главная", reverse_lazy("index")),
                ("Задачи", "")
            )
        return breadcrumbs
