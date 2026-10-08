from datetime import datetime
from rich.prompt import Prompt , FloatPrompt
import questionary
import sys
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

from db import ExpensesDb

console = Console()

expensesDb = ExpensesDb()

expensesDb.setup()


depenses = [
        { "description" : "je ne sais pas ", "date" : "2026-15-25" , "price" : 500 , "category_id" : 2}
    ] # [{ description, date , price , category}]


categories = [
    {"id" : 1 ,"name" : "Bills"},
    {"id" : 2 ,"name" : "Rent"},
    {"name" : "Groceries"} ,
    {"name" : "Emergencies"},
    {"name" : "Shopping"},
    {"name" : "Subscriptions"},
    {"name" : "Entertainment"},
    {"name" : "Dining out"},
    {"name" : "Phone and Internet"},
    {"name" : "Unexpected Expenses"},
    {"name" : "Others"},
]


def show_header():
    title = Text()
    title.append("EXPENSE " , style="bold cyan")
    title.append("TRACKER" , style="bold white")
    
    subtitle = Text("\nPersonnal finance manager",
        style="dim"
    )
    
    content = Text.assemble(title , subtitle)

    console.print(
        Panel(
            content,
            border_style="cyan",
            padding=(1,4),
            expand=False
        )
    )

def add_expense():
    if len(categories) == 0:
        print("❌ No category yet !")
        return
    price = FloatPrompt.ask("💰 Enter the price")

    category_name = questionary.select(
        "🏷️ Choose a category",
        choices=[category["name"] for category in categories],
    ).ask()


    description = Prompt.ask(
        "📝 Enter the expense's description",
        default=""
    )

    date_str = Prompt.ask(
        "📅 Enter the date",
        default=datetime.now().strftime("%Y-%m-%d")
    )

    date = datetime.strptime(date_str, "%Y-%m-%d")


    depenses.append({
        "description": description,
        "date": date,
        "price": price,
        "category": category_name,
    })

    print("✅ Expense added!")


def display_expenses(expenses):
    table = Table(title="💰 Expenses")

    table.add_column("Date")
    table.add_column("Description")
    table.add_column("Category")
    table.add_column("Price", justify="right")

    for expense in expenses:
        table.add_row(
            expense["date"].strftime("%Y-%m-%d"),
            expense["description"],
            expense["category"],
            f"${expense['price']:.2f}",
        )

    console.print(table)
    

def add_category():
    while True:
        name = Prompt.ask("🏷️ Enter the category name").strip()

        if not name:
            print("❌ Category name cannot be empty.")
            continue

        if any(category["name"].lower() == name.lower() for category in categories):
            print("❌ This category already exists.")
            continue

        break

    categories.append({
        "name": name,
    })

    print(f"✅ {name} successfully added!")

def view_expenses():
    display_expenses(depenses)

def exit_program():
    print("Good Bye!")
    sys.exit()
    
def view_total():
    total = 0
    
    for i in depenses:
        total += i["price"]
    
    print(f"Total : ${total:.2f}")
    

list_menu = [
    {"name": "💸 Add an expense", "function": add_expense},
    {"name": "🏷️  Add category", "function": add_category},
    {"name": "📊 View expenses", "function": view_expenses},
    {"name": "📊 View Total", "function": view_total},
    {"name": "📅 View expenses between two dates", "function": None},
    {"name": "🗂️  View spending by category", "function": None},
    {"name": "🚪 Exit", "function": exit_program},
]


def print_menu():
    choice = questionary.select(
        "What would you like to do?",
        choices=[item["name"] for item in list_menu],
        pointer="❯",
    ).ask()

    selected = next(
        item for item in list_menu
        if item["name"] == choice
    )

    if selected["function"]:
        selected["function"]()
    else:
        print(f"❌ {selected["name"]} not implemented")

show_header()
while True:
    print_menu()