# events/forms.py (новый файл)
from django import forms
from .models import Quest

class UserQuestForm(forms.ModelForm):
    """
    Форма для создания пользовательского квеста.
    """
    class Meta:
        model = Quest
        fields = ['title', 'description', 'required_level', 'reward_experience', 'reward_gold']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'required_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reward_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'reward_gold': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        help_texts = {
            'title': 'Краткое и понятное название квеста.',
            'description': 'Подробное описание задания для героя.',
            'required_level': 'Минимальный уровень героя для получения квеста.',
            'reward_experience': 'Количество опыта, которое получит герой за выполнение.',
            'reward_gold': 'Количество золота, которое получит герой за выполнение.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значения по умолчанию для новых квестов
        if not self.instance.pk: # Если это новый объект
            self.fields['quest_type'].initial = 'user_generated'
            self.fields['is_approved'].initial = False
            # Эти поля не должны быть редактируемыми пользователем напрямую
            self.fields['quest_type'].widget = forms.HiddenInput()
            self.fields['is_approved'].widget = forms.HiddenInput()
            # self.fields['creator'].widget = forms.HiddenInput() # Будет установлено во view
