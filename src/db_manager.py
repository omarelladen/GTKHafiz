
import sqlite3
import os

from user import User
from chapter import Chapter
from book import Book

class DBManager():
    def __init__(self, db_filename: str = ''):
        self.db_filename = db_filename

    def _load_db_books(self, cur):
        db_table_books = [a for a in cur.execute("SELECT * FROM books")]
        list_books=[]
        for b in db_table_books:
            list_books.append(Book(b[1], b[2], b[3], b[4], b[5], b[6]))
        return list_books

    def _load_db_chapters(self, cur):
        db_table_chapters = [a for a in cur.execute("SELECT * FROM chapters")]
        list_chapters=[]
        for c in db_table_chapters:
            list_chapters.append(Chapter(c[0], c[1], c[2], c[3], c[4], c[5]))
        return list_chapters

    def _load_db_user(self, cur):
        # Get the username from system
        try:
            username = os.getlogin()
        except:
            username = "user"

        user_data = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user_data:  # username already exists in the db, so load it
            self._user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            db_table_users_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
            for t in db_table_users_mem_chapters:
                self._user.mem_chapters.append(t[1])
        else:  # create a new user in the db
            self._user = User(username)
            cur.execute("""
                INSERT INTO users
                (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
                """, (self._user.username, self._user.n_mem_chapters, self._user.n_mem_words, self._user.n_mem_verses, self._user.n_mem_letters))

        return self._user

    def load_db_data(self):
        if not os.path.isfile(self.db_filename):
            raise FileNotFoundError(f'Failed to find database "{self.db_filename}"')
        try:
            con = sqlite3.connect(self.db_filename)
            cur = con.cursor()

            list_books    = self._load_db_books(cur)
            list_chapters = self._load_db_chapters(cur)
            user          = self._load_db_user(cur)

            con.commit()
            con.close()
        except con.DatabaseError:
            raise con.DatabaseError(f'Failed to load data from "{self.db_filename}"')
        return user, list_books, list_chapters

    def save_user_data(self):
        con = sqlite3.connect(self.db_filename)
        cur = con.cursor()

        cur.execute("""
            UPDATE users
            SET n_mem_chapters = ?, n_mem_verses = ?, n_mem_words = ?, n_mem_letters = ?
            WHERE username = ?
        """, (self._user.n_mem_chapters, self._user.n_mem_verses, self._user.n_mem_words, self._user.n_mem_letters, self._user.username))

        cur.execute("""
            DELETE FROM mem_chapters
            WHERE users_username = ?
        """, (self._user.username,))

        for c in self._user.mem_chapters:
            cur.execute("""
                INSERT INTO mem_chapters
                (users_username, chapters_number) VALUES (?, ?)
            """, (self._user.username, c))

        con.commit()
        con.close()
