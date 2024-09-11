import mysql.connector
from mysql.connector import Error
import pandas as pd

df_State_1 = pd.read_csv(r".\\csv\\Andhra.csv")
df_State_2 = pd.read_csv(r".\\csv\\Bihar.csv")
df_State_3 = pd.read_csv(r".\\csv\\Himachal.csv")
df_State_4 = pd.read_csv(r".\\csv\\Kadamba.csv")
df_State_5 = pd.read_csv(r".\\csv\\Kerala.csv")
df_State_6 = pd.read_csv(r".\\csv\\Patiala and East Punjab.csv")
df_State_7 = pd.read_csv(r".\\csv\\Rajasthan.csv")
df_State_8 = pd.read_csv(r".\\csv\\South Bengal.csv")
df_State_9 = pd.read_csv(r".\\csv\\Telangana.csv")
df_State_10 = pd.read_csv(r".\\csv\\West Bengal Surface.csv")
final_df = pd.concat([df_State_1, df_State_2, df_State_3, df_State_4, df_State_5, df_State_6, df_State_7, df_State_8, df_State_9, df_State_10], ignore_index=True)



final_df.dropna(inplace=True)


print(final_df)

# Database
host = 'localhost'
user = 'root'
password = 'Redbus_2024'
database = 'redbus_db'
table_name = 'BusData'

# Table schema
table_schema = '''
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255) NOT NULL,
    Route VARCHAR(255) NOT NULL,
    URL VARCHAR(255) NOT NULL,
    Bus_Name VARCHAR(255) NOT NULL,
    Type VARCHAR(255) NOT NULL,
    Origin VARCHAR(255) NOT NULL,
    Departure VARCHAR(255) NOT NULL,
    Destination VARCHAR(255) NOT NULL,
    Arrival VARCHAR(255) NOT NULL,
    Duration VARCHAR(255) NOT NULL,
    Fare VARCHAR(255) NOT NULL,
    Seats VARCHAR(255) NOT NULL,
    Rating VARCHAR(255) NOT NULL    
'''

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin= 'mysql_native_password'
    )

    if connection.is_connected():
        cursor = connection.cursor()


        # Delete Existing table
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_query)
        connection.commit()
        print(f"Table '{table_name}' deleted successfully.")
            
        # Create New table
        cursor.execute(f"CREATE TABLE {table_name} ({table_schema})")
        print(f"Table '{table_name}' created successfully in database '{database}'.")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

try:
    # Read the CSV file
    df =final_df

    # Connect to MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin= 'mysql_native_password'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Create insert statement dynamically based on the dataframe columns
        cols = "`,`".join([str(i) for i in df.columns.tolist()])
        for i, row in df.iterrows():
            sql = f"INSERT INTO `{table_name}` (`{cols}`) VALUES ({'%s, ' * (len(row) - 1)}%s)"
            cursor.execute(sql, tuple(row))

        # Commit the transaction
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully into {table_name} table")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")