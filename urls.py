from django.urls import path

from dashboard.views import issue, board, rest


app_name = "dashboard"

urlpatterns = [
    # board
    path('create_board', board.BoardCreateView.as_view(), name='create_board'),
    path('update_board/<int:pk>', board.BoardUpdateView.as_view(), name='update_board'),
    path("boards", board.BoardListView.as_view(), name="list_boards"),
    # issue
    path('create_issue', issue.IssueCreateView.as_view(), name='create_issue'),
    path('update_issue/<int:pk>', issue.IssueUpdateView.as_view(), name='update_issue'),
    path('detail_issue/<int:pk>', issue.IssueDetailView.as_view(), name='detail_issue'),
    path('issues', issue.IssueListView.as_view(), name='list_issues'),
    path('issues/<int:user_id>', issue.IssueListView.as_view(), name='list_issues'),
    # rest
    path("update_issue_order", rest.UpdateIssueOrderView().as_view(), name="update_issue_order"),
    path("load_issues", rest.IssuesList.as_view(), name="load_issues"),
]
