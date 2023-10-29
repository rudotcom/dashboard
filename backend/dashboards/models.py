import datetime
import pandas as pd
from django.contrib.postgres.fields import ArrayField
from django.db import models


class DataSource(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=100)
    # employee = models.Manager TODO добавить связь
    description = models.CharField(verbose_name="Описание", max_length=255, blank=True)
    date = models.DateField(verbose_name="Дата")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    csv = models.FileField(verbose_name="Файл", upload_to='csv')
    accrual = models.BooleanField(verbose_name="Календарное накопление данных", default=False)

    class Meta:
        verbose_name = "Источник данных"
        verbose_name_plural = "Источники данных"
        ordering = ['-created_at']

    def __str__(self):
        return ''.join([str(self.pk), '. ', self.name])

    def get_csv(self):
        table_class = 'table table-striped table-condensed table-fixed-header'
        df = pd.read_csv(self.csv.path, sep=';')
        return df.to_html(index=False, escape=False, classes=table_class)

    def age_badge(self):
        age = datetime.datetime.now(datetime.timezone.utc) - self.created_at
        minutes = age.seconds // 60
        print('m', self.id, self.created_at, minutes, age.days)

        if age.days > 0:  # 24 * 60
            badge = '<span class="badge bg-label-warning">Давно</span>'
        elif minutes < 5:
            badge = '<span class="badge bg-label-success">Новый</span>'
        elif minutes < 30:
            badge = '<span class="badge bg-label-info">Недавно</span>'
        else:
            badge = '<span class="badge bg-label-primary">Сегодня</span>'
        return badge


class ChartData(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=100)
    datasource = models.ForeignKey(DataSource, related_name="datasources", on_delete=models.PROTECT)
    columns = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    filter_columns = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    group_columns = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    user_filter_columns = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    # chart axes
    x_axis = models.CharField(verbose_name='Ось X', max_length=50)
    y_axis = models.CharField(verbose_name='Ось Y', max_length=50)

    class Meta:
        verbose_name = "Данные графика"
        verbose_name_plural = "Данные графиков"
        ordering = ['-pk']

    def __str__(self):
        return ''.join([str(self.pk), '. ', self.name])

    def df_filters(self, number_rows):
        df = pd.read_csv(self.datasource.csv.path, usecols=self.columns, sep=';')
        total = df[self.group_columns].sum().values[0]
        df['ratio_total'] = df[self.group_columns] / total * 100
        df['ratio_total'] = df['ratio_total'].astype('int')
        df = df.sort_values(by=self.group_columns, ascending=False).reset_index(drop=True).head(number_rows)
        top = df[self.group_columns].max().values[0]
        df['ratio_top'] = df[self.group_columns] / top * 100
        df['ratio_top'] = df['ratio_top'].astype('int')
        filters = {column: sorted(list(df[column].unique())) for column in self.filter_columns}
        return df, filters, total

    @classmethod
    def aggregate_table(cls, data_source_id: int, name: str, use_cols: list, group_columns: list):
        data_source = DataSource.objects.get(pk=data_source_id)
        chart_data = cls.objects.create(name=name, datasource=data_source)
        chart_data.columns = use_cols

        df = pd.read_csv(data_source.csv.path, usecols=use_cols, sep=';')
        df = df.dropna()
        columns = df.columns

        chart_data.group_columns = group_columns
        chart_data.filter_columns = [column for column in columns if column not in group_columns]

        chart_data.save()
        return chart_data

    def get_aggregated_data(self):
        # functions = ['sum', 'mean', 'median', 'min', 'max', 'std', 'var', 'prod', 'size', ]
        # text handling: ['nunique', mode, set]  # mode from scipy

        aggregation_columns = {column: ["min", "max", "sum", "mean"] for column in self.group_columns}

        df = pd.read_csv(self.datasource.csv.path, usecols=self.columns, sep=';')
        df = df.loc[(df[self.group_columns] != 0).all(axis=1)]

        columns = [column for column in self.columns if column not in self.group_columns]

        filter_columns = {column: sorted(list(df[column].unique())) for column in columns}

        grouped = df.groupby(columns, as_index=False)
        # aggregated = grouped.agg(aggregation_columns).round(2)
        return *grouped, filter_columns


class Dashboard(models.Model):
    ...


class FAQSection(models.Model):
    name = models.CharField(verbose_name="Раздел", max_length=100)
    icon = models.CharField(verbose_name="Иконка", max_length=100)
    description = models.CharField(verbose_name="Описание", max_length=255)


class FAQ(models.Model):
    class Meta:
        verbose_name = "Вопрос-Ответ"
        verbose_name_plural = "Вопросы-Ответы"
        ordering = ['-pk']

    section = models.ForeignKey(FAQSection, related_name="sections", on_delete=models.PROTECT)
    question = models.CharField(verbose_name="Вопрос", max_length=255)
    answer = models.TextField(verbose_name="Ответ")
    date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
