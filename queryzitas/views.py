import pyodbc
from django.db import connection
from django.shortcuts import render
from db2.settings import DATABASES

from django.http import HttpResponse
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


class DeleteFormView(SuccessMessageMixin, FormView):
    form_class = DeleteForm
    template_name = 'Delete.html'
    success_url = 'queryzitas:delete'
    success_message = 'Cliente deletado com sucesso.'

    def form_valid(self, form):
        dados = form.clean() 
        if self.request.method == "POST":
            if form.is_valid():
                with connection.cursor() as cursor:
                    cursor.execute(f"exec deletarDados {dados['id']}")
            else:
                form = DeleteForm()

        return super(
            DeleteFormView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self):
        return reverse(self.success_url)



class ReadFormView(SuccessMessageMixin, FormView):
    resultados = None
    form_class = ReadForm
    template_name = 'Read.html'

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("selecionarDados")
        lista = []
        for row in cursor:
            lista.append(row)
        print(f'lista: {lista}')

        return render(request, 'Read.html',{'selected':lista})

    success_url = reverse_lazy('queryzitas:read')

class FaturamentoFormView(SuccessMessageMixin, FormView):
    resultados = []
    form_class = FaturamentoForm
    template_name = 'Faturamento.html'
    success_url = 'queryzitas:faturamento'
    success_message = 'Consulta concluida com sucesso.'

    def form_valid(self, form):
        dados = form.clean()
        if self.request.method == "POST":
            if form.is_valid():
                cursor = connection.cursor()
                cursor.execute(f"""
                    select * from [dbo].faturamento({dados['id']});
                """)
                for row in cursor:
                    self.resultados.append(row)
                print(f'resultados: {self.resultados}')
            else:
                form = InsertForm()

        return super(
            FaturamentoFormView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'resultados': self.resultados
        })
        return super(
            FaturamentoFormView, self).get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self):
        return reverse(self.success_url)
    