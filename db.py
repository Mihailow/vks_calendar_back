import json

import psycopg2
import psycopg2.extras

DB_HOST = "localhost"
DB_NAME = "vks_main"
DB_USER = "postgres"
DB_PASS = "postgres"

def postgres_do_query(query: object, params: object) -> object:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    try:
        results = cursor.fetchall()
    except:
        results = None
    conn.commit()
    cursor.close()
    conn.close()
    return results


def postgres_select_one(query, params):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        result = dict(result)
    conn.commit()
    cursor.close()
    conn.close()

    return result


def postgres_select_all(query, params):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    results = cursor.fetchall()
    if results:
        res = []
        for r in results:
            res.append(dict(r))
        results = res
    conn.commit()
    cursor.close()
    conn.close()
    return results


def get_month_info(month, year):
    first_date = f"01.{month}.{year}"
    if month+1 == 13:
        second_date = f"01.{1}.{year+1}"
    else:
        second_date = f"01.{month+1}.{year}"
    info = postgres_select_all("SELECT to_char(day, 'DD.MM.YYYY') AS date, info FROM calendar WHERE day >= %s AND day < %s ORDER by date;",
                               (first_date, second_date,))
    return info


def insert_date_info(date, info):
    day = postgres_select_one("SELECT * FROM calendar WHERE day = %s;",
                              (date,))
    if day:
        postgres_do_query("UPDATE calendar SET info = %s WHERE day = %s;",
                          (json.dumps(info), date,))
    else:
        postgres_do_query("INSERT INTO calendar VALUES(%s, %s);",
                          (date, json.dumps(info),))
