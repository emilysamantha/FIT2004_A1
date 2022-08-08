"""
Questions:
- Are we allowed to modify the original list that is passed in?
- Can we use deepcopy?

"""
import copy


def analyze(results: list, roster: int, score: int) -> list:
    """

    TODO:
    - Check for length 1 results
    """
    # Create top10_matches and searched_matches arrays
    top10_matches = []
    searched_matches = []

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

    removed_count = 0
    for i in range(1, len(results)):            # O(N)
        if results_filter[i] == results_filter[i - 1]:
            lst.pop(i - removed_count)
            removed_count += 1

    print("results_filter:")
    print(results_filter)

    print("Filtered lst:")
    print(lst)

    # Sort team2 in lexicographical order
    lst = radix_sort_team(lst, roster, 1)       # O(M) * (N)

    # Sort team1 in lexicographical order
    lst = radix_sort_team(lst, roster, 0)       # O(M) * (N)

    # Sort score in descending order
    lst = radix_sort_score(lst)                 # O(N)

    # Grab top 10 highest matches from sorted results
    for i in range(10):  # O(1)
        top10_matches.append(lst[i])

    return top10_matches


def counting_sort_string(string: str, roster: int) -> str:
    """

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

    """
    # Call countingSort 3 times, looking at one digit at a time starting from the least significant digit
    digit_place = 0
    for i in range(3):                          # O(1) * O(N) = O(N)
        lst = counting_sort_score(lst, digit_place)
        digit_place += 1

    return lst


def counting_sort_score(lst: list, digit_place: int) -> list:
    """

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


# print("Before: ")
# print(example)
# print("After: ")
print(analyze(results, 2, 0))
