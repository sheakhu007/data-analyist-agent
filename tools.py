from langchain_core.tools import tool
import sqlite3

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Example:
    25 * 12 + 10
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)
    
@tool
def joke_generator() -> str:
    """
    Generate a random joke.
    """
    import random
# here can we create dynamic unique jokes using LLM or any other method?

    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "Why did the math book look sad? Because it had too many problems.",
        "Why did the tomato turn red? Because it saw the salad dressing!"
    ]

    return random.choice(jokes)

@tool
def run_sql(query: str) -> str:
    """
    Execute a SQLite query against the sales database.

    Only call this tool after generating a valid SQLite query.
    """

    conn = sqlite3.connect("database/sales.db")

    cursor = conn.cursor()

    try:
        cursor.execute(query)

    except Exception as e:
        return f"ERROR: {str(e)}"

    rows = cursor.fetchall()

    conn.close()

    return str(rows)

@tool
def get_schema() -> str:
    """
    Return the schema of the SQLite database.

    Use this tool before generating SQL whenever you are unsure
    about table names or column names.
    """

    conn = sqlite3.connect("database/sales.db")

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(sales)")

    schema = cursor.fetchall()

    conn.close()

    return str(schema)

TOOLS = [
    get_schema,
    run_sql,
    calculator,
    joke_generator
]