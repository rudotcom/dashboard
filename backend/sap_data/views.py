import json
from datetime import datetime, date

from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from dashboards.templatetags.dashboards_extras import month_name
from sap_data.conf import SITE, LUX_DATA_COLUMNS, LUX_DATA_FOREIGN_COLUMNS, MONTH_SHORT
from sap_data.models import LuxData, Company, Manager, Site, MaterialGroup
from sap_data.utils import save_file_data, get_dataset, get_monthly_dataset, get_daily_dataset, get_y_axis_min_max, \
    get_price_dataset, remove_trailing_zeros, get_price_rise, get_monthly_site_dataset


class LuxTableUploadView(View):
    template_name = 'sap_data/upload.html'

    def get(self, request, *args, **kwargs):

        context = {
            'companies': Company.objects.filter(sector_amount__isnull=False).order_by('sector_amount', '-amount'),
            'today': date.today(),
            'columns': LUX_DATA_COLUMNS + LUX_DATA_FOREIGN_COLUMNS
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if not 'lux_file' in request.FILES:
            messages.error(self.request, 'Файл не выбран!')
            return render(self.request, self.template_name)

        file = request.FILES['lux_file']

        if not file.name.endswith('.xlsx') and not file.name.endswith('.XLSX'):
            messages.error(self.request, 'Неверный формат файла. <br>Разрешенный формат: MS Excel XLSX')
            return render(self.request, self.template_name)

        save_file_data(self.request, file)

        context = {
            'companies': Company.objects.filter(sector_amount__isnull=False).order_by('sector_amount', '-amount'),
            'today': date.today(),
        }
        return render(self.request, self.template_name, context)


class MainView(View):
    template_name = 'sap_data/main.html'

    def get(self, request, *args, **kwargs):
        year = datetime.today().year
        month = request.GET.get('month')
        site = request.GET.getlist('site')
        sector = request.GET.getlist('sector')

        queryset = LuxData.objects.all()
        if site:
            queryset = queryset.filter(site__in=site)
        if sector:
            queryset = queryset.filter(customer__sector_amount__in=sector)

        current_year_queryset = queryset.filter(factura_date__year=year)
        overall_total = current_year_queryset.aggregate(sum=Sum('amount'))['sum']

        month_data = current_year_queryset.filter(
            factura_date__month=month) if month and int(month) > 0 else current_year_queryset

        if current_year_queryset.count() == 0:
            messages.error(self.request, 'Данные отсутствуют!')
            return HttpResponseRedirect(reverse('sap_data:lux_table'))

        customers, customer_total = get_dataset(month_data, ['customer__name'], 'amount', '-total')
        products, _ = get_dataset(month_data, [
            'material__group__brief_name', 'material__group__layers', 'material__group__color'
        ], 'amount', 'material__group__name')
        managers, _ = get_dataset(month_data, ['manager__name'], 'amount', '-total')
        regions, _ = get_dataset(month_data, ['region__name'], 'amount', '-total')
        vehicles, _ = get_dataset(month_data, ['vehicle__number_plate', 'vehicle__make__name'], 'amount', '-total')

        monthly_shipment_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'amount', Sum)
        monthly_shipment_current_year = get_monthly_dataset(queryset, datetime.now().year, 'amount', Sum)
        monthly_income_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'cost_net', Sum)
        monthly_income_current_year = get_monthly_dataset(queryset, datetime.now().year, 'cost_net', Sum)

        shipment_min, shipment_max, shipment_tick = get_y_axis_min_max(
            monthly_shipment_prev_year + monthly_shipment_current_year)
        income_min, income_max, income_tick = get_y_axis_min_max(
            monthly_income_prev_year + monthly_income_current_year
        )

        monthly_price_prev_year = get_price_dataset(monthly_income_prev_year, monthly_shipment_prev_year)
        monthly_price_current_year = get_price_dataset(monthly_income_current_year, monthly_shipment_current_year)
        # get min, max for chart y axis:
        price_min, price_max, price_tick = get_y_axis_min_max(
            monthly_price_prev_year + monthly_price_current_year, 1)

        # remove all trailing zeros from price list to not display them on chart
        monthly_price_current_year = remove_trailing_zeros(monthly_price_current_year)

        price_rise, monthly_price_last = get_price_rise(monthly_price_current_year)

        number_of_months_with_price_above_zero = len(monthly_price_current_year)
        monthly_price_prev_year = [round(x, 2) for x in monthly_price_prev_year]
        monthly_price_current_year = [round(x, 2) for x in monthly_price_current_year]

        context = {
            'year': year,
            'month': month,
            'site': site,
            'sector': sector,
            'customers': customers[:21],
            'overall_total': overall_total,
            'products': products.order_by('-total'),
            'managers': managers[:21],
            'regions': regions[:21],
            'vehicles': vehicles[:21],
            'price_rise_percent': price_rise,
            'month_average_price': monthly_price_last,
            'month_of_price': number_of_months_with_price_above_zero,
            'average_price_data': json.dumps({
                "series": [
                    {
                        "name": year - 1,
                        "data": monthly_price_prev_year
                    },
                    {
                        "name": year,
                        "data": monthly_price_current_year
                    },
                ],
                "colors": ["#CACACA", "#FC0101"],
                "categories": ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                "yaxis": {"min": price_min, "max": price_max, "tickAmount": price_tick}
            }),
            'shipment_data': json.dumps({
                'series': [
                    {
                        "name": year - 1,
                        "type": "column",
                        "data": monthly_shipment_prev_year,
                    },
                    {
                        "name": year,
                        "type": "column",
                        "data": monthly_shipment_current_year,
                    }],
                "colors": ["#ECECEC", "#ED9001"],
                'categories': ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                'yaxis': {
                    "max": shipment_max,
                    "min": shipment_min,
                    "tickAmount": shipment_tick,
                }
            }),
            'sale_data': json.dumps({
                'series': [
                    {
                        "name": year - 1,
                        "type": "column",
                        "data": monthly_income_prev_year,
                    },
                    {
                        "name": year,
                        "type": "column",
                        "data": monthly_income_current_year,
                    }
                ],
                "colors": ["#ECECEC", "#01A5ED"],
                'categories': ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                'yaxis': {
                    "max": income_max,
                    "min": income_min,
                    "tickAmount": income_tick,
                }
            }),
            'product_data': json.dumps(
                {
                    "labels": [f"{product['material__group__layers']}-сл {product['material__group__brief_name']}" for product in products],
                    "series": list(map(int, [product['ratio'] for product in products])),
                    "total": f'{round(customer_total / 1000, 2)}k',
                    "colors": [product['material__group__color'] for product in products]
                }
            )

        }

        return render(self.request, self.template_name, context=context)


