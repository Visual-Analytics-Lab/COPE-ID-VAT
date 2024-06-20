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

def connect(topic_name, doc_ids):
    """ Connect to the PostgreSQL database server """
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
    
    values = (topic_name, doc_ids)

    # execute a statement
    cur.execute('INSERT INTO main_bert_main_sample_data (topic_name, documents) VALUES (%s, %s)',
                    values)
       
    conn.commit()
    conn.close()

if __name__ == '__main__':
    data = pd.read_json('Bert_main_sample_data.json')
    for d in data.iterrows():
        topic = d[1][0][0].split('_')[1:]
        topic_str = ' '.join(topic)
        doc_ids = list(map(int, d[1]['Topics']))
        print('a')

        connect(topic_str, doc_ids)
