from django import forms

from dashboard.models import Board, Issue


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['number'].required = True


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue

        fields = ['id', 'name', 'description', 'private',
                  'assignee', 'board', 'order', 'labels',
                  'expiration_date', 'number', 'assigner']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['board'].required = True
        self.fields['number'].required = True

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['private'] and not cleaned_data['assignee']:
            raise forms.ValidationError(u'Чтобы сделать задачу приватной, укажите исполнителя')
        if not self.instance and cleaned_data['assignee']:
            cleaned_data['assigner'] = self.user
        if self.instance:
            if not self.instance.assignee and cleaned_data['assignee']:
                cleaned_data['assigner'] = self.user
            elif self.instance.assignee and cleaned_data['assignee']:
                if self.instance.assignee != cleaned_data['assignee']:
                    cleaned_data['assigner'] = self.user
                else:
                    cleaned_data['assigner'] = self.instance.assigner

        return cleaned_data
