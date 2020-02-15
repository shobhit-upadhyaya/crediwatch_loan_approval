
from sqlalchemy import create_engine
import sqlalchemy as db

import pandas as pd

def save_data(df, database_filename, table_name):
    """
    Input:  dataframe
    Return: None
    Desc:
    Saves the input dataframe into database table. 
    You can do this with pandas.DataFrame.to_sql method combined with the SQLAlchemy library. 
    Remember to import SQLAlchemy's `create_engine`
    """
    engine = create_engine('sqlite:///'+database_filename)

    if not engine.dialect.has_table(engine, table_name):
        df.to_sql(table_name, engine, index=False)  

def create_table(database_filename, table_name):
    engine = create_engine('sqlite:///'+database_filename)
    if not engine.dialect.has_table(engine, table_name):

        connection = engine.connect()
        metadata = db.MetaData(engine)

        emp = db.Table(table_name, metadata,
                      db.Column('CIN', db.String(255)),
                      db.Column('Loan Amount', db.Float()),
                      db.Column('Interest Rate', db.Float()),
                      db.Column('Interest Rate', db.Float()),
                      db.Column('Loan tenure', db.Integer()),
                      db.Column('Monthly Income', db.Float()),
                      db.Column('Current Debt', db.Float()),
                      db.Column('debt_to_income_ratio', db.Float()),
                      db.Column('p_value', db.Float()),
                      db.Column('loan_request_status', db.Boolean())
                      )
        emp.create()


def insert_result(database_filename, table_name, row):
        engine = create_engine('sqlite:///'+database_filename)

        connection = engine.connect()
        metadata = db.MetaData(engine)

        emp = db.Table(table_name, metadata,
                      db.Column('CIN', db.String(255)),
                      db.Column('Loan Amount', db.Float()),
                      db.Column('Interest Rate', db.Float()),
                      db.Column('Interest Rate', db.Float()),
                      db.Column('Loan tenure', db.Integer()),
                      db.Column('Monthly Income', db.Float()),
                      db.Column('Current Debt', db.Float()),
                      db.Column('debt_to_income_ratio', db.Float()),
                      db.Column('p_value', db.Float()),
                      db.Column('loan_request_status', db.Boolean())
                      )    

        query = db.insert(emp) 
        values_list = [row]
        ResultProxy = connection.execute(query,values_list)


def load_data(database_filepath, table_name):
    '''
        Input: database_filepath
        return : df
        Desc:
            Creates sqlite engine.
            Reads the data of sql table and load it as dataframe.
            Load dataset from database by using read_sql_table()
    '''

    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table(table_name, engine)
    return df

def filter_df_cin(cin, database_filepath, table_name):
    df = load_data(database_filepath, table_name)
    print(df.columns)
    return df[df.CIN==cin].to_json()

def filter_df_cluster(cluster_number, database_filepath, table_name):
    df = load_data(database_filepath, table_name)
    print(df.shape)
    print(cluster_number[0])
    print("Exist clusters: ",df['OPTIMAL_CLUSTERS'].unique())
    mask = df['OPTIMAL_CLUSTERS'].apply(lambda x: x==cluster_number[0])
    print(sum(mask))
    df_filtered = df[mask]
    print(df_filtered.shape)
    return df_filtered #.to_json()


