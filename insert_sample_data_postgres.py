import psycopg2
import pandas as pd
from configparser import ConfigParser
from sqlalchemy import create_engine

def config(filename="database.ini", section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# def connect(df, source, doc_text):
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     # read connection parameters
#     params = config()

#     # connect to the PostgreSQL server
#     print('Connecting to the PostgreSQL database...')
#     conn = psycopg2.connect(**params)
    
#     # create a cursor
#     cur = conn.cursor()
    
#     # execute a statement
#     for i in df.index:

#         df_json = str(df.loc[i].to_json(orient = 'columns'))
#         values = (df_json, source, df[doc_text][i])
#         cur.execute("INSERT INTO main_sample_data (doc_json, doc_source, doc_text) VALUES (%s, %s, %s)",
#                     values)
       
#     conn.commit()
#     print(f"Records created successfully for {source}\n")
#     conn.close()

def connect(id, doc_json, doc_source, doc_text):
    """ Connect to the PostgreSQL database server """
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
    
    values = (id, doc_json, doc_source, doc_text)

    # execute a statement
    cur.execute("INSERT INTO test_main_sample_data (id, doc_json, doc_source, doc_text) VALUES (%s, %s, %s, %s)",
                    values)
       
    conn.commit()
    conn.close()

if __name__ == '__main__':
        data = pd.read_json('/home/shared/data/test_main_sample_data.json')
        for d in data.iterrows():
             doc_json = d[1]['doc_json']
             doc_source = d[1]['doc_source']
             doc_text = d[1]['doc_text']
             id = d[1]['id']
             print ('a')

             connect(id, doc_json, doc_source, doc_text)

        #connect(data, source, doc_text_field)

