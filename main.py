import psycopg2
from config import config


def connect():
    connection = None
    try:
        params = config()
        print("Connecting to postgreSQL database...")
        connection = psycopg2.connect(**params)

        crsr = connection.cursor()
        print("PostgreSQL database version: ")
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        create_script = """CREATE TABLE IF NOT EXISTS employee (
            id  int PRIMARY KEY,
            name    varchar(40) NOT NULL,
            salary int,
            dept_id varchar(30)
        )
        """
        crsr.execute(create_script)

        insert_script = "INSERT INTO employee(id,name,salary, dept_id) VALUES (%s,%s,%s,%s)"
        insert_value = (2,"Dany", 16000, 'G1')
        crsr.execute(insert_script, insert_value)

        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminated")

if __name__ == "__main__":
    connect()