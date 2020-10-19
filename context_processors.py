import datetime

from dashboard.models import Issue
from dashboard.serializers import IssueSerializer


def user_deadline_issues(request):
    context = {}
    if request.user.is_authenticated:
        issues_qs = Issue.objects.filter(
            assignee=request.user.id,
            active=True,
            expiration_date__isnull=False
        )
        issues = [IssueSerializer(issue).data for issue in issues_qs]
        for issue in issues:
            issue['deadline'] = datetime.datetime.strptime(
                issue['expiration_date'],
                '%d.%m.%Y'
            ).date() - datetime.datetime.now().date()
        sorted_issues = sorted(issues, key=lambda i: i['deadline'])
        context['deadline_issues'] = sorted_issues[:3]
    return context
