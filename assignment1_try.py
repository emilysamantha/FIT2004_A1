"""
TODO:
- Confirm space complexity
- Check edge cases
- Try removing returning lists

"""


def analyze(results: list, roster: int, score: int) -> list:
    """
    Performs an analysis on tournament results. Uses radix sort and counting sort to perform
    the analysis on the list of matches.

    :Input:
        results:
            Past tournament data represented as a list of lists. The inner list can be
            described as [team1, team2, score], where team1 and team2 are uppercase strings
            and score is an integer value in the range of 0 to 100 inclusive.
        roster:
            Positive integer to denote the character set used in team1 and team2.
            For example, roster=5 indicates a character set of {A, B, C, D, E}
        score:
            The score we want to search for and return in searchedmatches.

    :Return:
        lst:
             List of findings denoted as [top10matches, searchedmatches], where
             top10matches is a list of 10 matches with the highest score and
             searchedmatches is a list of matches with the same score as score

    :Time Complexity: O(N * M)
    :Aux Space Complexity: O(N * M)     ??
    """
    # Create top10_matches and searched_matches arrays
    top10matches = []
    searchedmatches = []

    # Go through results and if a score is less than 50, switch it to its alternate format
    switch_format(results)

    # Sort the team string in each match
    for i in range(len(results)):       # O(N) * O(M)
        results[i][0] = counting_sort_string(results[i][0], roster)
        results[i][1] = counting_sort_string(results[i][1], roster)

    # Sort team2 in lexicographical order
    results = radix_sort_team(results, roster, 1)       # O(M) * (N)

    # Sort team1 in lexicographical order
    results = radix_sort_team(results, roster, 0)       # O(M) * (N)

    # Sort score in descending order
    results = radix_sort_score(results)                 # O(N)

    # Filter duplicate matches
    results = filter_duplicates(results)

    # If the number of matches in results is less than 10, set num_top_matches as the length of results
    num_top_matches = 10
    if len(results) < 10:
        num_top_matches = len(results)

    # Grab top 10 highest matches from sorted results
    for i in range(num_top_matches):            # O(1)
        top10matches.append(results[i])

    # Look for searchedmatches
    find_searchedmatches(results, score, searchedmatches)

    return [top10matches, searchedmatches]


def switch_format(lst: list) -> None:
    """
    Function to switch the format of matches that have a score below 50.
    Switches team1 with team2 and sets the score of the match as the alternate format (100-score).

    :Input:
        lst: The results list

    :Time Complexity: O(N)
    :Aux Space Complexity: ??
    """
    for i in range(len(lst)):  # O(N)
        if lst[i][2] < 50:
            lst[i] = [lst[i][1], lst[i][0], 100 - lst[i][2]]


def counting_sort_string(string: str, roster: int) -> str:
    """
    Function to sort a string in ascending lexicographical order using counting sort algorithm.

    :Input:
        string:
            The string to be sorted
        roster:
            Positive integer to denote the character set used in string.
            For example, roster=5 indicates a character set of {A, B, C, D, E}

    :Return:
        str: string that has been sorted in ascending lexicographical order

    :Time Complexity: O(M)
    :Aux Space Complexity: O(M)
    """
    # Create count array
    count = [0 for i in range(roster)]          # O(1)

    # Go through each character in string and increment count[char_index] by 1
    for i in range(len(string)):                # O(M)
        char_processed = string[i]
        char_index = ord(char_processed) - 65
        count[char_index] += 1

    # Create output string
    output = ""

    # Iterate through count array and append each character
    for i in range(roster):                     # O(1)
        output += chr(i + 65) * count[i]

    return output


def radix_sort_team(lst: list, roster: int, team_num: int) -> list:
    """
    Function to sort one of the teams inside the results list in ascending lexicographical order
    using radix sort algorithm.

    :Input:
        lst:
            The results list to be sorted
        roster:
            Positive integer to denote the character set used in team1 and team2.
            For example, roster=5 indicates a character set of {A, B, C, D, E}
        team_num:
            Integer to denote the team number that we want to sort.
            Team numbers start from 0 (0 to represent team1 and 1 to represent team2)

    :Return:
        lst: The results list that has been sorted

    :Time Complexity: O(M * N)
    :Aux Space Complexity: O(N)         ??
    """
    # Determine number of characters in the team
    num_chars = len(lst[0][0])

    # Call counting_sort_team team_length times, looking at one character at a time starting from the last character
    char_place = 1
    for _ in range(num_chars):                  # O(M) * O(N)
        lst = counting_sort_team(lst, roster, char_place, team_num)
        char_place += 1

    return lst


