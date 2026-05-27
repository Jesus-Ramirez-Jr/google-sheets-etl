import pandas as pd
from etl import transform


def test_column_names_lowercased():
    sample_data = [{'First Name': 'John', 'Last Name': 'Does'}]
    df = transform(sample_data)
    assert list(df.columns) == ['first_name', 'last_name']


def test_strip_blank_spaces():
    sample_data = [{'first name': 'john', 'last name': 'does'}]
    df = transform(sample_data)
    assert list(df.columns) == ['first_name', 'last_name']
