"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    num = 0
    if len(paragraphs) <= k :
        return ''
    for i in range(len(paragraphs)) :
        if select(paragraphs[i]) :
            num += 1
        if k == num - 1 :
            return paragraphs[i]
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    """
    def check(paragraphs) :
        remove_punctuation(paragraphs)
        paragraphs = ' ' + paragraphs
        lenpara = len(paragraphs)
        paragraphs += ' '
        paragraphs = paragraphs.lower()
        lentop = len(topic)
        for i in range(lentop) :
            lentopx = len(topic[i])
            border = [0 for j in range(lentopx)]
            j = 0
            for k in range(1, lentopx) :
                while j and topic[i][k] != topic[i][j] :
                    j = border[j-1]
                if topic[i][k] == topic[i][j] :
                    j += 1
            j = 0
            for k in range(0, lenpara) :
                while j and paragraphs[k] != topic[i][j] :
                    j = border[j-1]
                if paragraphs[k] == topic[i][j] :
                    j += 1
                if (j == lentopx) and paragraphs[k+1] == ' ' and paragraphs[k-j] == ' ' :
                    return True
                if (j == lentopx) and not(paragraphs[k+1] == ' ' and paragraphs[k-j] == ' ') :
                    j = 0
        return False
    return check
    The code is false.
    """
    def func(para):
        para = split(lower(remove_punctuation(para)))
        for i in para:
            if i in topic:
                return True
        return False
    return func
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.
    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    match_count = 0
    # BEGIN PROBLEM 3
    len_typed = len(typed_words)
    len_ref = len(reference_words)
    for i in range(min(len_typed, len_ref)):
        if typed_words[i] == reference_words[i]:
            match_count += 1
    if len_typed == 0:
        return 0.0
    return match_count / len_typed * 100.0
    # END PROBLEM 3

def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    len_typed = len(typed)
    return len_typed / 5 / elapsed * 60
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    unvalid_num = 0
    num_limit = limit + 1
    word = user_word
    len_valid = len(valid_words)
    for i in range(len_valid):
        if user_word == valid_words[i]:
            return user_word
    for i in range(len_valid):
        diff_num = diff_function(user_word, valid_words[i], limit)
        if diff_num <= limit and diff_num < num_limit:
            word = valid_words[i]
            num_limit = diff_num
    return word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    
    def move(str1, str2, ans):
        if str1 == '':
            return len(str2) + ans
        if str2 == '':
            return len(str1) + ans
        if ans > limit:
            return ans
        if str1[0] != str2[0]:
            ans += 1
        return move(str1[1:], str2[1:], ans)
    return move(start, goal, 0)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    
    if limit < 0: # Fill in the condition
        # BEGIN
        return 1
        # END

    elif start == '' or goal == '': # Feel free to remove or add additional cases
        # BEGIN
        return len(start) + len(goal)
        # END

    elif start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)

    else:
        add_diff = pawssible_patches(start, goal[1:], limit - 1)
        remove_diff = pawssible_patches(start[1:], goal, limit - 1)
        substitute_diff = pawssible_patches(start[1:], goal[1:], limit - 1)
        # BEGIN
        return min(add_diff, remove_diff, substitute_diff) + 1
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    right_sum = 0
    for i in range(len(typed)):
        if typed[i] != prompt[i]:
            break
        else:
            right_sum += 1
    point = right_sum / len(prompt)
    send({'id': user_id, "progress": point})
    return point
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    player_num = len(times_per_player)
    times = [[] for i in range(player_num)]
    for i in range(player_num):
        times[i] = [times_per_player[i][j + 1] - times_per_player[i][j] for j in range(len(words))]
    return game(words, times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    best_time = [[] for i in player_indices]
    for i in word_indices:
        quickest_time = time(game, 0, i)
        quickest_player = 0
        for j in player_indices:
            if time(game, j, i) < quickest_time:
                quickest_player = j
                quickest_time = time(game, j, i)
        best_time[quickest_player].insert(len(best_time[quickest_player]), word_at(game, i))
    return best_time


    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)