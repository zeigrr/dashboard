import json

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import Issue
from dashboard.serializers import IssueSerializer


class UpdateIssueOrderView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        params = request.POST.dict()
        board_id = params['board_id']
        issues = json.loads(params['issues'])
        for issue in issues:
            Issue.objects.filter(id=issue['issue_id']).update(number=issue['number'], board_id=board_id)

        return Response()


class IssuesList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = request.GET.dict()
        board_id, board_last_issue = data.get('board_id'), data.get('board_last_issue')
        issues_qs = []
        if board_id and board_last_issue:
            issues_qs = Issue.objects.select_related('assignee').prefetch_related('labels').filter(
                active=True,
                board=board_id,
                number__lt=board_last_issue)
        return JsonResponse({'issues': [IssueSerializer(issue).data for issue in issues_qs[:5]]})
