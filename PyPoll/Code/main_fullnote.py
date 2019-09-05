import csv
import os
csvpath = os.path.join('..', 'Resources', 'election_data.csv') 

with open(csvpath, "r") as f:
    reader = csv.reader(f,delimiter = ",")
    next(reader) # skip the first row
    data = list(reader) # make a list of lists
    row_count = len(data) # count the length of the list of lists
print("there are", row_count, "rows of data, excluding the header") # 3521001

name_only = [list(row) for row in data] # use this to create a copy of the list 


for x in name_only: #for all the lists in name_only
         del x[:2] #del x[0] #remove the first two items from each list, i.e. list[0] and list[1]; this leaves the name of the candidate

# quick test
# print(name_only[0:5]) #[['Khan'], ['Correy'], ['Khan'], ['Khan'], ['Khan']]
# print(name_only[1:5]) #[['Correy'], ['Khan'], ['Khan'], ['Khan']]

# uniq_candidates_test = set(map(tuple, name_only)) 
# print(uniq_candidates_test) 
        # {('Queen', 'Li'), ('Bamoo', "O'Tooley"), ('Trandee', 'Correy'), ('Raffah', 'Khan'), ('Marsh', 'Khan'), ('Queen', 'Correy'), ('Trandee', "O'Tooley"), ('Raffah', 'Correy'), ('Queen', "O'Tooley"), ('Raffah', 'Li'), ('Marsh', 'Li'), ('Trandee', 'Khan'), ('Bamoo', 'Li'), ('Queen', 'Khan'), 
        # ('Marsh', 'Correy'), ('Bamoo', 'Khan'), ('Trandee', 'Li'), ('Marsh', "O'Tooley"), ('Bamoo', 'Correy')}

uniq_candidates = [list(t) for t in set(map(tuple, name_only))]
print(uniq_candidates) #[["O'Tooley"], ['Khan'], ['Li'], ['Correy']]

# the map(tuple, name_only) part performs the function tupule on the name_only iterable. 
# the set(...) creates an unordered collection with no duplicate elements
# the list(t) for t in part takes the output form the set(...) and convert it back to a list

# tupules 
        # consist of a number of values separated by commas
        # https://docs.python.org/3/tutorial/datastructures.html
                # "Though tuples may seem similar to lists, they are often used in different situations and for different purposes. Tuples are immutable, and usually contain a heterogeneous sequence of elements that are accessed via unpacking (see later in this section) or indexing (or even by attribute in the case of namedtuples). Lists are mutable, and their elements are usually homogeneous and are accessed by iterating over the list."
# set 
        # https://docs.python.org/3/tutorial/datastructures.html
                # A set is an unordered collection with no duplicate elements. Basic uses include membership testing and eliminating duplicate entries. Set objects also support mathematical operations like union, intersection, difference, and symmetric difference.
# map()
        # https://www.geeksforgeeks.org/python-map-function/
                # map() function returns a list of the results after applying the given function to each item of a given iterable (list, tuple etc.)
                    # Syntax: 
                        # map(fun, iter)
                   # Parameters :
                       # fun : It is a function to which map passes each element of given iterable.
                                # https://www.geeksforgeeks.org/python-difference-iterable-iterator/#targetText=Python%20%7C%20Difference%20between%20iterable%20and,using%20__next__()%20method.&targetText=For%20example%2C%20a%20list%20is,list%20is%20not%20an%20iterator.
                                # iterable is an object that one can iterate over. A list is iterable but a list is not an iterator
                       # iter : It is a iterable which is to be mapped.

# this is using a counter to double-check the answer for the code later on.
# https://stackoverflow.com/questions/19211018/using-counter-with-list-of-lists
from collections import Counter
c=Counter()
for i in name_only: # for each i-th list in the name_only list of lists; each i = list (containing one name)
    for j in set(i): # for each j-th item in each list (in this case each list only contains one name)
        c[j] += 1 # += adds another value with the variable's value and assigns the new value to the variable;
                    # in this every time each name is counted we add 1 to the total value
print(c) #Counter({'Khan': 2218231, 'Correy': 704200, 'Li': 492940, "O'Tooley": 105630})

print(len(uniq_candidates)) #4

# this method (which doesn't require a counter) will work better if the list has a huge number of various candidates
votes = 0
vote_result = []
for i in range(0, len(uniq_candidates)): # for i in 0 to len(uniq_candidates) which is 4 in this case
    for j in range(0, row_count): # for j in 0 to row_count, which is all the votes that came in
        if name_only[j][0]==uniq_candidates[i][0]: # if the j-th list (list item [0] because there's only one item in the list) mathces the i-th uniq_candidate, 
            votes = votes + 1 # then add 1 to the total count of votes
            # this inner looop with j basically count through all the ballots starting with the first candidate
# The i outter loop basically repeats the inner loop with a different i-th candidate
    vote_result.extend((uniq_candidates[i][0], votes)) # everytime we finish counting the votes for i-th unique candiate, we extend (we don't append here because we're adding multiple elements to the list and extending it ) the vote_results list by adding the i-th name from the uniq_candidates list, followed by the # of votes he/she received
    votes = 0
    # reset the counter at 0 here because after each j loop before going to the next i we want to reset the votes counter

 # Append vs. Extend
        # Append adds its argument as a single element to the end of a list. The length of the list itself will increase by one. extend iterates over its argument adding each element to the list, extending the list. The length of the list will increase by however many elements were in the iterable argument.

