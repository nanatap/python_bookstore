# python_bookstore
Desktop application storing the book database. It has 5 main functions,

1) View all books in the database,   
2) select desired row and modify the book information,
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
You can find more detailed explanations for each function inline.
