import os

import pandas as pd
from django.core.files.base import ContentFile
from django.shortcuts import render
from openpyxl import load_workbook

from dashboards.models import DataSource


def handle_uploaded_file(instance, file):
    # Load the XLSX file using openpyxl
    workbook = load_workbook(file, read_only=True)
    os.unlink(instance.csv.path)
    sheet = workbook.active

    # Convert the XLSX data to a pandas DataFrame
    data = sheet.values
    columns = next(data)
    df = pd.DataFrame(data, columns=columns)
    df.dropna(how='all', axis=1, inplace=True)

    # Convert the DataFrame to CSV
    csv_data = df.to_csv(index=False, sep=';', decimal='.', float_format='%.5f').encode('utf-8')

    # Save the CSV data to the DataSource model
    instance.csv.save(''.join([str(instance.pk), '_', instance.name, '.csv']), ContentFile(csv_data))
    instance.save()


def create_chart_data(data_source_id, columns, filter_columns, group_columns: dict, user_filter_columns, x_axis, y_axis):
    # group_columns = {'column1': 'sum', 'column2': 'mean'}
    data = DataSource.objects.get(pk=data_source_id)
    df = pd.read_csv(data.csv)
    df = df[columns]
    df = df.dropna()
    # specify grouping columns and aggregation functions
    df.groupby(group_columns).agg()
    df = df.reset_index()

