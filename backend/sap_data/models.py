import datetime

from django.db import models

from sap_data.conf import *


class Site(models.Model):
    code = models.SmallIntegerField(verbose_name="Код Филиала")
    name = models.CharField(verbose_name="Наименование", max_length=100, blank=True, null=True)
    brief_name = models.CharField(verbose_name="Краткое наименование", max_length=20, blank=True, null=True)
    eng_name = models.CharField(verbose_name="Наименование на английском", max_length=20, blank=True, null=True)
    color = models.CharField(verbose_name="Цвет", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
        ordering = ['code']


class Manager(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100, blank=True, null=True)


class VehicleMake(models.Model):
    name = models.CharField(verbose_name="Марка транспортного средства", max_length=100, blank=True, null=True)


class Vehicle(models.Model):
    number_plate = models.CharField(verbose_name="Регистрационный номер ТС", max_length=100, blank=True, null=True)
    make = models.ForeignKey(VehicleMake, verbose_name="Марка транспортного средства", on_delete=models.CASCADE,
                             null=True)
    type = models.CharField(verbose_name="Тип транспортного средства", max_length=100, choices=VEHICLE_TYPE,
                            blank=True, null=True)


class MaterialClass(models.Model):
    # Гофротара
    # Гофрокартон
    code = models.CharField(verbose_name="Код вида материала", max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name="Наименование вида материала", max_length=100, blank=True, null=True)


class MaterialGroup(models.Model):
    # Гофрокороб 4-х клапанный 3-х слойный
    # Гофрокороб сложной высечки 3-х слойный
    # Гофрокартон 5-ти слойный
    # Комплектующие 3-х слойные
    code = models.CharField(verbose_name="Код группы материала", max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name="Наименование группы", max_length=100, blank=True, null=True)
    m_class = models.ForeignKey(MaterialClass, verbose_name="Вид материала", on_delete=models.CASCADE)
    layers = models.CharField(verbose_name="Количество слоев", max_length=1, choices=((3, '3-сл'), (5, '5-сл')),
                              blank=True, null=True)
    brief_name = models.CharField(verbose_name="Краткое наименование", max_length=20, blank=True, null=True)
    color = models.CharField(verbose_name="Цвет", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Группа материалов"
        verbose_name_plural = "Группы материалов"
        ordering = ['layers', 'brief_name']


class Material(models.Model):
    code = models.CharField(verbose_name="Код материала", max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name="Наименование", max_length=100, blank=True, null=True)
    group = models.ForeignKey(MaterialGroup, verbose_name="Группа", on_delete=models.CASCADE)


class Address(models.Model):
    address = models.CharField(verbose_name="Адрес Заказчика", max_length=500, blank=True, null=True)


class Company(models.Model):
    sap_id = models.PositiveIntegerField(verbose_name="ID заказчика SAP", blank=True, null=True)
    name = models.CharField(verbose_name="Наименование заказчика", max_length=100, blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name="Адрес", on_delete=models.CASCADE, null=True)
    sector_amount = models.CharField(verbose_name="Сектор", max_length=100, blank=True, null=True,
                                     choices=SECTOR_AMOUNT)
    amount = models.DecimalField(verbose_name="Объем м2 в месяц", max_digits=10, decimal_places=3, null=True)
    last_checked = models.DateField(verbose_name="Последнее обновление", null=True)
    name_stripped = models.CharField(verbose_name="Наименование без формы собственности", max_length=100,
                                     blank=True, null=True)

    def assign_sector(self, month_amount):
        self.amount = month_amount
        if month_amount >= SECTOR_CRITERIA['big']:
            self.sector_amount = 'big'
        elif month_amount >= SECTOR_CRITERIA['middle']:
            self.sector_amount = 'middle'
        else:
            self.sector_amount = 'small'
        self.last_checked = datetime.datetime.now()
        self.save()

    @property
    def get_display(self):
        return self.get_sector_amount_display()

    def save(self, *args, **kwargs):
        self.name_stripped = self.name.upper().strip()
        for form in COMPANY_FORMS:
            if form.upper() in self.name_stripped:
                self.name_stripped = self.name_stripped.removeprefix(
                    form + ' '
                ).strip().strip('"').strip('«').strip('»').strip('“').strip()
        super(Company, self).save()

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"
        ordering = ('name_stripped', )


class Region(models.Model):
    code = models.CharField(verbose_name="Регион", max_length=3)
    name = models.CharField(verbose_name="Наименование региона", max_length=100)


class Contract(models.Model):
    number = models.CharField(verbose_name="Номер договора", max_length=100)
    date = models.DateField(verbose_name="Дата договора")


class LuxData(models.Model):
    factura = models.PositiveIntegerField(verbose_name="Фактура")
    factura_date = models.DateField(verbose_name="Дата фактуры")
    factura_class = models.CharField(verbose_name="Вид фактуры", max_length=5, choices=FACTURA_CLASS)
    factura_type = models.CharField(verbose_name="Тип фактуры", max_length=5, choices=FACTURA_TYPE)
    sales_channel = models.CharField(verbose_name="Канал продаж", max_length=5, choices=SALES_CHANNEL)
    sales_dept = models.CharField(verbose_name="Отдел сбыта", max_length=5, choices=SALES_DEPT)
    sales_group = models.CharField(verbose_name="Группа сбыта", max_length=5, choices=SALES_GROUP)
    sales_docu_type = models.CharField(verbose_name="Тип документа сбыта", max_length=3, choices=SALES_DOCU_TYPE)
    my_site = models.ForeignKey(Site, verbose_name="Филиал", on_delete=models.CASCADE, null=True)
    site = models.CharField(verbose_name="Завод", max_length=4, choices=SITE)
    warehouse = models.CharField(verbose_name="Склад", max_length=4, choices=WAREHOUSE)
    shipment = models.PositiveIntegerField(verbose_name="Поставка", blank=True, null=True)
    shipment_class = models.CharField(verbose_name="Вид поставки", max_length=5, choices=SHIPMENT_CLASS)
    date_created = models.DateField(verbose_name="Дата создания")
    date_fact = models.DateField(verbose_name="Дата ФактДвиженМтр", null=True)
    created_by = models.CharField(verbose_name="Создал", max_length=20)
    customer = models.ForeignKey(Company, verbose_name="Заказчик", on_delete=models.CASCADE, related_name='customers')
    recipient = models.ForeignKey(Company, verbose_name="Получатель материала", on_delete=models.CASCADE,
                                  related_name='recipients', null=True)
    payer = models.ForeignKey(Company, verbose_name="Плательщик", on_delete=models.CASCADE, related_name='payers',
                              null=True)
    address_delivery = models.ForeignKey(Address, verbose_name="Адрес Доставки", related_name='delivery_addresses',
                                         on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, verbose_name="Регион", on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(verbose_name="Город", max_length=150, blank=True, null=True)
    street = models.CharField(verbose_name="Улица", max_length=150, blank=True, null=True)
    shipper = models.CharField(verbose_name="Пункт отгрузки/приемки", max_length=5, choices=SHIPPER,
                               blank=True, null=True)
    country = models.CharField(verbose_name="Страна получатель", max_length=15, choices=COUNTRY)
    material = models.ForeignKey(Material, verbose_name="Материал", on_delete=models.CASCADE)
    short_text = models.CharField(verbose_name="Краткий текст позиции заказа клиента", max_length=100)
    vehicle = models.ForeignKey(Vehicle, verbose_name="Транспорт", on_delete=models.CASCADE, blank=True, null=True)

    currency = models.CharField(verbose_name="Валюта", max_length=3, choices=CURRENCY)
    price_doc = models.DecimalField(verbose_name="Цена в валюте документа", max_digits=10, decimal_places=2)
    price = models.DecimalField(verbose_name="Цена за 1000 м2", max_digits=11, decimal_places=3, null=True)
    price_derived = models.DecimalField(verbose_name="Цена расч.", max_digits=11, decimal_places=2, null=True)
    price_usd = models.DecimalField(verbose_name="Цена в USD", max_digits=7, decimal_places=2, null=True)
    price_unit = models.CharField(verbose_name="Единица цены", max_length=7, choices=PRICE_UNIT)
    cost_net = models.DecimalField(verbose_name="Стоимость нетто", max_digits=12, decimal_places=2, null=True)
    cost = models.DecimalField(verbose_name="Сумма в рублях", max_digits=12, decimal_places=2, null=True)
    cost_boe = models.DecimalField(verbose_name="Сумма в рублях на дату ГТД", max_digits=12, decimal_places=2, null=True)
    vat = models.DecimalField(verbose_name="НДС", max_digits=10, decimal_places=2, null=True)
    cost_vat = models.DecimalField(verbose_name="Сумма с НДС", max_digits=12, decimal_places=2, null=True)
    cost_usd = models.DecimalField(verbose_name="Стоимость в USD", max_digits=9, decimal_places=2, null=True)
    cost_gross = models.DecimalField(verbose_name="Стоимость в внутренней валюте", max_digits=12, decimal_places=2, null=True)

    weight_net = models.DecimalField(verbose_name="Вес нетто", max_digits=9, decimal_places=3, null=True)
    weight_gross = models.DecimalField(verbose_name="Вес брутто", max_digits=9, decimal_places=3, null=True)
    weight_unit = models.CharField(verbose_name="Единица веса", max_length=5, choices=WEIGHT_UNIT)
    number = models.DecimalField(verbose_name="Кол-во в ед. продажи", max_digits=9, decimal_places=3, null=True)
    sale_unit = models.CharField(verbose_name="ЕИ продажи", max_length=5, choices=SALE_UNIT)
    amount = models.DecimalField(verbose_name="Объем в ед. продажи", max_digits=9, decimal_places=3, null=True)
    deliverance = models.CharField(verbose_name="Индикатор спец. обработки", max_length=15, choices=DELIVERANCE)

    contract = models.ForeignKey(Contract, verbose_name="Договор", on_delete=models.CASCADE, null=True)

    manager = models.ForeignKey(Manager, verbose_name="Менеджер", related_name='managers', on_delete=models.CASCADE,
                                null=True)
    manager_dispatch = models.ForeignKey(Manager, verbose_name="Менеджер поставки", related_name='dispatchers',
                                         on_delete=models.CASCADE, null=True)
    doc = models.PositiveIntegerField(verbose_name="Документ-образец")
    doc_position = models.SmallIntegerField(verbose_name="Позиция сделки")

    class Meta:
        unique_together = ('factura', 'doc_position')

    def save(self, *args, **kwargs):
        self.price = self.cost_boe * 1000 / self.amount if self.amount else None
        super(LuxData, self).save(*args, **kwargs)

