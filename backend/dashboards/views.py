import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from dashboards.forms import DataSourceForm, DataChartForm
from dashboards.models import DataSource, ChartData, Dashboard, FAQ
from dashboards.utils import handle_uploaded_file


class DashboardMVPView(ListView):
    template_name = 'dashboards/dashboard-mvp.html'

    def get(self, request, *args, **kwargs):
        chart_data = ChartData.objects.get(id=1)
        df, filters, total = chart_data.df_filters(10)
        # product_data = ChartData.objects.get(id=)

        context = {
            # 'table_products': table_products,
            'table_clients_header': df.columns[:-2],
            'table_clients_total': total,
            'table_clients': df.iterrows(),
        }
        return render(self.request, self.template_name, context=context)


class DataListView(ListView):
    template_name = 'dashboards/data-list.html'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'kwargs': self.kwargs,
            'departments': None,
            'period': None,
        }
        context.update(super().get_context_data(**kwargs))
        return context

    def get_queryset(self):
        origin = self.kwargs.get('data')
        origin_model = {
            'sources': DataSource,
            'charts': ChartData,
            'dashboards': Dashboard,
        }
        self.model = origin_model[origin]

        return self.model.objects.all()


class DataDetailView(DetailView):
    template_name = 'dashboards/data-detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'kwargs': self.kwargs,
            'object': self.object,
        }
        if self.kwargs.get('data') == 'sources':
            context['table'] = self.object.get_csv()
        return context

    def get_queryset(self):
        origin = self.kwargs.get('data')
        origin_model = {
            'sources': DataSource,
            'charts': ChartData,
            'dashboards': Dashboard,
        }
        self.model = origin_model[origin]
        return self.model.objects.all()


class DataObjectEditView(DetailView):
    template_name = 'dashboards/data-edit.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:not-implemented'))


class DataObjectDeleteView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:not-implemented'))


class DataCreateView(View):

    def get(self, request, *args, **kwargs):
        data = kwargs.get('data')
        pk = kwargs.get('pk')
        if not pk and data == 'source':
            form = DataSourceForm()
            template_name = 'dashboards/data-create-source.html'
            return render(request, template_name, {'form': form})

        return HttpResponseRedirect(reverse('dashboard:not-implemented'))

    def post(self, request, *args, **kwargs):
        data = kwargs.get('data')

        if data == 'source':
            template_name = 'dashboards/data-create-source.html'
            form = DataSourceForm(request.POST, request.FILES)
            file = request.FILES['csv']
            if not file.name.endswith('.xlsx'):
                messages.error(self.request, 'Неверный формат файла. <br>Разрешенный формат: MS Excel XLSX')
                return render(self.request, template_name, {'form': form})

            if form.is_valid():
                instance = form.save()
                handle_uploaded_file(instance, file)

                # redirect to data source list page
                return HttpResponseRedirect(reverse('dashboard:data-list', kwargs={'data': 'sources'}))
            else:
                form = DataSourceForm(request.POST, request.FILES)

            return render(self.request, template_name, {'form': form})


class DashboardCreateView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:not-implemented'))


class NotImplementedView(View):
    template_name = 'dashboards/not-implemented.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DashboardAnalyticsView(View):
    template_name = 'dashboards/dashboard-analytics.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class CreateDataChart(View):
    template_name = 'dashboards/create-data-chart.html'

    def get(self, request, *args, **kwargs):
        form = DataChartForm()
        return render(self.request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DataChartForm(request.POST, request.FILES)
        return render(self.request, self.template_name, {'form': form})


class DashboardCRMView(View):
    template_name = 'dashboards/dashboard-crm.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DashboardECommerceView(View):
    template_name = 'dashboards/dashboard-ecommerce.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DashboardLogisticView(View):
    template_name = 'dashboards/dashboard-logistic.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DashboardAcademyView(View):
    template_name = 'dashboards/dashboard-academy.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DashboardFAQView(View):
    template_name = 'dashboards/dashboard-faq.html'

    def get(self, request, *args, **kwargs):
        faq = FAQ.objects.all().order_by('section')
        return render(self.request, self.template_name, {'faq': faq})


class IndexView(View):
    template_name = 'generic/index.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class DocumentationView(View):

    def get(self, request, *args, **kwargs):
        if kwargs.get('doc'):
            template_name = f'generic/doc/{kwargs.get("doc")}.html'
        else:
            template_name = 'generic/doc/index.html'

        return render(self.request, template_name)
