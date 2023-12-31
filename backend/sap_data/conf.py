import pandas as pd


SECTOR_AMOUNT = (
    ('big', 'Крупный'),
    ('small', 'Малый'),
    ('middle', 'Средний'),
)
SECTOR_CRITERIA = {
    'big': 100_000,
    'middle': 30_000,
}

MONTH_SHORT = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

FACTURA_CLASS = (
    ('F2', 'Счет-фактура'),
    ('F3', 'Счет-фактура/ЦенаПст'),
    ('G2', 'Кредитовое авизо'),
    ('ISP', 'Исправ. сч.фактура'),
    ('L2', 'Дебетовое авизо'),
    ('RE', 'КредитованВозвратов'),
    ('S1', 'Сторно счета-фактуры'),
    ('S2', 'Сторно возврата'),
)
FACTURA_TYPE = (
    ('A', 'Фактура со ссылкой на заказ'),
    ('L', 'Фактура на основе поставок'),
)

SALES_CHANNEL = (
    ('10', 'Внутренний рынок'),
    ('20', 'Экспорт'),
)
SALES_DEPT = (
    ('2000', 'Отдел продаж'),
    ('2500', 'ОМТС'),
)
SALES_GROUP = (
    ('101', 'Реал. ГП на ВнутрРын'),
    ('102', '102'),
    ('103', 'Прочая реализация'),
)
SALES_DOCU_TYPE = (
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('S', 'S'),
)
SITE = (
    ('2001', 'Подольск'),
    ('2002', 'Истра'),
    ('2004', 'Воронеж'),
    ('2005', 'Ульяновск'),
)
WAREHOUSE = (
    ('1001', 'Склад Готовой Продукции'),
    ('5002', 'Инвентарный склад'),
)
SHIPMENT_CLASS = (
    ('LF', 'LF'),
    ('ZLD', 'ZLD'),
    ('ZLE', 'ZLE'),
    ('ZLF', 'ZLF'),
)
DOCUMENT = (
    ('invoice', 'Счет'),
    ('debit_note', 'Дебетовое авизо'),
    ('credit_note', 'Кредитовое авизо'),
    ('reversal', 'Сторно счета-фактуры'),
)
COUNTRY = (
    ('Россия', 'Россия'),
    ('Беларусь', 'Беларусь'),
)
VEHICLE_TYPE = (
    ('0001', 'Автомашина'),
    ('0011', 'Контейнер/автомашина'),
)
CURRENCY = (
    ('USD', 'Доллар'),
    ('EUR', 'Евро'),
    ('RUR', 'Российский рубль'),
    ('BYR', 'Белорусский рубль'),
)
PRICE_UNIT = (
    ('1', 1),
    ('1000', 1000),
)
WEIGHT_UNIT = (
    ('kg', 'кг'),
    ('t', 'т'),
)
SHIPPER = (
    ('2100', 'Ф-л Подольск Архбум'),
    ('2200', 'Ф-л Истра Архбум'),
    ('2400', 'Ф-л Воронеж Архбум'),
    ('2500', 'Ф-л Ульяновск Архбум'),
)
SALE_UNIT = (
    ('m2', 'М2'),
    ('tpc', 'ТШТ'),
    ('pc', 'ШТ'),
)
DELIVERANCE = (
    ('customer', 'Перевозка собственным транспортом'),
)

LUX_DATA_COLUMNS = (
    ('factura', 'Фактура', int),
    ('factura_date', 'Дата фактуры', pd.Timestamp),
    ('factura_class', 'Вид фактуры', str),
    ('factura_type', 'Тип фактуры', str),
    ('sales_channel', 'Канал сбыта', str),
    ('sales_dept', 'Отдел сбыта', str),
    ('sales_group', 'Группа сбыта', str),
    ('sales_docu_type', 'Тип документа сбыта', str),
    ('warehouse', 'Склад', int),
    ('shipment', 'Поставка', int),
    ('shipment_class', 'Вид поставки', str),
    ('date_fact', 'Дата ФактДвиженМтр', pd.Timestamp),
    ('date_created', 'Дата создания', pd.Timestamp),
    ('created_by', 'Создал', str),
    ('country', 'Страна получатель', str),
    ('short_text', 'Краткий текст позиции заказа клиента', str),

    ('currency', 'ВалютаДокумента', str),
    ('price_doc', 'Цена в валюте документа', float),
    ('price_derived', 'Цена расч.', float),
    ('price_usd', 'Цена в USD', float),
    ('price_unit', 'Единица цены', str),
    ('cost_net', 'Стоимость нетто', float),
    ('cost', 'Сумма в рублях на дату фактуры', float),
    ('cost_boe', 'Сумма в рублях на дату ГТД', float),
    ('vat', 'Сумма налога', float),
    ('cost_vat', 'Сумма с НДС', float),
    ('cost_usd', 'Стоимость в валюте', float),
    ('cost_gross', 'Стоимость в внутренней валюте', float),

    ('shipper', 'Пункт отгрузки/приемки', int),
    ('amount', 'ФактурКолич в СЕИ', float),  # Sales amount
    ('weight_net', 'Вес нетто', float),
    ('weight_gross', 'Вес брутто', float),
    ('weight_unit', 'ЕИ веса', str),
    ('number', 'Кол-во в ед. продажи', float),
    ('sale_unit', 'ЕИ продажи', str),
    ('city', 'Город', str),
    ('street', 'Улица', str),

    ('doc', 'Документ-образец', int),
    ('doc_position', 'ОбразецПозицСделки', int),
    ('site', 'Завод', int),
)
LUX_DATA_FOREIGN_COLUMNS = (
    ('site_name', 'Название завод', int),
    ('customer', 'Заказчик', int),  # SAP ID
    ('customer_name', 'Наименование заказчика', str),
    ('recipient', 'Получатель материала', int),
    ('recipient_name', 'Наименование получателя материала', str),
    ('payer', 'Плательщик', int),
    ('payer_name', 'Наименование плательщика', str),
    ('address_customer', 'Адрес Заказчика', str),
    ('address_recipient', 'Адрес Получателя', str),
    ('address_delivery', 'Адрес Доставки', str),
    ('region', 'Регион', int),
    ('region_name', 'Наименование регион', str),

    ('material', 'Материал', int),
    ('material_name', 'Наименование материала', str),
    ('material_group', 'Группа материалов', str),
    ('material_class', 'Вид материала', str),
    ('material_class_name', 'Наименование вида материала', str),
    ('material_group_name', 'Наименование группы материалов', str),

    ('vehicle_make', 'Марка транспортного средства', str),
    ('vehicle_number_plate', 'Регистрационный номер ТС', str),
    ('vehicle_type', 'Вид ТранспСредства', int),

    ('deliverance', 'Наименования индикатора спец. обработки', str),
    ('contract', '№ Контракта', str),
    ('contract_date', 'Дата контракта', pd.Timestamp),

    ('manager', 'Ответственный менеджер', str),
    ('manager_dispatch', 'Отгр. менеджер', str),
)

COMPANY_FORMS = [
    'ФИЛИАЛ',
    'ОБОСОБЛЕННОЕ ПОДРАЗДЕЛЕНИЕ', 'ОП',
    'ООО',
    'ЗАО',
    'ОАО',
    'ИП',
    'ПАО',
    'СПО',
    'ЧП',
    'ИПО',
    'СП',
    'АО',
    'АКЦИОНЕРНОЕ ОБЩЕСТВО',
    'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ',
    'ГРУППА КОМПАНИЙ',
    'ФИРМА',
    'ПКО', 'ПКФ', 'ПК', 'НПК', 'НПП', 'НПМК', 'НПФ', 'ПО', 'ПРОИЗВОДСТВЕННАЯ КОМПАНИЯ',
    'ПРОИЗВОДСТВЕННОЕ ПРЕДПРИЯТИЕ',
    'ПРЕДПРИЯТИЕ',
    'КФХ', 'КФ', 'КОНДИТЕРСКАЯ ФАБРИКА', 'КОНДИТЕРСКИЙ КОНЦЕРН',
    'КОМПАНИЯ',
    'ОБОСОБЛЕННОЕ СТРУКТУРНОЕ ПОДРАЗДЕЛЕНИЕ',
    'УК',
    'МГК', 'ГК',
    'ТК',
    'ТОРГОВЫЙ ДОМ', 'ТД',
]