def counting_sort_team(lst: list, roster: int, char_place: int, team_num: int) -> list:
    """
    Function to sort a specified column of characters in ascending lexicographical order
    using counting sort algorithm.

    :Input:
        lst:
            The results list to be sorted
        roster:
            Positive integer to denote the character set used in team1 and team2.
            For example, roster=5 indicates a character set of {A, B, C, D, E}
        char_place:
            Integer to denote which character place we are sorting on.
            1 to denote the last character in the string, 2 to denote the second last
            character in the string, and so on
        team_num:
            Integer to denote the team number that we want to sort.
            Team numbers start from 0 (0 to represent team1 and 1 to represent team2)

    :Return:
        lst: The results list that has been sorted

    :Time Complexity: O(N)
    :Aux Space Complexity: O(N)         ??
    """
    # Create count array
    count = [0 for i in range(roster)]          # O(1)

    # Go through each character in lst and increment count[char_index] by 1
    for i in range(len(lst)):                   # O(N)
        char_processed = lst[i][team_num][-char_place]
        char_index = ord(char_processed) - 65
        count[char_index] += 1

    # Create position array
    position = [0 for i in range(roster)]       # O(1)

    # Go through each value in count and set position[i] = position[i-1] + count[i-1]
    for i in range(1, roster):                  # O(1)
        position[i] = position[i - 1] + count[i - 1]

    # Create output array
    output = [0 for i in range(len(lst))]       # O(N)

    # Go through each value in lst and set output[position[char_index]] = lst[i]
    for i in range(len(lst)):                   # O(N)
        char_processed = lst[i][team_num][-char_place]
        char_index = ord(char_processed) - 65
        output[position[char_index]] = lst[i]

        # Increment position[value]
        position[char_index] += 1

    return output


def radix_sort_score(lst: list) -> list:
    """
    Function to sort the score inside the results list in decreasing order
    using radix sort algorithm.

    :Input:
        lst:
            The results list to be sorted

    :Return:
        lst: The results list that has been sorted

    :Time Complexity: O(N)
    :Aux Space Complexity: O(N)         ??
    """
    # Call counting_sort_score 3 times, looking at one digit at a time starting from the least significant digit
    digit_place = 0
    for i in range(3):                          # O(1) * O(N) = O(N)
        lst = counting_sort_score(lst, digit_place)
        digit_place += 1

    return lst


