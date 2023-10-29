import calendar
import math
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum, F, IntegerField
from django.db.models.functions import Cast, TruncMonth, TruncDay

from sap_data.conf import LUX_DATA_COLUMNS, LUX_DATA_FOREIGN_COLUMNS
from sap_data.models import Manager, Vehicle, VehicleMake, MaterialClass, MaterialGroup, Material, \
    Company, Address, LuxData, Region, Contract, Site


def save_df_to_model(request, df):
    cache.set('stage', 'reading db', timeout=None)
    vehicle_make_list = {make.name: make for make in VehicleMake.objects.all()}
    vehicle_list = {vehicle.number_plate: vehicle for vehicle in Vehicle.objects.all()}
    material_class_list = {m_class.name: m_class for m_class in MaterialClass.objects.all()}
    material_group_list = {group.code: group for group in MaterialGroup.objects.all()}
    material_list = {material.name: material for material in Material.objects.all()}
    company_list = {company.sap_id: company for company in Company.objects.all()}
    address_list = {address.address: address for address in Address.objects.all()}
    manager_list = {manager.name: manager for manager in Manager.objects.all()}
    region_list = {region.code: region for region in Region.objects.all()}
    contract_list = {contract.number: contract for contract in Contract.objects.all()}
    site_list = {site.code: site for site in Site.objects.all()}
    print(material_group_list)

    def get_create_site(site, site_name):
        if site not in site_list:
            site_list[site] = Site.objects.create(code=site, name=site_name)
        return site_list[site]

    def get_create_vehicle(*vehicle):
        vehicle_make, vehicle_number_plate, vehicle_type = vehicle
        if vehicle_number_plate is np.nan:
            return None

        if vehicle_make is np.nan:
            vehicle_make_list[vehicle_make] = None
        elif vehicle_make not in vehicle_make_list:
            vehicle_make_list[vehicle_make] = VehicleMake.objects.create(name=vehicle_make)

        if vehicle_number_plate not in vehicle_list:
            vehicle_list[vehicle_number_plate] = Vehicle.objects.create(
                number_plate=vehicle_number_plate, make=vehicle_make_list[vehicle_make], type=vehicle_type)

        return vehicle_list[vehicle_number_plate]

    def get_create_material(*material):
        material, name, material_group, m_class, class_name, group_name = material
        if material is None:
            return None

        if class_name not in material_class_list:
            material_class_list[class_name] = MaterialClass.objects.create(code=m_class, name=class_name)

        if str(material_group) not in material_group_list:
            material_group_list[str(material_group)] = MaterialGroup.objects.create(
                code=str(material_group), name=group_name, m_class=material_class_list[class_name])

        if material not in material_list:
            material_list[material] = Material.objects.create(code=material, name=name,
                                                              group=material_group_list[str(material_group)])
        return material_list[material]

    def get_create_company(sap_id, name, address):
        if np.isnan(sap_id):
            return None

        address = get_create_address(address) if address else None

        if sap_id not in company_list:
            company_list[sap_id] = Company.objects.create(sap_id=sap_id, name=name, address=address)
        return company_list[sap_id]

    def get_create_manager(manager_name):
        if manager_name is np.nan:
            return None
        if manager_name not in manager_list:
            manager_list[manager_name] = Manager.objects.create(name=manager_name)
        return manager_list[manager_name]

    def get_create_address(address):
        if address is None or address is np.nan:
            return None
        if address not in address_list:
            address_list[address] = Address.objects.create(address=address)
        return address_list[address]

    def get_create_region(region, region_name):
        if np.isnan(region):
            return None
        if region not in region_list:
            region_list[region] = Region.objects.create(code=int(region), name=region_name)
        return region_list[region]

    def get_create_contract(contract, contract_date):
        contract_date = pd.Timestamp(contract_date).to_pydatetime()
        if contract is np.nan:
            return None
        if contract not in contract_list:
            contract_list[contract] = Contract.objects.create(number=contract, date=contract_date)
        return contract_list[contract]

    # parsing df rows
    cache.set('stage', 'importing', timeout=None)
    imported, skipped, errors = 0, 0, 0
    data_batch = []
    for i, row in enumerate(df.itertuples()):
        cache.set('progress', i * 100 // len(df), timeout=None)
        if i % 100 == 0:
            print(cache.get('stage'), cache.get('progress'))
        lux_data = LuxData()
        for field in LUX_DATA_COLUMNS:  # attributes having no foreign key - tuples
            try:
                value = field[2](getattr(row, field[0]))  # assign data type from conf tuple
            except ValueError:
                value = None
            # convert date to pandas date format
            value = value.to_pydatetime() if 'date' in field[0] else value

            if value and not pd.isna(value):
                setattr(lux_data, field[0], value)

        lux_data.my_site = get_create_site(row.site, row.site_name)
        lux_data.customer = get_create_company(
            row.customer,
            row.customer_name,
            row.address_customer,
        )
        lux_data.recipient = get_create_company(
            row.recipient,
            row.recipient_name,
            row.address_recipient,
        )
        lux_data.payer = get_create_company(
            row.payer,
            row.payer_name,
            None
        )
        lux_data.address_delivery = get_create_address(row.address_delivery)
        lux_data.material = get_create_material(
            row.material,
            row.material_name,
            row.material_group,
            row.material_class,
            row.material_class_name,
            row.material_group_name,
        )
        lux_data.vehicle = get_create_vehicle(
            row.vehicle_make,
            row.vehicle_number_plate,
            row.vehicle_type,
        )
        lux_data.manager = get_create_manager(row.manager)
        lux_data.manager_dispatch = get_create_manager(row.manager_dispatch)
        lux_data.region = get_create_region(row.region, row.region_name)
        lux_data.contract = get_create_contract(row.contract, row.contract_date)

        data_batch.append(lux_data)

    lines = len(LuxData.objects.bulk_create(data_batch, batch_size=500, ignore_conflicts=True))

    return lines


def save_file_data(request, file):
    lux_headers = {field[1]: field[0] for field in LUX_DATA_COLUMNS + LUX_DATA_FOREIGN_COLUMNS}
    pd_data_types = {field[0]: field[2] for field in LUX_DATA_COLUMNS + LUX_DATA_FOREIGN_COLUMNS}

    cache.set('stage', 'uploading', timeout=None)
    df = pd.read_excel(
        io=file,
        header=0,
        usecols=lux_headers.keys(),
        dtype=pd_data_types,
    )
    # Проверить наличие заголовка столбцов
    try:
        df.loc[:, lux_headers.keys()]
    except BaseException as e:
        messages.warning(request, f'Импорт невозможен\nФормат файла не соответствует требованиям:\n\n{e}\n'
                                  f'\nФайл должен содержать колонки {lux_headers.keys()}\n')
        return

    df = df.rename(columns=lux_headers)
    df.dropna(how='all', axis=1, inplace=True)

    imported = save_df_to_model(request, df)
    sectorize()

    messages.info(request, f'Файл загружен!<hr>Строк: {imported}')

    return messages


def sectorize():
    # get the month previous to current one
    prev_month = datetime.today().replace(day=1) - timedelta(days=1)
    year, month = prev_month.year, prev_month.month

    sales = LuxData.objects.filter(factura_date__year=year, factura_date__month=month)

    df = pd.DataFrame(sales.values())

    df_sector = df.groupby(['customer_id'])['amount'].sum().reset_index().sort_values(by='amount', ascending=False)

    cache.set('stage', 'sectorizing', timeout=None)
    for row in df_sector.itertuples():
        customer = Company.objects.get(id=row.customer_id)
        customer.assign_sector(row.amount)


def get_dataset(queryset, attribute, summable, sort=None):
    queryset = queryset.values(*attribute).annotate(total=Sum(summable)).exclude(total__exact=None)
    top_queryset_total = sum([total for total in queryset.order_by('-total')[:10].values_list('total', flat=True)])
    top_queryset_amount = queryset.order_by('-total')[0]['total'] if queryset else 0
    total = sum([total for total in queryset.filter(total__gt=0).order_by('-total').values_list('total', flat=True)])
    dataset = queryset.annotate(ratio=(F('total') / top_queryset_total * 100)).annotate(
        ratio=Cast('ratio', IntegerField())).order_by('-total')
    dataset = dataset.annotate(top_ratio=(F('total') / top_queryset_amount * 100)).annotate(
        top_ratio=Cast('top_ratio', IntegerField())).order_by(sort)

    return dataset, total


def get_y_axis_min_max(dataset, multiplier=1000):
    non_zero_dataset = [total for total in dataset if total != 0]
    min_value = math.floor(min(non_zero_dataset) / multiplier) * multiplier if non_zero_dataset else 0
    max_value = math.ceil(max(dataset) / multiplier) * multiplier if non_zero_dataset else 0
    tick = (max_value - min_value) / 5 / multiplier
    # TODO: fix tick for different charts
    return min_value, max_value, 5


def get_monthly_dataset(queryset, year, param, annotation):
    """
    Acquire a list of values by month of year
    :param queryset: queryset to be annoteted
    :param year: year to filter
    :param param: queryset attribute to annotate by
    :param annotation: annotation function applied to attribute
    :return: list of values
    """
    queryset = queryset.filter(factura_date__year=year)

    dataset = get_totals_by_month(annotation, param, queryset)
    return list(map(float, dataset))


def get_totals_by_month(annotation, param, queryset):
    dataset = [0] * 12
    queryset = queryset.annotate(month=TruncMonth('factura_date')) \
        .values('month') \
        .annotate(total=annotation(param))
    for item in queryset:
        dataset[item['month'].month - 1] = round(item['total'] / 1000, 2)
    return dataset


def get_monthly_site_dataset(queryset, site, param, annotation):
    queryset = queryset.filter(my_site=site)
    dataset = get_totals_by_month(annotation, param, queryset)

    dataset = remove_trailing_zeros(dataset)
    return list(map(float, dataset))


def get_daily_dataset(queryset, year, month, param, annotation):
    """
    Acquire a list of values by day of month
    :param queryset: queryset to be annoteted
    :param year: corrent year to get number of day in a month
    :param month: month to filter
    :param param: queryset attribute to annotate by
    :param annotation: annotation function applied to attribute
    :return: list of values, max value, min value rounded up for axes,
    """
    num_days = calendar.monthrange(year, month)[1]
    dataset = [0] * num_days
    queryset = queryset.filter(factura_date__month=month).annotate(day=TruncDay('factura_date')) \
        .values('day') \
        .annotate(total=annotation(param))
    for item in queryset:
        dataset[item['day'].day - 1] = round(item['total'] / 1000, 2)
    return list(map(float, dataset))


def get_price_dataset(income_dataset, shipment_dataset):
    # Average price is calculated as income / shipment every period (month, day)
    return [
        x / y if y else 0 for x, y in zip(
            map(float, income_dataset), map(float, shipment_dataset))
    ]


def remove_trailing_zeros(dataset):
    while dataset and dataset[-1] == 0:
        dataset.pop()
    return dataset


def get_price_rise(dataset):
    if len(dataset) > 1:
        monthly_price_last = dataset[-1]  # last value above zero
        monthly_price_prev_last = dataset[-2]  # before last value
        price_rise_on_prev_month = int(
            (monthly_price_last - monthly_price_prev_last) / monthly_price_prev_last * 100
        ) if monthly_price_prev_last else 0
    else:
        price_rise_on_prev_month = monthly_price_last = 0
    return price_rise_on_prev_month, monthly_price_last
