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
        required=False
    )
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=False
    )
    cidade = forms.CharField(
        label='Cidade',
        max_length=50,
        required=False
    )

class DeleteForm(forms.Form):
        id = forms.CharField(
        label='id',
        max_length=100,
        required=False
    )

class ReadForm(forms.Form):
    pass

class FaturamentoForm(forms.Form):
    pass