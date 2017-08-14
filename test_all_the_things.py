import os
import json
import psycopg2


from random import randint, choice
from string import ascii_lowercase

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'amazing_password'


def test_database():
    """Tests if we can actually talk to the CircleCI PostgreS instance"""
    conn = psycopg2.connect(host=DB_HOST,
                            port=DB_PORT,
                            dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS)

    cur = conn.cursor()

    # Create table
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

    # Bung in some random data
    for entry in range(10):
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s);",
                    (randint(0, 1000), _randstr()))

    # Read back everything we just inserted.
    cur.execute("SELECT * FROM test;")
    data = cur.fetchall()
    print(json.dumps(data, indent=4, sort_keys=True))

    conn.commit()
    cur.close()
    conn.close()


def test_explore_circle_ci_environment():
    print("Current working directory is: {}".format(os.getcwd()))
    print("\nEnvironment: {}".format(os.environ))


def _randstr(len=6):
    return "".join([choice(ascii_lowercase) for i in range(len)])
