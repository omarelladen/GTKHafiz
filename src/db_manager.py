
import sqlite3
import os

from user import User
from chapter import Chapter
from book import Book

class DBManager():
    def __init__(self, db_filename):
        self.db_filename = db_filename

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
        db_table_users = [a for a in cur.execute("SELECT * FROM users")]
        if len(db_table_users) > 0:
            list_users =[]
            for u in db_table_users:
                list_users.append(User(u[0], u[1], u[2], u[3], u[4]))
            user = list_users[0]

            db_table_users_mem_chapters = [a for a in cur.execute("SELECT * FROM mem_chapters")]
            for t in db_table_users_mem_chapters:
                user.mem_chapters.append(t[1])
        else:
            username = os.getlogin()
            user = User(username)

            cur.execute("""
                INSERT INTO users
                (username, n_mem_chapters, n_mem_words, n_mem_verses, n_mem_letters) VALUES (?, ?, ?, ?, ?)
                """, (user.username, user.n_mem_chapters, user.n_mem_words, user.n_mem_verses, user.n_mem_letters))
        return user

    def load_db_data(self):
        con = sqlite3.connect(self.db_filename)
        cur = con.cursor()

        list_books    = self.__load_db_books(cur)
        list_chapters = self.__load_db_chapters(cur)
        user          = self.__load_db_user(cur)
        
        con.commit()
        con.close()

        return user, list_books, list_chapters

    def save_mem_chapters(self, user:User, chapter:Chapter, op:str):
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
