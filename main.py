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

        crsr.execute("DROP TABLE IF EXISTS employee")

        create_script = """CREATE TABLE IF NOT EXISTS employee (
            id  int PRIMARY KEY,
            name    varchar(40) NOT NULL,
            salary int,
            dept_id varchar(30)
        )
        """
        crsr.execute(create_script)

        insert_script = "INSERT INTO employee(id,name,salary, dept_id) VALUES (%s,%s,%s,%s)"
        insert_value = [(1,"James",16000,'F1'),(2,"JoJo", 26000, 'D1'),(3, "Alan", 63000, "F1")]
        for record in insert_value:
            crsr.execute(insert_script, record)

        crsr.execute('SELECT * FROM employee')
        print(crsr.fetchall())

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