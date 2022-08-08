"""
TO_DO:
- [DONE] Filter duplicates -> sort each team string and find ones that match (same team1, team2, and score)
- Fix complexity for when sorting by team -> line 81, going through list to check for same takes O(N) and
  sorting the team itself takes O(N*M)
- [DONE] Try moving the sort by team to outside the main radix sort
- [DONE] Confirm it's ok to sort in ascending order, then reverse it
- Confirm whether we can use deepcopy

"""
import copy


def analyze(results: list, roster: int, score: int) -> list:
    """

    TO-DO:
    - [DONE] Take into account alternate score
    - [DONE] Check for duplicate matches (matches that have the same team combination and same score)
    - Check for results that have less than 10 matches
    """
    # Create top10_matches and searched_matches arrays
    top10_matches = []
    searched_matches = []

    # Sort results using radix sort
    sorted_results = radix_sort(results, roster)    # O(N)

    # Reverse sorted_results to be in descending order
    sorted_results = sorted_results[::-1]

    # Sort by team1
    starting_index = 0
    stopping_index = 0
    for i in range(1, len(sorted_results)):         # O(N) *
        # If the current score is equal to the previous score,
        # set the current index as stopping index
        if sorted_results[i][2] == sorted_results[i - 1][2]:
            stopping_index = i
        # Else if the current score is different from the previous score,
        # sort team1 from the starting_index up to the stopping_index
        elif sorted_results[i][2] != sorted_results[i - 1][2] and starting_index < stopping_index:
            sorted_sublist = radix_sort_team1(sorted_results, roster, starting_index, stopping_index + 1)
            for j in range(starting_index, stopping_index + 1):
                sorted_results[j] = sorted_sublist[j - starting_index]
            starting_index = i
        # Else if the current score is different from the previous score
        # and starting_index and stopping_index are the same,
        # set the current index as the starting_index
        else:
            starting_index = i

    # Grab top 10 highest matches from sorted results
    for i in range(3):                             # O(1)
        top10_matches.append(sorted_results[i])

    # return [top10_matches, searched_matches]
    return top10_matches


def counting_sort(lst: list, digit_place: int) -> list:
    """
    Stable counting sort

    TIME COMPLEXITY: O(N)
    SPACE COMPLEXITY: O(N)

    """
    # Create count array
    count = [0 for i in range(10)]              # O(1)

    # Iterate through each value in lst and increment count[digit_processed] by 1
    for i in range(len(lst)):                   # O(N)
        digit_processed = (lst[i][2] // (10 ** digit_place)) % 10
        count[digit_processed] += 1

    # Create position array
    position = [0 for i in range(10)]           # O(1)

    # Iterate through each value in count and set position[i] = position[i-1] + count[i-1]
    for i in range(1, 10):                      # O(1)
        position[i] = position[i-1] + count[i-1]

    # Create output array
    output = [0 for i in range(len(lst))]       # O(N)

    # Iterate through each value in lst and set output[position[digit_processed]] = lst[i]
    for i in range(len(lst)):                   # O(N)
        digit_processed = (lst[i][2] // (10 ** digit_place)) % 10
        output[position[digit_processed]] = lst[i]

        # Increment position[value]
        position[digit_processed] += 1

    return output


def radix_sort(lst: list, roster: int) -> list:
    """
    Radix sort

    TIME COMPLEXITY: O(N)
    SPACE COMPLEXITY: O(N)

    """
    # Create output array
    output = [lst[i] for i in range(len(lst))]      # O(N)

    # Go through results and if a score is less than 50, switch it to its alternate format
    for i in range(len(lst)):                       # O(N)
        if output[i][2] < 50:
            output[i] = [output[i][1], output[i][0], 100 - output[i][2]]

    # Filter duplicate matches
    # Sort the team string in each match and if they have the same team and score, only keep one
    output_filter = copy.deepcopy(output)           # O(N * M)
    for i in range(len(lst)):
        output_filter[i][0] = counting_sort_string(output_filter[i][0], roster)
        output_filter[i][1] = counting_sort_string(output_filter[i][1], roster)

    removed_count = 0
    for i in range(1, len(lst)):
        if output_filter[i] == output_filter[i-1]:
            output.pop(i - removed_count)
            removed_count += 1

    # Call countingSort 3 times, looking at one digit at a time starting from the least significant digit
    digit_place = 0
    for i in range(3):                              # O(1) * O(N) = O(N)
        output = counting_sort(output, digit_place)
        digit_place += 1

    return output


def counting_sort_string(string: str, roster: int) -> str:
    # Create count array
    count = [0 for i in range(roster)]      # O(1)

    # Iterate through each character in string and increment count[char_index] by 1
    for i in range(len(string)):            # O(M)
        char_processed = string[i]
        char_index = ord(char_processed) - 65
        count[char_index] += 1

    # Create output string
    output = ""

    # Iterate through count array and append each character
    for i in range(roster):                 # O(1)
        output += chr(i + 65) * count[i]

    return output


def counting_sort_team1(lst: list, roster: int, char_place: int, starting_index: int, stopping_index: int) -> list:
    # Create count array
    count = [0 for i in range(roster)]                              # O(1)

    # Iterate through each value in the sub-array to be sorted and increment count[char_index] by 1
    for i in range(starting_index, stopping_index):                 # In total for all calls: O(N)
        char_processed = lst[i][0][-char_place]
        char_index = ord(char_processed) - 65
        count[char_index] += 1

    # Create position array
    position = [0 for i in range(roster)]                           # O(1)

    # Iterate through each value in count and set position[i] = position[i-1] + count[i-1]
    for i in range(1, roster):                                      # O(1)
        position[i] = position[i - 1] + count[i - 1]

    # Create output array
    output = [0 for i in range(starting_index, stopping_index)]     # In total for all calls: O(N)

    # Iterate through each value in the sub-array and set output[position[char_index]] = lst[i]
    for i in range(starting_index, stopping_index):                 # In total for all calls: O(N)
        char_processed = lst[i][0][-char_place]
        char_index = ord(char_processed) - 65
        output[position[char_index]] = lst[i]

        # Increment position[value]
        position[char_index] += 1

    return output


def radix_sort_team1(lst: list, roster: int, starting_index: int, stopping_index: int) -> list:
    # If lst is empty, do nothing
    if len(lst) == 0:
        return

    # Create result array
    output = [lst[i] for i in range(starting_index, stopping_index)]    # In total for all calls: O(N)

    # Determine length of team
    team_length = len(lst[0][0])

    # Call counting_sort_team1 team_length times, looking at one character at a time starting from the last character
    char_place = 1
    for _ in range(team_length):                                        # In total for all calls: O(M) * O(N)
        output = counting_sort_team1(lst, roster, char_place, starting_index, stopping_index)
        char_place += 1

    return output

list = [["CBA", "DBD", 85], ["ABC", "BDD", 85], ["EAE", "BCA", 85], ["EEE", "BDB", 17], ["EAD", "ECD", 21],
["ECA", "CDE", 13], ["CDA", "ABA", 76]]
print("Before: ")
print(list)
print("After: ")
print(analyze(list, 5, 0))
