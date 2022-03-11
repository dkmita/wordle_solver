#!/usr/bin/env python
import word_lists
from analyze_word_frequency import get_word_frequency
from hint import SpotHint, CountHint, get_count_hash, get_spot_hash, ALPHABET
import time
import math
from datetime import datetime
from sets import Set
from collections import defaultdict

from analyze_letter_frequency import analyze_word_set

LETTER_COUNT = 5

#print "LEGAL_WORDS", len(word_sets.LEGAL_WORDS)
#analyze_word_set(word_sets.LEGAL_WORDS, LETTER_COUNT)

#print
#print "ANSWER_WORDS", len(word_sets.ANSWER_WORDS)
#analyze_word_set(word_sets.ANSWER_WORDS, LETTER_COUNT)

total_gpw_time = 0

def get_letter_count(letter, word):
  return len([l for l in word if l == letter])

class Word:
  def __init__(self, word, freq_score):
    self.text = word.upper()
    self.freq_score = freq_score
    self.hint_hashes = Set()

    letter_counts = defaultdict(lambda: 0)
    self.hint_hashes = Set()
    for spot in range(LETTER_COUNT):
      letter = self.text[spot]
      self.hint_hashes.add(get_spot_hash(True, letter, spot))
      letter_count = letter_counts[letter] + 1
      self.hint_hashes.add(get_count_hash(letter, letter_count, False))
      letter_counts[letter] = letter_count
    for letter in ALPHABET:
      letter_count = letter_counts[letter]
      self.hint_hashes.add(get_count_hash(letter, letter_count, True))


global word_frequencies
word_frequencies = get_word_frequency()
def get_word_freq_score(word):
  return int(math.log(word_frequencies[word]))-8 if word in word_frequencies else 0

ANSWER_WORDS = [Word(w, get_word_freq_score(w)) for w in word_lists.ANSWER_WORDS]
POSSIBLE_WORDS = ANSWER_WORDS + [Word(w, get_word_freq_score(w)) for w in word_lists.OTHER_LEGAL_WORDS]

def get_hints(guess, answer):
  hints = Set()
  for spot in range(LETTER_COUNT):
    guess_letter = guess[spot]
    if answer[spot] == guess_letter:
      hints.add(SpotHint(True, guess_letter, spot))
    elif guess[spot] not in answer:
      hints.add(CountHint(guess_letter, 0, True))
    else:
      hints.add(SpotHint(False, guess_letter, spot))
      letter_already_guessed_count = get_letter_count(guess_letter, guess[:spot])
      answer_letter_count = get_letter_count(guess_letter, answer)
      if letter_already_guessed_count + 1 > answer_letter_count:
        hints.add(CountHint(guess_letter, answer_letter_count, True))
      else:
        hints.add(CountHint(guess_letter, letter_already_guessed_count + 1, False))
  return hints


def prune_possible_answers(possible_answers, hints):
  possible_words = []
  for answer in possible_answers:
    passes_all_hints = True
    for hint in hints:
      if not hint.passes_hint(answer):
        passes_all_hints = False
        break
    if passes_all_hints:
      possible_words.append(answer)
  #print "gpw took ", (time.time() - gpw_word_start) * 1000, "millis"
  return possible_words

def guess_score(word, hints):
  pass
  #letters_used
  #for hint

class WordleSolve:
  def __init__(self, answer):
    self.answer = answer.upper()
    self.possible_answers = [pw for pw in POSSIBLE_WORDS if pw.freq_score > 0]
    self.sorted_guesses = POSSIBLE_WORDS
    self.hints = Set()

  def guess_word(self, guess, verbose = False):
    if verbose:
      print "Guessed:", guess.upper()
    self.hints = self.hints.union(get_hints(guess.upper(), self.answer))
    if verbose:
      self.possible_answers = prune_possible_answers(self.possible_answers, self.hints)
      self.sorted_guesses = self.prune_possible_guesses(self.sorted_guesses)
      print self
      print "  Sorted guess list length:", len(self.sorted_guesses)
      print "  Possible answer count:", len(self.possible_answers)
      if len(self.possible_answers) <= 60:
        for word in sorted(self.possible_answers)[:60]:
          print "   ", word.text, " freq:", word.freq_score
          #for hint in processed_word[1]:
          #  print hint,


  def prune_possible_guesses(self, guesses):
    possible_guesses = []
    for guess in guesses:
      passes_all_hints = True
      for hint in self.hints:
        if hint.should_prune(guess):
          passes_all_hints = False
          break
      if passes_all_hints:
        possible_guesses.append(guess)
    #print "gpw took ", (time.time() - gpw_word_start) * 1000, "millis"
    return possible_guesses


  def __str__(self):
    return "  Hints: " + str([str(h) for h in sorted(list(self.hints), key = lambda x: x.get_sort_order())])


def analyze_best_guess(pruned_guess_processed_list, possible_answer_processed_words):
  first_guess_word_to_possible_words = defaultdict(lambda: 0)
  analyze_start_time = datetime.now()
  print "Analyzing to find best word. Started at: ", analyze_start_time.strftime("%H:%M:%S")
  if len(pruned_guess_processed_list) > 100:
    print "  Done Percentage: "
  guesses_analyzed = 0
  for processed_guess in pruned_guess_processed_list:
    start_first_guess = time.time()
    for answer in possible_answer_processed_words:
      hints = get_hints(processed_guess.text, answer.text)
      possible_answers_after_guess = len(prune_possible_answers(possible_answer_processed_words, hints))
      #print "If", answer, " possible words after", possible_words_after_guess
      first_guess_word_to_possible_words[processed_guess] += possible_answers_after_guess
    guesses_analyzed += 1
    if len(pruned_guess_processed_list) > 100 and (guesses_analyzed % (len(pruned_guess_processed_list)/20)) == 0:
      now = datetime.now()
      print "   ", str(int(math.ceil(guesses_analyzed * 100.0 / float(len(pruned_guess_processed_list))))).rjust(3), "  ", now.strftime("%H:%M:%S")
    #print "checked first guess of ", guess, "in", (time.time() - start_first_guess) * 1000, "millis"

  ordered_first_guesses = sorted(list(first_guess_word_to_possible_words.items()), key=lambda x:x[1]*1000 - x[0].freq_score)
  print "  Best guesses:", len(first_guess_word_to_possible_words)
  for x in range(min(10, len(first_guess_word_to_possible_words))):
    print ordered_first_guesses[x][0].text, "%.2f%%" % (100-(ordered_first_guesses[x][1] / float(len(possible_answer_processed_words))**2 * 100.0)), "|",
  print
  return ordered_first_guesses[0][0]

import random
answer = "WATCH" #random.choice(word_lists.ANSWER_WORDS).text
print answer
solve = WordleSolve(answer)

comment = ''''''
solve.guess_word("ROATE", verbose=True)
guess_count = 1
while True:
  if len(solve.possible_answers) == 1:
    guess_count += 1
    break
  guess_list = (solve.sorted_guesses + solve.possible_answers) if len(solve.possible_answers) > 3 else solve.possible_answers
  best_guess = analyze_best_guess(guess_list, solve.possible_answers)
  if best_guess == answer:
    solve.guess_word(best_guess.text, verbose=True)
    print "  Got lucky!"
    guess_count += 1
    break
  solve.guess_word(best_guess.text, verbose=True)
  guess_count += 1

print "Took ", guess_count, "guesses"







