
class Chapter:
    def __init__(self,
        number: int = 0,
        name_arabic: str = '',
        name_latin: str = '',
        n_verses: str = 0,
        n_words: int = 0,
        n_letters: int = 0
    ):
        self.number = number
        self.name_arabic = name_arabic
        self.name_latin = name_latin
        self.n_verses = n_verses
        self.n_words = n_words
        self.n_letters = n_letters
