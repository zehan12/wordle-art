ef wordle_guess(guess, answer):
    """Given a Wordle guess and the current answer, return the Wordle pattern
    for that guess. The pattern is a 5-character string
    containing G, Y, or W for Green, Yellow, or White."""

    assert len(guess) == 5
    assert len(answer) == 5

    pattern = "WWWWW"
    matched = ""  # characters in the guess that are correct-position matches

    for index, char in enumerate(guess):
        if char == answer[index]:
            pattern = pattern[:index] + "G" + pattern[index + 1 :]
            matched += char

    for index, char in enumerate(guess):
        # If this character occurs in a different position in the answer, AND
        # this character wasn't already matched, then this position in the
        # pattern is a Y.
        other_chars = answer[:index] + answer[index + 1 :]
        if char in other_chars and char not in matched:
            # This may be a Y, but need to allow for duplicated letters.
            # We scan through the answer, determining whether all occurrences
            # of char are already accounted for with Gs or Ys. If so, this is
            # a W instead of a Y.
            char_count = answer.count(char)
            for answer_i, answer_c in enumerate(answer):
                if answer_c == char:
                    if pattern[answer_i] == "G":
                        char_count -= 1  # this occurrence is already matched
            if char_count > 0:
                # There are occurences of char not covered by Gs yet.
                for guess_i, guess_c in enumerate(guess):
                    if guess_c == char and pattern[guess_i] == "Y":
                        char_count -= 1  # out-of-position match already accounted for
            if char_count > 0:
                # There is at least one occurence of this character not yet
                # accounted for by a G or a Y.
                pattern = pattern[:index] + "Y" + pattern[index + 1 :]

    return pattern
