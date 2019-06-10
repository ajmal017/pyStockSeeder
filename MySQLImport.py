import json
import pymysql
import pandas as pd
import sqlalchemy


try:
    with open('config.json') as config:
        cfg = json.load(config)
except:
    print("You must create a config.json file. An example file is provided: example-config.json")
    print("Edit the file and change the name to config.json")
    exit(0)

connection = pymysql.connect(host=cfg["MySQL"]["host"],
                             user=cfg["MySQL"]["user"],
                             password=cfg["MySQL"]["password"],
                             db=cfg["MySQL"]["db"],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def SQLInsertHistory(file):
        # creates table and inserts complete stock history file into the table
        df = pd.read_csv(file)
        cols = ["Open", "High", "Low", "Close", "Adjusted_close", "Volume"]
        df[cols].apply(pd.to_numeric, errors='coerce')
        df["Date"] = pd.to_datetime(df['Date'])

        database_username = cfg["MySQL"]["user"]
        database_password = cfg["MySQL"]["password"]
        database_ip = cfg["MySQL"]["host"]
        database_name = cfg["MySQL"]["db"]
        database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                       format(database_username, database_password,
                                                              database_ip, database_name,
                                                              auth_plugin='mysql_native_password'))

        df.to_sql(con=database_connection, name=cfg["DBTables"]["history"], if_exists='replace')


def SQLInsertStockfile(file):
    # creates table and inserts the stock profile info into a table
    df = pd.read_csv(file)
    df["marketcap"].apply(pd.to_numeric, errors='coerce')

    database_username = cfg["MySQL"]["user"]
    database_password = cfg["MySQL"]["password"]
    database_ip = cfg["MySQL"]["host"]
    database_name = cfg["MySQL"]["db"]
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password,
                                                          database_ip, database_name,
                                                          auth_plugin='mysql_native_password'))

    df.to_sql(con=database_connection, name=cfg["DBTables"]["stocks"], if_exists='replace')


def main():
    # this is the first iteration but a second condition will be made
    # in which stock history updates can be made and added to the history
    # additionally, another condition will be made that permits adding more
    # stock profile symbols
    SQLInsertStockfile(cfg["writeseeder"])
    SQLInsertHistory(cfg["allHistory"])


main()
