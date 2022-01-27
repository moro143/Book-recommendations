import get_requests
import psycopg2
import os

SERVER_HOST = "localhost"
DATABASE = os.environ.get("BOOKSDATABASE")
USER = os.environ.get("USER_POSTEGRES")
PASSWORD = os.environ.get("PASSWORD")

BOOKS_API_DATABASE = {
    "key": {"name": "book_key", "data_type": "text"},
    "type": {"name": "book_type", "data_type": "text"},
    "title": {"name": "book_title", "data_type": "text"},
    "first_publish_year": {"name": "first_publish_year", "data_type": "date"},
    "number_of_pages_median": {"name": "number_of_pages_median", "data_type": "number"},
    "author_key": {"name": "author_key", "data_type": "array_text"},
    "author_name": {"name": "author_name", "data_type": "array_text"},
    "subject": {"name": "subjects", "data_type": "array_text"},
    "subject_facet": {"name": "subject_facet", "data_type": "array_text"},
    "subject_key": {"name": "subject_key", "data_type": "array_text"}
}

def import_new_book_by_request(q):
    results = get_requests.search_book(q)
    n = 0
    for result in results:
        print(n/len(results))
        n+=1
        result_keys = result.keys()
        
        columns = ""
        values = ""

        conn = psycopg2.connect(
            host=SERVER_HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT book_key FROM books WHERE book_key = '" + result["key"] + "'")
        
        if not cur.fetchone():
            for col_name in BOOKS_API_DATABASE.keys():
                if col_name in result_keys:
                    if BOOKS_API_DATABASE[col_name]["data_type"] == "text":
                        columns += BOOKS_API_DATABASE[col_name]["name"] + ", "
                        values += "'" + str(result[col_name]).replace("'", "''")+ "', "

                    elif BOOKS_API_DATABASE[col_name]["data_type"] == "date":
                        columns += BOOKS_API_DATABASE[col_name]["name"] + ", "
                        values += "'" + str(result[col_name]).replace("'", "''") + "-01-01', "
                    
                    elif BOOKS_API_DATABASE[col_name]["data_type"] == "number": 
                        columns += BOOKS_API_DATABASE[col_name]["name"] + ", "
                        values += str(result[col_name]).replace("'", "''") + ", "
            
                    elif BOOKS_API_DATABASE[col_name]["data_type"] == "array_text": 
                        columns += BOOKS_API_DATABASE[col_name]["name"] + ", "
                        array_value = "'{"
                        for v in result[col_name]:
                            array_value += '"' + str(v).replace("'", "''").replace('"','') + '", '
                        values += str(array_value[:-2]) + "}', "
            columns = columns[:-2]
            values = values[:-2]

            command = f"INSERT INTO books ({columns}) VALUES ({values});"
            cur.execute(command)
            conn.commit()
        cur.close()
        conn.close()

