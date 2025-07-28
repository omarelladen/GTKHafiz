
import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor

from user import User
from chapter import Chapter
from book import Book

class DBManager():
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.executor = ThreadPoolExecutor(max_workers=1)

    def __load_db_books(self, cur):
        db_table_books = [a for a in cur.execute("SELECT * FROM books")]
        list_books=[]
        for b in db_table_books:
            list_books.append(Book(b[1], b[2], b[3], b[4], b[5], b[6]))
        return list_books

    def __load_db_chapters(self, cur):
        db_table_chapters = [a for a in cur.execute("SELECT * FROM chapters")]
        list_chapters=[]
        for c in db_table_chapters:
            list_chapters.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))
        return list_chapters

    def __load_db_user(self, cur):
        
        # Get the username from system 
        try:
            username = os.getlogin()
        except:
            username = 'user'

        user_data = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user_data: # username already exists in the db, so load it
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            db_table_users_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
            for t in db_table_users_mem_chapters:
                user.mem_chapters.append(t[1])
        else: # create a new user in the db
            user = User(username)
            cur.execute("""
                INSERT INTO users
                (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
                """, (user.username, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))

        return user

    def load_db_data(self):
        if not os.path.isfile(self.db_filename):
            raise FileNotFoundError(f'Failed to find database "{self.db_filename}"')
        
        try:    
            con = sqlite3.connect(self.db_filename)
            cur = con.cursor()

            list_books    = self.__load_db_books(cur)
            list_chapters = self.__load_db_chapters(cur)
            user          = self.__load_db_user(cur)
            
            con.commit()
            con.close()
        except:
            print(f'Failed to load data from "{self.db_filename}"')
            exit(1)

        return user, list_books, list_chapters

    def save_mem_chapters(self, user, chapter, op):
        self.executor.submit(self._save_mem_chapters, user, chapter, op)

    def _save_mem_chapters(self, user:User, chapter:Chapter, op:str):
            con = sqlite3.connect(self.db_filename)
            cur = con.cursor()

            cur.execute("""
                UPDATE users
                SET n_mem_chapters = ?, n_mem_verses = ?, n_mem_words = ?, n_mem_letters = ?
                WHERE username = ?
            """, (user.n_mem_chapters, user.n_mem_verses, user.n_mem_words, user.n_mem_letters, user.username))

            if op == 'add':
                cur.execute("""
                    INSERT INTO mem_chapters
                    (users_username, chapters_number) VALUES (?, ?)
                """, (user.username, chapter.number))
            elif op == 'rm':
                cur.execute("""
                    DELETE FROM mem_chapters
                    WHERE users_username = ? AND
                          chapters_number = ?
                """, (user.username, chapter.number))

            con.commit()
            con.close()
