import psycopg2
import os
import numpy as np

SERVER_HOST = "localhost"
DATABASE = os.environ.get("BOOKSDATABASE")
USER = os.environ.get("USER_POSTEGRES")
PASSWORD = os.environ.get("PASSWORD")

def get_all_books():
    command = "SELECT * FROM books;"
    
    conn = psycopg2.connect(
            host=SERVER_HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
    cur = conn.cursor()
    cur.execute(command)
    
    result = cur.fetchall()
    
    cur.close()
    conn.commit()
    return result

def get_all_books_column(column_name):
    command = f"SELECT {column_name} FROM books;"
    
    conn = psycopg2.connect(
            host=SERVER_HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
    cur = conn.cursor()
    cur.execute(command)
    
    result = cur.fetchall()
    
    cur.close()
    conn.commit()
    return result   

def get_most_popular_categories(n=10, column_categories="subjects"):
    books = get_all_books_column(column_categories)
    categories = []
    for book in books:
        if book[0]!=None:
            for cat in book[0]:
                categories.append(cat)
    (category, counts) = np.unique(categories, return_counts=True)
    sorted_books = [x for _, x in sorted(zip(counts, category))]
    sorted_books.reverse()
    return sorted_books[:n]
    
    

print(get_most_popular_categories(50))
        
