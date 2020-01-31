import psycopg2
import DB_config

try:
    connection = psycopg2.connect(user = DB_config.user,
                                  password = DB_config.password,
                                  host = DB_config.host,
                                  port = DB_config.port,
                                  database = DB_config.database)
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    #print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT * FROM program;")
    record = cursor.fetchone()

    print(res)
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
