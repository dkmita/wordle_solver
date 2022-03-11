#!/usr/bin/env python
import word_lists


def get_word_frequency():
    frequency_map = {}
    f = open("unigram_freq.csv", "r")
    line_count = 0
    while True:

        line = f.readline()
        if not line:
            break
        split_line = line.split(',')
        if len(split_line) != 2:
            continue
        else:
            line_count += 1
            if len(split_line[0]) == 5:
                frequency_map[split_line[0].lower()] = int(split_line[1])
    f.close()
    return frequency_map

comment = '''
freq_map = get_word_frequency()

no_freq = []
freq_count = 0
bad_words = []
total_freq_value = 0
THRESHOLD = 100000
for word in word_lists.ANSWER_WORDS:
    if word in freq_map:
        freq_count += 1
        freq_value = freq_map[word.lower()]
        total_freq_value += freq_map[word.lower()]
        if freq_value <= THRESHOLD:
            bad_words.append(word)
    else:
        no_freq.append(word)

print "ANSWER LIST:"
print "no frequencies", len(no_freq), "BAD:", len(bad_words), bad_words
answer_word_avg = total_freq_value/freq_count
print "average frequency", freq_count, total_freq_value/freq_count

no_freq = []
freq_count = 0
good_words = []
total_freq_value = 0
for word in word_lists.OTHER_LEGAL_WORDS:
    if word in freq_map:
        freq_count += 1
        freq_value = freq_map[word.lower()]
        total_freq_value += freq_map[word.lower()]
        if freq_value > THRESHOLD:
            good_words.append(word)
    else:
        no_freq.append(word)

print
print "OTHER LEGAL WORDS:"
print "total: ", len(word_lists.OTHER_LEGAL_WORDS)
print "no frequency:", len(no_freq), "GOOD:", len(good_words), [gw for gw in good_words if (gw[4] != 's') and gw[3:5] != "ed"]
print "average freqency:", freq_count, total_freq_value/freq_count
'''
