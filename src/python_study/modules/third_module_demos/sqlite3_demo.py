import sqlite3


def init():
    connect = sqlite3.connect("demo.db")
    cursor = connect.cursor()
    cursor.execute("create table user (id varchar(20) primary key, name varchar(20))")
    cursor.execute("insert into user (id, name) values ('1', 'Michael')")
    print("----- cursor.rowcount -----", cursor.rowcount)
    connect.commit()
    cursor.close()
    connect.close()


def main() -> None:
    init()
    pass
