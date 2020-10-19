import typing

from django.db.models import Q
from django.urls import reverse_lazy

from dashboard.forms import BoardForm
from dashboard.models import Board, Issue
from project.lib.views.views import CreateView, UpdateView, ListView
from user.models import User


class BoardCreateView(CreateView):
    permission_required = "board.add_board"
    template_name = 'edit_board.html'
    model = Board
    form_class = BoardForm
    success_url = reverse_lazy('dashboard:list_boards')
    title = 'Новая доска'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = self._get_number()
        context['breadcrumbs'] = self._get_breadcrumbs()
        return context

    def _get_number(self):
        try:
            last_board = self.model.objects.latest('number')
            last_board_number = last_board.number
        except self.model.DoesNotExist:
            last_board_number = 0
        return last_board_number + 1

    def _get_breadcrumbs(self):
        return (
            ("Главная", reverse_lazy("index")),
            ("Доски", reverse_lazy("dashboard:list_boards")),
            (self.title, "")
        )


class BoardUpdateView(UpdateView):
    permission_required = "board.edit_board"
    template_name = 'edit_board.html'
    model = Board
    form_class = BoardForm
    success_url = reverse_lazy('dashboard:list_boards')
    title = 'Редактирование доски'

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


class BoardListView(ListView):
    permission_required = "board.view_board"
    template_name = 'boards.html'
    model = Board
    context_object_name = 'boards'
    title = 'Доски'
    breadcrumbs: typing.Sequence = (("Главная", reverse_lazy("index")), (title, ""))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.breadcrumbs
        return context

    def get_queryset(self):
        user = self.request.user
        boards = self.model.objects.all().values()
        for board in boards:
            issues_qs = Issue.objects.select_related('assignee').prefetch_related('labels').filter(
                active=True,
                board=board['id']
            )
            if not user.is_superuser:
                users_ids = User.objects.exclude(id=user.id).values_list('id', flat=True)
                issues_qs = issues_qs.exclude(Q(private=True) & (Q(assignee__in=users_ids) & Q(assigner__in=users_ids)))
            issues = list(issues_qs[:5])
            board['limited_issues'] = issues
            board['last_issue'] = issues[-1].number if issues else None
        return boards
