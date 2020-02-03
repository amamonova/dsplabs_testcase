from config import CONFIG

import sqlite3
import logging


logging.basicConfig(format=('%(asctime)s - %(name)s - '
                            '%(levelname)s - %(message)s'),
                    level=logging.INFO)
logger = logging.getLogger()


def create_db():
    """
    Function creates database
    :return: None
    """
    conn = sqlite3.connect(CONFIG['DATABASE_NAME'])
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS voice 
                          (uid text, audio_path text)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS photo
                          (uid text, photo_path text)""")
    conn.commit()

    close_conn(conn)


def create_conn():
    """
    Function creates connection to database.
    :return: connect and cursor.
    """

    conn = sqlite3.connect(CONFIG['DATABASE_NAME'])
    cursor = conn.cursor()

    conn.commit()

    return conn, cursor


def close_conn(conn):
    """
    Function closes connection to db.
    :param conn: connection to db
    :return: True
    """
    if conn:
        conn.close()
    return True


def check_user(cursor, id, table, field_name):
    """
    Function for selecting rows by user id.
    :param cursor:
    :param id: user id
    :param table: table name
    :param field_name: field name in the table
    :return: list of selected rows
    """
    cursor.execute(f"""SELECT {field_name} FROM {table}
                       WHERE uid={id}""")
    result = cursor.fetchall()

    if result:
        return result
    return []


def get_name(cursor, uid, table_name, field_name):
    """
    Function creates new name for file based on number of saved items in db.
    :param cursor:
    :param uid: user id
    :param table_name: table name
    :param field_name: field name in the table
    :return: filename with number
    """
    if table_name == 'voice':
        field_name = 'audio_path'
        name = 'audio_message'
    elif table_name == 'photo':
        field_name = 'photo_path'
        name = 'photo_message'

    flag = check_user(cursor, uid, table_name, field_name)

    return f'{uid}_{name}_{len(flag)}'


def insert_data(conn, cursor, table_name, uid, field_name, field_data):
    """
    Function insert data to the table.
    :param conn:
    :param cursor:
    :param table_name:
    :param uid: user id
    :param field_name: field name in the table
    :param field_data: inserting data
    :return: None
    """
    try:
        insert_query = f"""INSERT INTO {table_name}
                           (uid, {field_name}) VALUES (?, ?)"""

        data_tuple = (uid, field_data)
        cursor.execute(insert_query, data_tuple)
        conn.commit()

        logger.info(f'Data for user {uid} inserted successfully '
                    f'in {table_name} table')
    except sqlite3.Error as error:
        logger.info("Failed to insert data into sqlite table", error)

