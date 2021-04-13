import sqlite3


def init():
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE books
                 (id INTEGER PRIMARY KEY, title, author, isbn, year)''')
    cur.execute("INSERT INTO books VALUES (NULL, 'No country for old man','Cormac Mccarthy', 9780307277039, 2006)")
    cur.execute("INSERT INTO books VALUES (NULL, 'The Picture of Dorian Gray','Oscar Wilde', 9780679432104, 1994)")
    cur.execute("INSERT INTO books VALUES (NULL, 'Journey to Ixtlan','Carlos Castaneda', 9780140192346, 1998)")
    cur.execute("INSERT INTO books VALUES (NULL, 'Mysteries','Knut Hamsun', 9780141186184, 2001)")
    cur.execute("INSERT INTO books VALUES (NULL, 'Buddenbrooks','Thomas Mann', 9783538053656, 1995)")
    conn.commit()
    return conn, cur


def insert(cur, name, author, isbn, year):
    cur.execute("INSERT INTO books VALUES (NULL, '" + name + "','" + author + "'," + isbn + "," +
                year + ")")


def delete_row(cur, id):
    cur.execute("DELETE FROM books WHERE id = " + id)


def search(cur, name, author, isbn, year):
    cur.execute("SELECT * FROM books WHERE title = ? OR author = ? OR isbn = ? OR year = ? ORDER BY title ASC",
                (name, author, isbn, year))
    rows = cur.fetchall()
    return rows


def update_entry(cur, name, author, isbn, year, id):
    cur.execute("UPDATE books SET title=?, author=?, isbn=?, year=? WHERE id=?", (name, author, isbn, year, id))


def close(conn):
    conn.close()