class MonthView(View):
    template_name = 'sap_data/month.html'

    def get(self, request, *args, **kwargs):
        year = datetime.today().year
        month = datetime.today().month
        day = request.GET.get('day')
        site = request.GET.getlist('site')
        sector = request.GET.getlist('sector')

        queryset = LuxData.objects.filter(factura_date__year=year)
        if site:
            queryset = queryset.filter(site__in=site)
        if sector:
            queryset = queryset.filter(customer__sector_amount__in=sector)

        current_month_queryset = queryset.filter(factura_date__month=month)
        overall_total = current_month_queryset.aggregate(sum=Sum('amount'))['sum']

        day_data = current_month_queryset.filter(
            factura_date__day=day) if day and int(day) > 0 else current_month_queryset

        if current_month_queryset.count() == 0:
            messages.error(self.request, 'Данные отсутствуют!')
            return HttpResponseRedirect(reverse('sap_data:lux_table'))

        customers, customer_total = get_dataset(day_data, ['customer__name'], 'amount', '-total')
        products, _ = get_dataset(day_data, [
            'material__group__brief_name', 'material__group__layers', 'material__group__color'
        ], 'amount', 'material__group__name')
        managers, _ = get_dataset(day_data, ['manager__name'], 'amount', '-total')
        regions, _ = get_dataset(day_data, ['region__name'], 'amount', '-total')
        vehicles, _ = get_dataset(day_data, ['vehicle__number_plate', 'vehicle__make__name'], 'amount', '-total')

        daily_shipment_prev_month = get_daily_dataset(queryset, year, month - 1, 'amount', Sum)
        daily_shipment_current_month = get_daily_dataset(queryset, year, month, 'amount', Sum)
        daily_income_prev_month = get_daily_dataset(queryset, year, month - 1, 'cost_net', Sum)
        daily_income_current_month = get_daily_dataset(queryset, year, month, 'cost_net', Sum)

        shipment_min, shipment_max, shipment_tick = get_y_axis_min_max(
            daily_shipment_prev_month + daily_shipment_current_month)
        income_min, income_max, income_tick = get_y_axis_min_max(
            daily_income_prev_month + daily_income_current_month
        )

        daily_price_prev_month = get_price_dataset(daily_income_prev_month, daily_shipment_prev_month)
        daily_price_current_month = get_price_dataset(daily_income_current_month, daily_shipment_current_month)
        # get min, max for chart y-axis:
        price_min, price_max, price_tick = get_y_axis_min_max(
            daily_price_prev_month + daily_price_current_month, 1)

        day_range = range(1, len(daily_price_current_month) + 1)
        # remove all trailing zeros from price list to not display them on chart
        while daily_price_current_month and daily_price_current_month[-1] == 0:
            daily_price_current_month.pop()

        # remove all trailing zeros from price list to not display them on chart
        daily_price_current_month = remove_trailing_zeros(daily_price_current_month)
        number_of_daily_price_current_month = len(daily_price_current_month)

        price_rise, daily_price_last = get_price_rise(daily_price_current_month)
        daily_price_prev_month = [round(x, 2) for x in daily_price_prev_month]
        daily_price_current_month = [round(x, 2) for x in daily_price_current_month]


        context = {
            'month': month,
            'day': day,
            'day_range': list(day_range),
            'site': site,
            'sector': sector,
            'customers': customers[:21],
            'overall_total': overall_total,
            'products': products.order_by('-total'),
            'managers': managers[:21],
            'regions': regions[:21],
            'vehicles': vehicles[:21],
            'price_rise_percent': price_rise,
            'day_average_price': daily_price_last,
            'day_of_price': number_of_daily_price_current_month + 1,
            'average_price_data': json.dumps({
                "series": [
                    {
                        "name": month_name(month),
                        "data": daily_price_current_month,
                        "color": '#FC0101'
                    },
                ],
                "colors": ["#FC0101"],
                'categories': list(day_range),
                "yaxis": {"min": price_min, "max": price_max, "tickAmount": price_tick}
            }),
            'shipment_data': json.dumps({
                "series": [
                    {
                        "name": month_name(month),
                        "type": "column",
                        "data": daily_shipment_current_month,
                    },
                ],
                "colors": ["#ED9001"],
                'categories': list(day_range),
                "yaxis": {
                    "max": shipment_max,
                    "min": shipment_min,
                    "tickAmount": shipment_tick,
                }
            }),
            'sale_data': json.dumps({
                "series": [
                    {
                        "name": month_name(month),
                        "type": "column",
                        "data": daily_income_current_month,
                    },
                ],
                "colors": ["#01A5ED"],
                'categories': list(day_range),
                "yaxis": {
                    "max": income_max,
                    "min": income_min,
                    "tickAmount": income_tick,
                }
            }),
            'product_data': json.dumps(
                {
                    "labels": [f"{product['material__group__layers']}-сл {product['material__group__brief_name']}" for product in products],
                    "series": list(map(int, [product['ratio'] for product in products])),
                    "total": f'{round(customer_total / 1000, 2)}k',
                    "colors": [product['material__group__color'] for product in products]
                }
            )

        }

        return render(self.request, self.template_name, context=context)


