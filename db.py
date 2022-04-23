import pickle
import sqlite3
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from driver.session import DriverSession
    from driver.session import DriverSessionStatus


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("db.sqlite3")
    except Exception as e:
        print(e)

    return conn


def save_number(session_id, order):
    CONNECTION = create_connection()

    CONNECTION.cursor().execute(
        """
        insert into number_orders values(?,?,?,?,?,?,?,?,?);
        """,
        [
            order["id"],
            order["phone"],
            order["operator"],
            order["price"],
            order["expires"],
            order['created_at'],
            order['country'],
            order['sms'],
            session_id
        ]
    )

    CONNECTION.commit()
    CONNECTION.close()


def save_session(sess: 'DriverSession'):
    with create_connection() as CONNECTION:
        CONNECTION.cursor().execute(
            """
            insert or ignore into sessions(step,status,cookies,id) values(?,?,?,?);
            """,
            [
                sess.step,
                sess.status,
                pickle.dumps(sess.driver.get_cookies()),
                sess.session_id
            ]
        )
        CONNECTION.cursor().execute(
            """
            update sessions set step = ?, status = ?, cookies = ? where id = ?
            """,
            [
                sess.step,
                sess.status,
                pickle.dumps(sess.driver.get_cookies()),
                sess.session_id,
                sess.status_history
            ]
        )

        CONNECTION.commit()


def retrieve_session_data(session_id) -> 'DriverSession':
    with create_connection() as CONNECTION:
        cur = CONNECTION.cursor()
        cur.execute(
            """
            select * from sessions where id = ? or 1 = 1 limit 1;
            """,
            [
                session_id
            ]
        )
        return cur.fetchone()


def retrieve_incomplete_sessions() -> 'DriverSession':
    with create_connection() as CONNECTION:
        cur = CONNECTION.cursor()
        cur.execute(
            """
            select * from sessions where status = ?;
            """,
            [
                'INCOMPLETE'
            ]
        )
        return cur.fetchone()


def get_all_accounts():
    with create_connection() as CONNECTION:
        cur = CONNECTION.cursor()
        cur.execute(
            """
            select * from accounts
            """,
        )
        return cur.fetchall()


def delete_all_accounts():
    with create_connection() as CONNECTION:
        cur = CONNECTION.cursor()
        cur.execute(
            """
            delete from accounts;
            """,
        )
        return cur.fetchone()


def save_account(email, phone, password):

    with create_connection() as CONNECTION:
        cur = CONNECTION.cursor()
        cur.execute(
            """
            insert into accounts values (?,?,?,?)
            """,
            [
                email,
                password,
                phone,
                int(time.time())
            ]
        )
        return cur.fetchone()
