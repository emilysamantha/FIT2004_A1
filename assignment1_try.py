"""
Questions:
- Can we use deepcopy?

TODO:
- Confirm space complexity
"""
import copy


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
            The score we want to search for in searchedmatches.

    :Return:
        lst:
             List of findings denoted as [top10matches, searchedmatches], where
             top10matches is a list of 10 matches with the highest score and
             searchedmatches is a list of matches with the same score as score

    :Time Complexity: O(M * N)
    :Aux Space Complexity: O(N)     ??

    TODO:
    - Decompose

    """
    # Create top10_matches and searched_matches arrays
    top10matches = []
    searchedmatches = []

    # Create lst which is a deepcopy of results, to avoid modifying the original list
    lst = copy.deepcopy(results)                # O(N)

    # Go through results and if a score is less than 50, switch it to its alternate format
    for i in range(len(lst)):                   # O(N)
        if lst[i][2] < 50:
            lst[i] = [lst[i][1], lst[i][0], 100 - lst[i][2]]

    # Filter duplicate matches
    # Sort the team string in each match and if they have the same team and score, only keep one
    results_filter = copy.deepcopy(lst)
    for i in range(len(lst)):                   # O(N) * O(M)
        results_filter[i][0] = counting_sort_string(lst[i][0], roster)
        results_filter[i][1] = counting_sort_string(lst[i][1], roster)
        lst[i][0] = counting_sort_string(lst[i][0], roster)
        lst[i][1] = counting_sort_string(lst[i][1], roster)

    # Sort the score in both results_filter and lst
    results_filter = radix_sort_score(results_filter)
    lst = radix_sort_score(lst)

    if len(results_filter) > 1:
        removed_count = 0
        for i in range(1, len(results)):        # O(N)
            if results_filter[i] == results_filter[i - 1]:
                lst.pop(i - removed_count)
                removed_count += 1

    # Sort team2 in lexicographical order
    lst = radix_sort_team(lst, roster, 1)       # O(M) * (N)

    # Sort team1 in lexicographical order
    lst = radix_sort_team(lst, roster, 0)       # O(M) * (N)

    # Sort score in descending order
    lst = radix_sort_score(lst)                 # O(N)

    num_top_matches = 10
    if len(lst) < 10:
        num_top_matches = len(lst)

    # Grab top 10 highest matches from sorted results
    for i in range(num_top_matches):            # O(1)
        top10matches.append(lst[i])

    # Look for searchedmatches
    found = False
    next_highest = 101
    if score < 50:
        for i in range(len(lst)):   # O(N)
            if (100 - lst[i][2]) == score:
                searchedmatches.append([lst[i][1], lst[i][0], 100 - lst[i][2]])
                found = True
            elif (100 - lst[i][2]) > score and found:
                break
            elif (100 - lst[i][2]) > next_highest:
                break
            elif (100 - lst[i][2]) > score and not found:
                searchedmatches.append([lst[i][1], lst[i][0], 100 - lst[i][2]])
                next_highest = 100 - lst[i][2]
            elif not found and (100 - lst[i][2]) == next_highest:
                searchedmatches.append([lst[i][1], lst[i][0], 100 - lst[i][2]])
    else:
        for i in range(len(lst) - 1, -1, -1):   # O(N)
            if lst[i][2] == score:
                searchedmatches.insert(0, lst[i])
                found = True
            elif lst[i][2] > score and found:
                break
            elif lst[i][2] > next_highest:
                break
            elif lst[i][2] > score and not found:
                searchedmatches.append(lst[i])
                next_highest = lst[i][2]
            elif not found and lst[i][2] == next_highest:
                searchedmatches.append(lst[i])

    return [top10matches, searchedmatches]


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
    # Call countingSort 3 times, looking at one digit at a time starting from the least significant digit
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

print(analyze(results, 5, 63))