class CompareView(View):
    template_name = 'sap_data/compare-sites.html'

    def get(self, request, *args, **kwargs):
        year = datetime.today().year
        group = request.GET.getlist('group')
        sector = request.GET.getlist('sector')

        queryset = LuxData.objects.filter(factura_date__year=year)
        if group:
            queryset = queryset.filter(material__group__code__in=group)
        if sector:
            queryset = queryset.filter(customer__sector_amount__in=sector)

        overall_total = queryset.aggregate(sum=Sum('amount'))['sum']

        if queryset.count() == 0:
            messages.error(self.request, 'Данные отсутствуют!')
            return HttpResponseRedirect(reverse('sap_data:lux_table'))

        monthly_shipment_current_year = []
        monthly_income_current_year = []

        shipment_series = []
        income_series = []
        site_colors = []
        for site in Site.objects.all():
            site_colors.append(site.color)
            site_shipment_dataset = get_monthly_site_dataset(queryset, site, 'amount', Sum)
            site_income_dataset = get_monthly_site_dataset(queryset, site, 'cost_net', Sum)
            monthly_shipment_current_year.append(site_shipment_dataset)
            monthly_income_current_year.append(site_income_dataset)
            shipment_series.append({
                "name": site.brief_name,
                "data": site_shipment_dataset,
            })
            income_series.append({
                "name": site.brief_name,
                "data": site_income_dataset,
            })

        shipment_min, shipment_max, shipment_tick = get_y_axis_min_max(
            [element for sublist in monthly_shipment_current_year for element in sublist]
        )
        income_min, income_max, income_tick = get_y_axis_min_max(
            [element for sublist in monthly_income_current_year for element in sublist]
        )

        context = {
            'year': year,
            'group': group,
            'material_groups_3': MaterialGroup.objects.filter(layers=3),
            'material_groups_5': MaterialGroup.objects.filter(layers=5),
            'sector': sector,
            'overall_total': overall_total,
            'shipment_data': json.dumps({
                'series': shipment_series,
                "colors": site_colors,
                'categories': MONTH_SHORT,
                'yaxis': {
                    "max": shipment_max,
                    "min": shipment_min,
                    "tickAmount": shipment_tick,
                }
            }),
            'sale_data': json.dumps({
                'series': income_series,
                "colors": site_colors,
                'categories': MONTH_SHORT,
                'yaxis': {
                    "max": income_max,
                    "min": income_min,
                    "tickAmount": income_tick,
                }
            }),
        }

        return render(self.request, self.template_name, context=context)


class ManagerView(View):
    template_name = 'sap_data/manager.html'

    def get(self, request, *args, **kwargs):
        year = datetime.today().year
        month = request.GET.get('month')
        site = request.GET.getlist('site')
        manager = request.GET.get('manager')

        queryset = LuxData.objects.all()
        if manager:
            manager = Manager.objects.get(pk=manager)
            queryset = queryset.filter(manager=manager)
        if site:
            queryset = queryset.filter(site__in=site).select_related('manager')

        current_year_queryset = queryset.filter(factura_date__year=year)
        overall_total = current_year_queryset.aggregate(sum=Sum('amount'))['sum']
        context = {
            'year': year,
            'month': month,
            'site': site,
            'managers': Manager.objects.filter(managers__factura_date__year=year).distinct('name'),
            'manager': manager,
        }
        if overall_total is None:
            messages.info(request, 'Данные по выбранным критериям отсутствуют!')
            overall_total = 0
            context['overall_total'] = overall_total
            return render(self.request, self.template_name, context=context)

        month_data = current_year_queryset.filter(
            factura_date__month=month) if month and int(month) > 0 else current_year_queryset

        sites, site_total = get_dataset(month_data, ['site'], 'amount', "-total")
        for dicti in sites:
            dicti.update({'site': dict(SITE)[dicti['site']]})

        customers, customer_total = get_dataset(month_data, ['customer__name'], 'amount', '-total')
        products, _ = get_dataset(month_data, [
            'material__group__brief_name', 'material__group__layers', 'material__group__color'
        ], 'amount', 'material__group__name')
        regions, _ = get_dataset(month_data, ['region__name'], 'amount', '-total')
        vehicles, _ = get_dataset(month_data, ['vehicle__number_plate', 'vehicle__make__name'], 'amount', '-total')

        monthly_shipment_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'amount', Sum)
        monthly_shipment_current_year = get_monthly_dataset(queryset, datetime.now().year, 'amount', Sum)
        monthly_income_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'cost_net', Sum)
        monthly_income_current_year = get_monthly_dataset(queryset, datetime.now().year, 'cost_net', Sum)

        shipment_min, shipment_max, shipment_tick = get_y_axis_min_max(
            monthly_shipment_prev_year + monthly_shipment_current_year)
        income_min, income_max, income_tick = get_y_axis_min_max(
            monthly_income_prev_year + monthly_income_current_year
        )

        monthly_price_prev_year = get_price_dataset(monthly_income_prev_year, monthly_shipment_prev_year)
        monthly_price_current_year = get_price_dataset(monthly_income_current_year, monthly_shipment_current_year)

        # get min, max for chart y axis:
        price_min, price_max, price_tick = get_y_axis_min_max(
            monthly_price_prev_year + monthly_price_current_year, 1)

        # remove all trailing zeros from price list to not display them on chart
        monthly_price_current_year = remove_trailing_zeros(monthly_price_current_year)

        price_rise, monthly_price_last = get_price_rise(monthly_price_current_year)

        number_of_months_with_price_above_zero = len(monthly_price_current_year)
        monthly_price_prev_year = [round(x, 2) for x in monthly_price_prev_year]
        monthly_price_current_year = [round(x, 2) for x in monthly_price_current_year]

        context.update({
            'sites': sites,
            'site_total': site_total,
            'customers': customers[:21],
            'overall_total': overall_total,
            'products': products.order_by('-total'),
            'regions': regions[:21],
            'vehicles': vehicles[:21],
            'price_rise_percent': price_rise,
            'month_average_price': monthly_price_last,
            'month_of_price': number_of_months_with_price_above_zero,
            'average_price_data': json.dumps({
                "series": [
                    {
                        "name": year - 1,
                        "data": monthly_price_prev_year
                    },
                    {
                        "name": year,
                        "data": monthly_price_current_year
                    },
                ],
                "colors": ["#CACACA", "#FC0101"],
                'categories': MONTH_SHORT,
                "yaxis": {"min": price_min, "max": price_max, "tickAmount": price_tick}
            }),
            'shipment_data': json.dumps({
                'series': [
                    {
                        "name": datetime.now().year - 1,
                        "type": "column",
                        "data": monthly_shipment_prev_year,
                    },
                    {
                        "name": datetime.now().year,
                        "type": "column",
                        "data": monthly_shipment_current_year,
                    }],
                "colors": ["#ECECEC", "#ED9001"],
                'categories': MONTH_SHORT,
                'yaxis': {
                    "max": shipment_max,
                    "min": shipment_min,
                    "tickAmount": shipment_tick,
                }
            }),
            'sale_data': json.dumps({
                'series': [
                    {
                        "name": year - 1,
                        "type": "column",
                        "data": monthly_income_prev_year,
                    },
                    {
                        "name": year,
                        "type": "column",
                        "data": monthly_income_current_year,
                    }],
                "colors": ["#ECECEC", "#01A5ED"],
                'categories': MONTH_SHORT,
                'yaxis': {"max": income_max,
                          "min": income_min,
                          'tickAmount': income_tick
                          }
            }),
            'product_data': json.dumps(
                {
                    "labels": [f"{product['material__group__layers']}-сл {product['material__group__brief_name']}" for product in products],
                    "series": list(map(int, [product['ratio'] for product in products])),
                    "total": f'{round(customer_total / 1000, 2)}k',
                    "colors": [product['material__group__color'] for product in products]
                }
            )
        })
        return render(self.request, self.template_name, context=context)


