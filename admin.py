from django.contrib.admin import ModelAdmin

from project.admin import project_admin_site

from .models import (
    Board,
    Issue,
    Label,
)


class BoardAdmin(ModelAdmin):
    list_display = ("id", "name")


class IssueAdmin(ModelAdmin):
    list_display = ("id", "name", "assignee", "private", "expiration_date")


class LabelAdmin(ModelAdmin):
    list_display = ("id", "name")


project_admin_site.register(Board, BoardAdmin)
project_admin_site.register(Issue, IssueAdmin)
project_admin_site.register(Label, LabelAdmin)
