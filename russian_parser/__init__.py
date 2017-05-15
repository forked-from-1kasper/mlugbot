# nominative
# genitive
# dative
# accusative
# instrumental
# prepositional


class Word:
    def __init__(self, text):
        self.text = text
        self.identify()

    def identify(self):
        pass


def parse(text):
    text = text.split()
    text = list(map(Word, text))
    return False
