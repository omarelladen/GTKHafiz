from chapter import Chapter

class User:
    def __init__(self,
        username: str = '',
        n_mem_chapters: int = 0,
        n_mem_words: int = 0,
        n_mem_verses: int = 0,
        n_mem_letters: int = 0,
        list_mem_chapters: list[Chapter] = [],
    ):
        self.username = username
        self.list_mem_chapters = list_mem_chapters
        self.n_mem_chapters = n_mem_chapters
        self.n_mem_words = n_mem_words
        self.n_mem_verses = n_mem_verses
        self.n_mem_letters = n_mem_letters
