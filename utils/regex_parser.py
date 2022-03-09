class WordParser:
    __WORD_PATTERN = r"(\W|^){}(\W|$)"

    @classmethod
    def contains(cls, phrase, text) -> bool:
        import re
        """Ritorna true se `text` contiene `phrase` come parola; per esempio,
        se il testo è "ciao, come stai?", darà True se `phrase` è 'ciao', oppure
        'come', oppure 'stai', ma darà False se è 'sta', 'ci', 'com'."""
        return bool(re.search(
            cls.__WORD_PATTERN.format(re.escape(phrase)), text)
        )