print("this is the vote result", vote_result) # this gives #['Khan', 631, 'Correy', 225, "O'Tooley", 23, 'Li', 121]; 
# we need to split this up so each candidate and the numb of votes they recieved are paired
# this is the vote result ["O'Tooley", 105630, 'Khan', 2218231, 'Li', 492940, 'Correy', 704200]

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
# https://stackoverflow.com/questions/4012340/colon-in-python-list-index

# """Yield successive n-sized chunks from l."""
# How many elements each 
# list should have 
def divide_chunks(l, n): # set up a function that takes requires the l and n parameters
    # looping till length l 
    for i in range(0, len(l), n):  # for in in range from 0 to length of the "l"ist, 
        yield l[i: i + n] # from the l list, slice from i to (i+n); not including (i+n)

n = 2 #each list will have two elements
name_and_votes = list(divide_chunks(vote_result, n)) 
print (name_and_votes) #[["O'Tooley", 105630], ['Khan', 2218231], ['Li', 492940], ['Correy', 704200]]

print(vote_result) #["O'Tooley", 105630, 'Khan', 2218231, 'Li', 492940, 'Correy', 704200]
print(vote_result[0:1]) #["O'Tooley"]; slice from 0 to 1 (1 not included)
print(vote_result[0:0 +1]) #["O'Tooley"]; same as above
print(vote_result[1:1 +1]) #[105630]; slice from 1 to 2 (2 not included); item 1 = second thing from the list since count starts from 0
print(vote_result[1:2]) #[105630]; same as above
print(vote_result[2:2 +1]) #['Khan']; slice from 2 to 3 (3 not included)
print(vote_result[0:0 +2]) #["O'Tooley", 105630]; slice from 0 to 2 (2 not included); this gives items 0 and 1
print(vote_result[1:1 +2]) #[105630, 'Khan']; slice from 1 to 3 (3 not included); this gives items 1 and 2
print(vote_result[2:2 +2]) #['Khan', 2218231]; slice from 2 to 4 (4 not included); this gives items 2 and 3
print(vote_result[2:2 +3]) #['Khan', 2218231, 'Li']; slice from 2 to 5 (5 not-included); this gives items 2, 3, 4

# https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list/4174955
#results_sorted = sorted(x, key=lambda x: x[1], reverse=True) #reverse the sorting so it's in decreasing order
results_sorted = sorted(name_and_votes, key=lambda name_and_votes:name_and_votes[1], reverse=True)
print(results_sorted)
# [['Khan', 2218231], ['Correy', 704200], ['Li', 492940], ["O'Tooley", 105630]]

# https://www.geeksforgeeks.org/sorted-function-python/
# Sorting 
        # Sorted() sorts any sequence (list, tuple) and always returns a list with the elements in sorted manner, without modifying the original sequence.
        # Syntax : sorted(iterable, key, reverse)
        # Parameters : sorted takes three parameters from which two are optional.
                # Iterable : sequence (list, tuple, string) or collection (dictionary, set, frozenset) or any other iterator that needs to be sorted.
                # Key(optional) : A function that would server as a key or a basis of sort comparison.
                # Reverse(optional) : If set true, then the iterable would be sorted in reverse (descending) order, by default it is set as false.
# https://www.w3schools.com/python/python_lambda.asp
    # A lambda function that adds 10 to the number passed in as an argument, and print the result:
        # x = lambda a : a + 10
        # print(x(5))

# need to determine the number of summary rows for the loop function later that prints out the results for each candidate
summary_nrow = len(results_sorted)
print(summary_nrow) #4

# the following is used to sum up all the votes received by each candidate to obtain the all_votes (total)
all_votes = 0
for i in range(0, summary_nrow):
    all_votes = all_votes + results_sorted[i][1]
print(all_votes)

# generate a print out with a summary of the results
print(
f"Election Results \n\
------------------------------------------ \n\
Total votes: {all_votes} \n\
------------------------------------------")
for i in range(0, summary_nrow):
    for j in range(0, 1):
        print(f"{results_sorted[i][j]}: {results_sorted[i][j+1]} votes ({round(results_sorted[i][j+1]/all_votes*100,2)} % of votes)")
print(
f"------------------------------------------ \n\
Winner of this election: {results_sorted[0][0]} \n\
------------------------------------------")


output_path = os.path.join("..", "Results", "Election_restul_output_test.csv")
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')  # Initialize csv.writer
    # csvwriter.writerow(['Election results', 'Number', '', ''])  # Write the first row (column headers)
    csvwriter.writerow(['Total votes', all_votes, '', ''])
    csvwriter.writerow([''])
    csvwriter.writerow(['Candidate', 'Number of votes received', 'Percentage of total votes', ''])
    # csvwriter.writerow(['----------------------', '', '', ''])
    for i in range(0, summary_nrow):
        for j in range(0, 1):
            csvwriter.writerow([results_sorted[i][j], results_sorted[i][j+1], round(results_sorted[i][j+1]/all_votes*100,2),'']) 
    csvwriter.writerow([''])
    csvwriter.writerow(['Winner:', results_sorted[0][0], '', ''])

quit()