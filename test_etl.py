import pandas as pd
from etl import transform


def test_column_names_lowercased():
    sample_data = [{'FirstName': 'John', 'LastName': 'Does'}]
    df = transform(sample_data)
    assert list(df.columns) == ['firstname', 'lastname']


def test_strip_blank_spaces():
    sample_data = [{'first name': 'john', 'last name': 'does'}]
    df = transform(sample_data)
    assert list(df.columns) == ['first_name', 'last_name']