def counting_sort_score(lst: list, digit_place: int) -> list:
    """
    Function to sort a specified digit place in descending order
    using counting sort algorithm

    :Input:
        lst:
            The results list to be sorted
        digit_place:
            Integer to denote which digit place we are sorting on

    :Return:
        lst: The results list that has been sorted

    :Time Complexity: O(N)
    :Aux Space Complexity: O(N)         ??
    """
    # Create count array
    count = [0 for i in range(10)]              # O(1)

    # Go through each value in lst and increment count[digit_processed] by 1
    for i in range(len(lst)):                   # O(N)
        digit_processed = (lst[i][2] // (10 ** digit_place)) % 10
        count[digit_processed] += 1

    # Create position array
    position = [0 for i in range(10)]           # O(1)

    # Go through each value in count and set position[i] = position[i-1] + count[i-1]
    for i in range(8, -1, -1):                  # O(1)
        position[i] = position[i+1] + count[i+1]

    # Create output array
    output = [0 for i in range(len(lst))]       # O(N)

    # Go through each value in lst and set output[position[digit_processed]] = lst[i]
    for i in range(len(lst)):                   # O(N)
        digit_processed = (lst[i][2] // (10 ** digit_place)) % 10
        output[position[digit_processed]] = lst[i]

        # Increment position[value]
        position[digit_processed] += 1

    return output


def filter_duplicates(lst: list) -> list:
    """
    Function to delete any duplicate matches, meaning matches that have the same team1, team2, and score.

    :Input:
        lst: The results list to be filtered

    :Output:
        lst: The results list that has been filtered.

    :Time Complexity: O(N)
    :Aux Space Complexity: O(N) ??
    """
    # Go through the list and if they have the same team and score, only keep one
    removed_count = 0
    i = 1
    length = len(lst)
    while i < length:
        if lst[i] == lst[i - 1]:
            lst.pop(i)
            i -= 1
            length -= 1
        i += 1
    return lst


def find_searchedmatches(lst: list, score: int, searchedmatches: list) -> None:
    """
    Function that goes through the sorted lst to find a match with the score that is passed.

    :Input:
        lst: Past tournament data represented as a list of lists that has been sorted by score
        in descending order, by team1 in ascending lexicographical order if score is equal, and by
        team2 in ascending lexicographical order if score and team1 are equal.
        score: The score we want to search for and return in searchedmatches.
        searchedmatches: list of matches with the same score as score.

    :Time Complexity: O(N)
    :Aux Space Complexity: O(N)
    """
    # Create flag to indicate whether a match has been found
    found = False
    next_highest = 101

    # If the score we are searching for is less than 50
    if score < 50:
        # Iterate through lst from the smallest index (going through lst from the smallest score going up)
        for i in range(len(lst)):       # O(N)
            # Invert the score in lst
            score_to_check = 100 - lst[i][2]

            # If score_to_check is equal to the score we are searching for
            if score_to_check == score:
                # Append the match to searchedmatches, but in the alternate format
                searchedmatches.append([lst[i][1], lst[i][0], score_to_check])
                # Mark found as True
                found = True
            # Else if we have found an equal score and score_to_check is greater than the score
            # or if we have not found an equal score (meaning we have appended the next highest score)
            # and score_to_check is greater than the next highest score
            elif (found and score_to_check > score) or (not found and score_to_check > next_highest):
                # Stop searching (break out of the loop)
                break
            # Else if we have not found an equal score and score_to_check is greater than the score
            # we are searching for
            elif not found and score_to_check > score:
                # Append the match to searchedmatches, but in the alternate format
                searchedmatches.append([lst[i][1], lst[i][0], score_to_check])
                # Set next highest to this score
                next_highest = score_to_check
            # ELse if we have not found an equal match and score_to_check is equal to the next highest score
            elif not found and score_to_check == next_highest:
                # Append the match to searchedmatches, but in the alternate format
                searchedmatches.append([lst[i][1], lst[i][0], score_to_check])
    # Else if the score we are searching for is 50 or greater
    else:
        # Going through lst from the largest index (going through lst from the smallest score going up)
        for i in range(len(lst) - 1, -1, -1):  # O(N)
            score_to_check = lst[i][2]
            # If score_to_check is equal to the score we are searching for
            if score_to_check == score:
                # Append the match to searchedmatches
                searchedmatches.insert(0, lst[i])
                # Mark found as True
                found = True
            # ELse if we have found an equal score and score to check is greater than the score
            # or if we have not found an equal score (meaning we have appended the next highest score)
            # and score_to_check is greater than the next highest score
            elif (found and score_to_check > score) or (not found and score_to_check > next_highest):
                # Stop searching (break out of the loop)
                break
            # Else if we have not found an equal score and score_to_check is greater than the score
            # we are searching for
            elif not found and score_to_check > score:
                # Append the match to searchedmatches
                searchedmatches.insert(0, lst[i])
                # Set next highest to this score
                next_highest = score_to_check
            # ELse if we have not found an equal match and score_to_check is equal to the next highest score
            elif not found and lst[i][2] == next_highest:
                # Append the match to searchedmatches
                searchedmatches.append(lst[i])


example = [["CBA", "DBD", 85],
           ["ABC", "BDD", 85],
           ["EAE", "BCA", 85],
           ["EEE", "BDB", 17],
           ["EAD", "ECD", 21],
           ["ECA", "CDE", 13],
           ["CDA", "ABA", 76]]
results = [["AAB", "AAB", 35], ["AAB", "BBA", 49], ["BAB", "BAB", 42],
           ["AAA", "AAA", 38], ["BAB", "BAB", 36], ["BAB", "BAB", 36],
           ["ABA", "BBA", 57], ["BBB", "BBA", 32], ["BBA", "BBB", 49],
           ["BBA", "ABB", 55], ["AAB", "AAA", 58], ["ABA", "AAA", 46],
           ["ABA", "ABB", 44], ["BBB", "BAB", 32], ["AAA", "AAB", 36],
           ["ABA", "BBB", 48], ["BBB", "ABA", 33], ["AAB", "BBA", 30],
           ["ABB", "BBB", 68], ["BAB", "BBB", 52]]
one_match = [["CBA", "DBD", 85]]

example2 = [["CBA", "DBD", 85], ["CBA", "DAD", 85], ["CBA", "DBD", 85], ["CBA", "DBD", 85]]

print(analyze(example, 5, 23))
