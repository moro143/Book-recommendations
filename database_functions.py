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

def get_all_books_columns(column_names=[]):
    string_column_names = ""
    for i in column_names:
        string_column_names += i +", "
    command = f"SELECT {string_column_names[:-2]} FROM books;"
    
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

def get_most_popular_categories(n=-1, column_categories="subjects"):
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

def score_likeness_by_category(categories=get_most_popular_categories(20)):
    books = get_all_books_columns(["book_id", "subjects"])
    categories = set(categories)
    scores = {}
    n=0
    for book1 in books:
        print(n/len(books))
        n+=1
        if book1[1] != None:
            for book2 in books[n:]:
                if book2[1] != None:
                    cat_book1 = set(book1[1])
                    cat_book2 = set(book2[1])
                    score = len(cat_book1.intersection(categories.intersection(cat_book2)))
                    scores[(book1[0], book2[0])] = score
                    #print(score)
                    # if book1[1] != None and book2[1] != None:
                    #     for cat in book1[1]:
                    #         if cat in categories and cat in book2[1]:
                    #             score+=1
                    #     sco   res[(book1[0], book2[0])] = score
    n=0
    for i in scores.keys():
        if scores[i]>n:
            n=scores[i]
            print(i, scores[i])
    return scores
            

scores = score_likeness_by_category()
