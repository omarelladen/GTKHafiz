
import os
import sqlite3

from user import User
from chapter import Chapter
from book import Book

class DBManager():
    def __init__(self, db_filename: str = ''):
        self._db_filename = db_filename

    def load_book(self):
        if not os.path.isfile(self._db_filename):
            raise FileNotFoundError(f'Failed to find database "{self._db_filename}"')
        try:
            con = sqlite3.connect(self._db_filename)
            cur = con.cursor()
            
            book_data = cur.execute("SELECT * FROM books").fetchone()
            book = Book(book_data[1], book_data[2], book_data[3], book_data[4], book_data[5], book_data[6])
        except con.DatabaseError:
            raise con.DatabaseError(f'Failed to load data from "{self._db_filename}"')
        return book

    def load_chapters(self):
        if not os.path.isfile(self._db_filename):
            raise FileNotFoundError(f'Failed to find database "{self._db_filename}"')
        try:
            con = sqlite3.connect(self._db_filename)
            cur = con.cursor()

            db_table_chapters = [a for a in cur.execute("SELECT * FROM chapters")]
            list_chapters=[]
            for c in db_table_chapters:
                list_chapters.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))
        except con.DatabaseError:
            raise con.DatabaseError(f'Failed to load data from "{self._db_filename}"')
        return list_chapters

    def load_user(self):
        if not os.path.isfile(self._db_filename):
            raise FileNotFoundError(f'Failed to find database "{self._db_filename}"')

        # Get the username from system
        try:
            username = os.getlogin()
        except:
            username = "user"

        try:
            con = sqlite3.connect(self._db_filename)
            cur = con.cursor()

            user_data = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user_data:  # username already exists in the db, so load it
                user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
                db_table_users_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
                for t in db_table_users_mem_chapters:
                    user.list_mem_chapters.append(t[1])
            else:  # create a new user in the db
                user = User(username)
                cur.execute("""
                    INSERT INTO users
                    (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
                    """, (user.username, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))

            con.commit()
            con.close()
        except con.DatabaseError:
            raise con.DatabaseError(f'Failed to load data from "{self._db_filename}"')

        return user
        
    def save_user_data(self, user):
        con = sqlite3.connect(self._db_filename)
        cur = con.cursor()

        # Update memorized stats
        cur.execute("""
            UPDATE users
            SET n_mem_chapters = ?, n_mem_verses = ?, n_mem_words = ?, n_mem_letters = ?
            WHERE username = ?
        """, (user.n_mem_chapters, user.n_mem_verses, user.n_mem_words, user.n_mem_letters, user.username))

        # Remove old memorized list
        cur.execute("""
            DELETE FROM mem_chapters
            WHERE users_username = ?
        """, (user.username,))

        # Insert updated memorized list
        for c in user.list_mem_chapters:
            cur.execute("""
                INSERT INTO mem_chapters
                (users_username, chapters_number) VALUES (?, ?)
            """, (user.username, c))

        con.commit()
        con.close()
