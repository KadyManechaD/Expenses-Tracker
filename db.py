import sqlite3


class ExpensesDb:

    def __init__(self):
        self.mydb = sqlite3.connect("expenses.db")
        self.mycursor = self.mydb.cursor()

    def setup(self):
        self.create_table_categories()
        self.create_table_expenses()
        self.seed_categories()


    def seed_categories(self):
        categories = [
            "Bills",
            "Rent",
            "Groceries",
            "Emergencies",
            "Shopping",
            "Subscriptions",
            "Entertainment",
            "Dining out",
            "Phone and Internet",
            "Unexpected Expenses",
            "Others",
        ]

        for category in categories:
            self.mycursor.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (category,)
            )

        self.mydb.commit()
        
    
    def create_table_categories(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        self.mydb.commit()

        print("Categories table created!")

    def create_table_expenses(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                price REAL NOT NULL,
                date TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        self.mydb.commit()

        print("Expenses table created!")

    def add_category(self, name):
        sql = "INSERT INTO categories (name) VALUES (?)"

        self.mycursor.execute(sql, (name,))
        self.mydb.commit()

    def add_expense(self, description, price, date, category_id):
        sql = """
            INSERT INTO expenses
                (description, price, date, category_id)
            VALUES (?, ?, ?, ?)
        """

        self.mycursor.execute(
            sql,
            (description, price, date, category_id)
        )

        self.mydb.commit()

    def get_categories(self):
        self.mycursor.execute("""
            SELECT id, name
            FROM categories
            ORDER BY name
        """)

        return self.mycursor.fetchall()

    def get_expenses(self):
        self.mycursor.execute("""
            SELECT
                expenses.id,
                expenses.description,
                expenses.price,
                expenses.date,
                categories.name
            FROM expenses
            JOIN categories
                ON expenses.category_id = categories.id
            ORDER BY expenses.date DESC
        """)

        return self.mycursor.fetchall()