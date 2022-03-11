#!/usr/bin/env python
from collections import defaultdict

def analyze_word_set(word_set, letter_count):
    word_count = len(word_set)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    letter_spots = []
    letter_in_word_frequency = defaultdict(lambda: 0)
    for spot in range(letter_count):
        letter_spots.append(defaultdict(lambda: 0))

    for word in word_set:
        for a in alphabet:
            if a in word:
                letter_in_word_frequency[a] += 1
        for spot in range(letter_count):
            letter_spots[spot][word[spot]] += 1

    ordered_letter_in_word_frequency = sorted(list(letter_in_word_frequency.items()), key=lambda x:x[1], reverse=True)

    for (al, count) in ordered_letter_in_word_frequency:
        percentage_count = count / float(word_count) * 100.0
        print " ", al.upper(), "  IN WORD:", ("%.2f%%" % percentage_count).rjust(6), "    IN SPOT:",
        for spot in range(letter_count):
            letter_count_in_spot = letter_spots[spot][al]
            percentage_in_spot = letter_count_in_spot / float(word_count) * 100.0
            print ("%.2f%%" % percentage_in_spot).rjust(6),
        print

