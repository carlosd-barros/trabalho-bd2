import pyodbc
from django.db import connection
from db2.settings import DATABASES

from django.urls import reverse
from django.urls.base import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import (
    InsertForm,
    DeleteForm,
    ReadForm,
    FaturamentoForm
)


class HomePageView(TemplateView):
    template_name = 'index.html'

class InsertFormView(SuccessMessageMixin, FormView):
    form_class = InsertForm
    template_name = 'Insert.html'
    success_url = 'queryzitas:insert'
    success_message = 'Dados inseridos com sucesso.'
    
    def form_valid(self, form):
        dados = form.clean()
        if self.request.method == "POST":
            if form.is_valid():
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        exec [dbo].[insert_cli] '{dados['nome']}', '{dados['cpf']}', '{dados['cidade']}';
                    """)
            else:
                form = InsertForm()

        return super(
            InsertFormView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self):
        return reverse(self.success_url)


class DeleteFormView(FormView):
    form_class = DeleteForm
    template_name = 'Delete.html'
    success_url = 'queryzitas:delete'


class ReadFormView(SuccessMessageMixin, FormView):
    resultados = None
    form_class = ReadForm
    template_name = 'Read.html'
    success_url = 'queryzitas:read'
    success_message = 'Consulta realizada com sucesso.'

    def form_valid(self, form):
        dados = form.clean()
        print(f"""
            cod: {dados['cod']}, {type(dados['cod'])}
            nome: {dados['nome']}, {type(dados['nome'])}
        """)
        if self.request.method == "POST":
            if form.is_valid():
                with connection.cursor() as cursor:
                    if dados['cod']:
                        cursor.execute(f"""
                            exec [dbo].[read_cli] {dados['cod']};
                        """)
                        self.resultados = cursor.fetchall()
                        print(f"""
                            cursor: {cursor.fetchall()}
                        """)
                    else:
                        cursor.execute(f"""
                            select * from Cliente;
                        """)
                        print(f"""
                            cursor: {cursor.fetchall()}
                        """)
                    self.resultados = cursor.fetchall()
            else:
                form = InsertForm()

        return super(
            ReadFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        print('entrou no get context', self.resultados)
        kwargs.update({
            'resultados': self.resultados
        })

        return super(
            ReadFormView, self).get_context_data(**kwargs)


    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self):
        return reverse(self.success_url)

class FaturamentoFormView(FormView):
    form_class = FaturamentoForm
    template_name = 'Faturamento.html'
    success_url = 'queryzitas:faturamneto'
    