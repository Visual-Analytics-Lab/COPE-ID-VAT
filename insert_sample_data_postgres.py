import psycopg2
import pandas as pd
from configparser import ConfigParser


def config(filename="M:\\COPE-ID\\COPE-ID-VAT\\database.ini", section='postgresql'):
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

def connect(df, source, doc_text):
    """ Connect to the PostgreSQL database server """
    conn = None
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    
    # create a cursor
    cur = conn.cursor()
    
    # execute a statement
    for i in df.index:

        df_json = str(df.loc[i].to_json(orient = 'columns'))
        values = (df_json, source, df[doc_text][i])
        cur.execute("INSERT INTO main_sample_data (doc_json, doc_source, doc_text) VALUES (%s, %s, %s)",
                    values)
       
    conn.commit()
    print(f"Records created successfully for {source}\n")
    conn.close()

def format_data_for_insert(filename):
    print('formatting data...')
    df = pd.read_csv(filename, encoding="utf-8", nrows=250)
    sampled_df = df.head(100)

    return sampled_df

if __name__ == '__main__':
    source_config = ConfigParser()
    source_config.read('M:\\COPE-ID\\COPE-ID-VAT\\config.ini')

    for section in source_config.sections():
        filename = source_config[section]['filename'].replace("'", '')
        source = source_config[section]['source'].replace("'", '')
        doc_text_field = source_config[section]['doc_text'].replace("'", '')

        data = format_data_for_insert(filename)

        connect(data, source, doc_text_field)

