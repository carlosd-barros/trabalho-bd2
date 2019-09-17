from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import (
    ModelChoiceField,
    ModelChoiceIterator,
    ModelMultipleChoiceField
)


class InsertForm(forms.Form):
    nome = forms.CharField(
        label='Nome',
        max_length=100,
        required=True
    )
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True
    )
    cidade = forms.CharField(
        label='Cidade',
        max_length=50,
        required=True
    )

class DeleteForm(forms.Form):
    pass

class ReadForm(forms.Form):
    cod = forms.IntegerField(
        label='Código',
        required=False
    )
    nome = forms.CharField(
        label='Nome',
        required=False
    )

    """def clean(self):
        cleaned_data = super().clean()
        cod = cleaned_data.get('cod')
        nome = cleaned_data.get('nome')

        if not cod and not nome:
            raise forms.ValidationError(
                "Preencha pelo menos um campo."
            )"""

class FaturamentoForm(forms.Form):
    pass