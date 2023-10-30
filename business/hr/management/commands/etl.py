from datetime import date, timedelta
import math
import pandas as pd

from sqlalchemy import create_engine
from django.core.management.base import BaseCommand

from hr.models import Industry, Employee
from hr.constants import (
    MAXIMUM_AGE,
    MINIMUM_WORKING_AGE
)


class _Transformer:
    def __init__(self, df):
        self.df = df
        
    def run(self):
        self._drop_irrelevant_columns()
        self._rename_columns()
        self._convert_dates()
        self._drop_na_for_annual_income_and_yoe()
        self._convert_from_float_to_int()
        self._drop_unrealistic_employees()
        self._replace_nas_for_industry()
        self._convert_dob_to_date()
        
        return self._create_and_industry_df_employee_df()
        
    def _drop_irrelevant_columns(self):
        self.df.drop(['email'], axis=1, inplace=True)

    def _rename_columns(self):
        renamed_columns = {
            'years_of_experience': 'yoe',
            'date_of_birth': 'dob',
            'salary': 'annual_income'
        }
        
        self.df.rename(columns=renamed_columns, inplace=True)

    def _convert_dates(self):        
        self.df['dob'] = pd.to_datetime(self.df['dob'], format='%d/%m/%Y')
            
    def _drop_na_for_annual_income_and_yoe(self):
        self.df = pd.DataFrame(self.df[self.df['annual_income'].notna()])
        self.df = pd.DataFrame(self.df[self.df['yoe'].notna()])
        
    def _convert_from_float_to_int(self):
        self.df['annual_income'] = self.df['annual_income'].astype(int)
        self.df['yoe'] = self.df['yoe'].astype(int)
    
    def _drop_unrealistic_employees(self):
        self._compute_age()
        
        self._drop_over_70_years_old_employees()
        self._drop_employees_who_worked_before_18_years_old()
        
        self._drop_age()
    
    def _compute_age(self):
        self.df['age'] = (date.today() - self.df['dob'].dt.date) / timedelta(days=365)
        self.df['age'] = self.df['age'].astype(int)
    
    def _drop_over_70_years_old_employees(self):
        self.df = pd.DataFrame(self.df[self.df['age'] <= MAXIMUM_AGE])
        
    def _drop_employees_who_worked_before_18_years_old(self):
        self.df = pd.DataFrame(self.df[self.df['age'] - self.df['yoe'] >= MINIMUM_WORKING_AGE])
        
    def _drop_age(self):
        self.df.drop(['age'], axis=1, inplace=True)
    
    def _replace_nas_for_industry(self):
        self.df['industry'].replace(to_replace='n/a', value=None, inplace=True)
    
    def _convert_dob_to_date(self):
        self.df['dob'] = self.df['dob'].dt.date
    
    def _create_and_industry_df_employee_df(self):
        industries = self.df['industry'].dropna().drop_duplicates()
        industry_df = pd.DataFrame({
            'id': range(1, industries.count() + 1),
            'name': industries
        })
        
        employee_df = self.df.replace(to_replace=list(industry_df['name']), value=list(industry_df['id']))
        employee_df['industry'] = employee_df['industry'].astype('Int64')
        renamed_column = {
            'industry': 'industry_id',
        }
        employee_df.rename(columns=renamed_column, inplace=True)
        
        return industry_df, employee_df

class _Etl:
    def __init__(self, path):
        self.path = path
    
    def extract(self):
        self.df = pd.read_json(self.path)

    def transform(self):
        transformer = _Transformer(self.df)
        self.industry_df, self.employee_df = transformer.run()
        
    def load(self):
        engine = create_engine('sqlite:///db.sqlite3')
        
        self.industry_df.to_sql(Industry._meta.db_table, if_exists='replace', con=engine, index=False)
        self.employee_df.to_sql(Employee._meta.db_table, if_exists='replace', con=engine, index=False)


class Command(BaseCommand):
    help = "A command to add data from a specific JSON file, i.e. MOCK_DATA.json"
    
    def handle(self, *args, path='hr/data/MOCK_DATA.json', **options):

        etl = _Etl(path)

        etl.extract()
        etl.transform()
        etl.load()
