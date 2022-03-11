ALPHABET = "abcdefghijklmnopqrstuvwxyz".upper()
alphabet_map = {}
for l in range(len(ALPHABET)):
    alphabet_map[ALPHABET[l]] = l

class Hint:
    def passes_hint(self, guess):
        pass
    def should_prune(self, guess):
        pass
    def get_sort_order(self):
        pass
    def __str__(self):
        return "a hint"

def get_spot_hash(is_there, letter, spot):
    return 90000 + is_there * 1000 + spot * 100 + alphabet_map[letter]

def get_count_hash(letter, count, is_exact):
    return count * 1000 + is_exact * 100 + alphabet_map[letter]

class SpotHint(Hint):

    def __init__(self, is_there, letter, spot):
        self.is_there = is_there
        self.letter = letter
        self.spot = spot
        self.hash = get_spot_hash(is_there, letter, spot)
        self.pruning_hash = get_count_hash(letter, 1, False)

    def passes_hint(self, processed_guess):
        return (processed_guess.text[self.spot] == self.letter) == self.is_there

    def should_prune(self, processed_guess):
        return self.pruning_hash in processed_guess.hint_hashes

    def get_sort_order(self):
        return -5 if self.is_there else -4

    def __str__(self):
        return ("" if self.is_there else "No ") + self.letter + " in position " + str(self.spot + 1)

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash


class CountHint(Hint):
    def __init__(self, letter, count, is_exact):
        self.letter = letter
        self.count = count
        self.is_exact = is_exact
        self.hash = get_count_hash(letter, count, is_exact)
        self.pruning_hash = get_count_hash(letter, 1, False)

    def passes_hint(self, processed_guess):
        return self.hash in processed_guess.hint_hashes

    def should_prune(self, processed_guess):
        return self.pruning_hash in processed_guess.hint_hashes

    def get_sort_order(self):
        return -1 * self.count

    def __str__(self):
        if self.count == 0 and self.is_exact:
            return "No " + str(self.letter) + "s"
        return ("" if self.is_exact else "At least ") + str(self.count) + " " + self.letter + ("s" if self.count > 1 else "")

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash