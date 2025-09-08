from chapter import Chapter

class Book:
    def __init__(self,
        name_arabic: str = '',
        name_latin: str = '',
        n_chapters: int = 0,
        n_verses: int = 0,
        n_words: int = 0,
        n_letters: int = 0,
        list_chapters: list[Chapter] = []
    ):
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_chapters = n_chapters
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters
        self.list_chapters = list_chapters
