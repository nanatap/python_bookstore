"""Desktop application storing the book database. It has 5 main functions,

1) View all books in the database,
2)select desired row and modify the book information,
3) Add new book,
4) Search for the specific book
(it has an exact search, meaning that, you need to input at least one full parameter: full name of the book,
full author name or just a year or publication).
5) Selected book row can be deleted from DB.

Finally, as all of the other applications, this program has the termination function.
Overall, program has two main files, Front-end (with Tkinter GUI) and the back-end with SQLlite3 DB.
Back-end creates Books table, has five main functions that supports front-end. Front-end itself contains: Main imports,
One class called: BookStore, GUI details (creating frame, rows, buttons and input fields), and functions that define the
whole application.
NOTE: Table data is displayed ASC for Book titles.
You can find more detailed explanations for each function inline."""

from doctest import master
from tkinter import *
from tkinter import ttk
import BooksDataBase

con, cursor = BooksDataBase.init()


def close_application():
    cursor.close()
    exit()


class BookStore(Frame):
    entryExample = None

    def __init__(self, top):
        """Creating Frame, it's rows and columns, with entry names, inputs and buttons"""

        super().__init__()
        top.geometry('1300x500')
        self.master.config(bg="#e6f7ff")
        Label(master, text="Title").grid(row=0)
        Label(master, text="Author").grid(row=1)

        self.e1 = Entry(master, width=90)
        self.e2 = Entry(master, width=90)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        Label(master, text="ISBN").grid(row=2)
        Label(master, text="year").grid(row=3)

        self.e3 = Entry(master, width=90)
        self.e4 = Entry(master, width=90)

        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        self.table = ttk.Treeview(top, columns=('Id', 'name', 'author', 'code', 'year'))
        self.table['show'] = 'headings'
        self.table.heading("Id", text="Id")
        self.table.heading("name", text="Name")
        self.table.heading("author", text="Author")
        self.table.heading("code", text="ISBN")
        self.table.heading("year", text="year")
        self.table.grid(row=6, column=1)
        self.table.bind("<ButtonRelease-1>", self.on_click)

        view_all = Button(top, text="View all", bg="black", width=12, command=self.view_all_books)
        view_all.grid(row=0, column=5, padx=10)
        search_entry = Button(top, text="Search entry", bg="black", width=12, command=self.search)
        search_entry.grid(row=1, column=5)
        add_entry = Button(top, text="Add entry", bg="black", width=12, command=self.add_entry)
        add_entry.grid(row=2, column=5)
        update_selected = Button(top, text="Update selected", bg="black", width=12, command=self.update_selected)
        update_selected.grid(row=3, column=5)
        delete_selected = Button(top, text="Delete selected", bg="black", width=12, command=self.delete_selected)
        delete_selected.grid(row=4, column=5)
        close_button = Button(top, text="Close", bg="black", width=12, command=close_application)
        close_button.grid(row=5, column=5)

        top.mainloop()

    def view_all_books(self):
        """Firstly, function Clears the table (in case there is previous data in it),
        then displays all the books from BooksDataBase. (Data is sorted ASC according to book's names"""
        self.table.delete(*self.table.get_children())
        for row in cursor.execute("SELECT * FROM books ORDER BY title ASC"):
            self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    def on_click(self, event):
        """On_click function is responsible for selecting the row and displaying it in the header, where user can modify
        the selected book data. At first function is clearing all the fields in the header,
        then it inserts the data line by line for each column"""
        item = self.table.selection()[0]
        self.clear(self.e1)
        self.clear(self.e2)
        self.clear(self.e3)
        self.clear(self.e4)
        self.e1.insert(0, self.table.item(item)["values"][1])
        self.e2.insert(0, self.table.item(item)["values"][2])
        self.e3.insert(0, self.table.item(item)["values"][3])
        self.e4.insert(0, self.table.item(item)["values"][4])

    @staticmethod
    def clear(entry):
        entry.delete(0, len(entry.get()))

    def delete_selected(self):
        """Easy delete function. Function deletes the selected row and at the end it calls the view_all_books
        functions to display the refreshed data automatically, without clicking any extra buttons."""
        item = self.table.selection()[0]
        BooksDataBase.delete_row(cursor, str(self.table.item(item)["values"][0]))
        self.view_all_books()

    def search(self):
        """Search function can find the book information, if the user specifies at least one field: Full name,
        Full author's name, year or ISBN code. If user does not specify year or ISBN code, function automatically
         assigns the value to TRUE"""
        self.table.delete(*self.table.get_children())
        name = self.e1.get()
        author = self.e2.get()
        isbn = self.e3.get()
        if isbn == "":
            isbn = '%'
        else:
            isbn = int(isbn)
        year = self.e4.get()
        if year == "":
            year = '%'
        else:
            year = int(year)

        rows = BooksDataBase.search(cursor, name, author, isbn, year)
        for row in rows:
            self.table.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    def add_entry(self):
        """Function adds new entry to the books database, in order to add new entry user needs to input alphanumeric
        book name and author's name. As soon as All the values are entered
        correctly, add_entry button adds new row to the database and updates the table automatically.
        Meanwhile, in the back-end as new entry is added to the DB, it automatically gives the new ID to the product.
        (ID Auto incrementation)"""
        if self.is_input_valid():
            e1_value = self.e1.get()
            e2_value = self.e2.get()
            e3_value = self.e3.get()
            e4_value = self.e4.get()
            BooksDataBase.insert(cursor, e1_value, e2_value, str(e3_value), str(e4_value))
            self.view_all_books()

    def update_selected(self):
        """Finally, update_selected function is responsible for the selected product changes. BooksDataBase file
        has the functions called update_entry which Sets new values depending on ID. Update_selected uses the back-end
        function to set new values to the selected product and refreshes the table."""
        item = self.table.selection()[0]
        if self.is_input_valid():
            BooksDataBase.update_entry(cursor, self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(),
                                       self.table.item(item)["values"][0])
        self.view_all_books()

    def is_input_valid(self):
        e1_value = self.e1.get()
        e2_value = self.e2.get()
        try:
            if not str(e2_value).replace(" ", "").isalpha() or not str(e1_value).replace(" ", "").isalnum():
                raise ValueError("Value is not alphanumeric")
            int(self.e3.get())
            int(self.e4.get())
            return True
        except ValueError as e:
            print("ValueError: " + str(e))
            return False


def main():
    top = Tk()
    BookStore(top)
    top.mainloop()


if __name__ == '__main__':
    main()
