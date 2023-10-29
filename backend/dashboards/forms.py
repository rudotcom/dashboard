from datetime import datetime, date

from django import forms
from .models import DataSource, ChartData


class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = ['name', 'description', 'csv', 'date', 'accrual']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название источника данных'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Краткое описание источника данных'}),
            'csv': forms.FileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date',
                                           'value': str(date.today()), 'id': 'html5-date-input'}),
            'accrual': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'id': 'flexSwitchCheckChecked', 'checked': ''})
        }


class DataChartForm(forms.ModelForm):
    class Meta:
        model = ChartData
        fields = ['name', 'filter_columns', 'group_columns', 'columns', 'user_filter_columns', 'x_axis', 'y_axis']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название графика'}),
            'filter_columns': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'group_columns': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'columns': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'user_filter_columns': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'x_axis': forms.Select(attrs={'class': 'form-select'}),
            'y_axis': forms.Select(attrs={'class': 'form-select'})
        }