class CustomerView(View):
    template_name = 'sap_data/customer.html'

    def get(self, request, *args, **kwargs):
        year = datetime.today().year
        month = request.GET.get('month')
        site = request.GET.getlist('site')
        customer = request.GET.get('customer')
        sector = request.GET.get('sector') or 'big'

        queryset = LuxData.objects.filter(customer__sector_amount=sector).select_related('customer')

        if customer:
            customer = Company.objects.get(pk=customer)
            queryset = queryset.filter(customer=customer)

        current_year_queryset = queryset.filter(factura_date__year=year)
        overall_total = current_year_queryset.aggregate(sum=Sum('amount'))['sum']
        context = {
            'year': year,
            'month': month,
            'sector': sector,
            'sites': SITE,
            'site': site,
            'customers': Company.objects.filter(
                sector_amount=sector, customers__factura_date__year=year
            ).distinct('name_stripped'),
            'customer': customer,
        }
        if overall_total is None:
            messages.info(request, 'Данные по выбранным критериям отсутствуют!')
            context['overall_total'] = 0
            return render(self.request, self.template_name, context=context)

        month_data = current_year_queryset.filter(
            factura_date__month=month) if month and int(month) > 0 else current_year_queryset

        sites, site_total = get_dataset(month_data, ['site'], 'amount', "-total")
        for dicti in sites:
            dicti.update({'site': dict(SITE)[dicti['site']]})
        managers, _ = get_dataset(month_data, ['manager__name'], 'amount', '-total')
        products, _ = get_dataset(month_data, [
            'material__group__brief_name', 'material__group__layers', 'material__group__color'
        ], 'amount', 'material__group__name')
        regions, _ = get_dataset(month_data, ['region__name'], 'amount', '-total')
        vehicles, _ = get_dataset(month_data, ['vehicle__number_plate', 'vehicle__make__name'], 'amount', '-total')

        monthly_shipment_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'amount', Sum)
        monthly_shipment_current_year = get_monthly_dataset(queryset, datetime.now().year, 'amount', Sum)
        monthly_income_prev_year = get_monthly_dataset(queryset, datetime.now().year - 1, 'cost_net', Sum)
        monthly_income_current_year = get_monthly_dataset(queryset, datetime.now().year, 'cost_net', Sum)

        shipment_min, shipment_max, shipment_tick = get_y_axis_min_max(
            monthly_shipment_prev_year + monthly_shipment_current_year)
        income_min, income_max, income_tick = get_y_axis_min_max(
            monthly_income_prev_year + monthly_income_current_year
        )

        monthly_price_prev_year = get_price_dataset(monthly_income_prev_year, monthly_shipment_prev_year)
        monthly_price_current_year = get_price_dataset(monthly_income_current_year, monthly_shipment_current_year)
        # get min, max for chart y axis:
        price_min, price_max, price_tick = get_y_axis_min_max(
            monthly_price_prev_year + monthly_price_current_year, 1)

        # remove all trailing zeros from price list to not display them on chart
        monthly_price_current_year = remove_trailing_zeros(monthly_price_current_year)

        price_rise, monthly_price_last = get_price_rise(monthly_price_current_year)

        number_of_months_with_price_above_zero = len(monthly_price_current_year)
        monthly_price_prev_year = [round(x, 2) for x in monthly_price_prev_year]
        monthly_price_current_year = [round(x, 2) for x in monthly_price_current_year]

        context.update({
            'sites': sites,
            'site_total': site_total,
            'managers': managers[:21],
            'overall_total': overall_total,
            'products': products.order_by('-total'),
            'regions': regions[:21],
            'vehicles': vehicles[:21],
            'price_rise_percent': price_rise,
            'month_average_price': monthly_price_last,
            'month_of_price': number_of_months_with_price_above_zero,
            'average_price_data': json.dumps({
                "series": [
                    {
                        "name": year - 1,
                        "data": monthly_price_prev_year
                    },
                    {
                        "name": year,
                        "data": monthly_price_current_year
                    },
                ],
                "colors": ["#CACACA", "#FC0101"],
                'categories': MONTH_SHORT,
                "yaxis": {"min": price_min, "max": price_max, "tickAmount": price_tick}
            }),
            'shipment_data': json.dumps({
                'series': [
                    {
                        "name": datetime.now().year - 1,
                        "type": "column",
                        "data": monthly_shipment_prev_year,
                    },
                    {
                        "name": datetime.now().year,
                        "type": "column",
                        "data": monthly_shipment_current_year,
                    }],
                "colors": ["#ECECEC", "#ED9001"],
                'categories': MONTH_SHORT,
                'yaxis': {
                    "max": shipment_max,
                    "min": shipment_min,
                    "tickAmount": shipment_tick,
                }
            }),
            'sale_data': json.dumps({
                'series': [
                    {
                        "name": year - 1,
                        "type": "column",
                        "data": monthly_income_prev_year,
                    },
                    {
                        "name": year,
                        "type": "column",
                        "data": monthly_income_current_year,
                    }],
                "colors": ["#ECECEC", "#01A5ED"],
                'categories': MONTH_SHORT,
                'yaxis': {"max": income_max,
                          "min": income_min,
                          'tickAmount': income_tick
                          }
            }),
            'product_data': json.dumps({
                "labels": [f"{product['material__group__layers']}-сл {product['material__group__brief_name']}" for
                           product in products],
                "series": list(map(int, [product['ratio'] for product in products])),
                "total": f'{round(overall_total / 1000, 2)}k',
                "colors": [product['material__group__color'] for product in products]
            })
        })

        return render(self.request, self.template_name, context=context)
