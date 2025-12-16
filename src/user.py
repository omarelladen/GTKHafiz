from .chapter import Chapter

class User:
    def __init__(self,
        username,
        n_mem_chapters = 0,
        n_mem_words = 0,
        n_mem_verses = 0,
        n_mem_letters = 0,
        list_mem_chapters: list[Chapter] = [],
    ):
        self.username = username
        self.list_mem_chapters = list_mem_chapters
        self.n_mem_chapters = n_mem_chapters
        self.n_mem_words = n_mem_words
        self.n_mem_verses = n_mem_verses
        self.n_mem_letters = n_mem_letters

    def add_mem_chapter(self, chapter):
        if not chapter.number in self.list_mem_chapters:
            self.list_mem_chapters.append(chapter.number)
            self.n_mem_chapters += 1
            self.n_mem_verses   += chapter.n_verses
            self.n_mem_words    += chapter.n_words
            self.n_mem_letters  += chapter.n_letters

    def rm_mem_chapter(self, chapter):
        if chapter.number in self.list_mem_chapters:
            self.list_mem_chapters.remove(chapter.number)
            self.n_mem_chapters -= 1
            self.n_mem_verses   -= chapter.n_verses
            self.n_mem_words    -= chapter.n_words
            self.n_mem_letters  -= chapter.n_letters
