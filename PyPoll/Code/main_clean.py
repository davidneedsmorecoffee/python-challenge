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

uniq_candidates = [list(t) for t in set(map(tuple, name_only))] # create a list of lists of candidates

# this method (which doesn't require a counter) will work better if the list has a huge number of various candidates
# this inner looop with j basically count through all the ballots starting with the first candidate
# The i outter loop basically repeats the inner loop with a different i-th candidate
votes = 0
vote_result = []
for i in range(0, len(uniq_candidates)): # for i in 0 to len(uniq_candidates) which is 4 in this case
    for j in range(0, row_count): # for j in 0 to row_count, which is all the votes that came in
        if name_only[j][0]==uniq_candidates[i][0]: # if the j-th list (list item [0] because there's only one item in the list) mathces the i-th uniq_candidate, 
            votes = votes + 1 # then add 1 to the total count of votes
    vote_result.extend((uniq_candidates[i][0], votes)) # everytime we finish counting the votes for i-th unique candiate, we extend (we don't append here because we're adding multiple elements to the list and extending it ) the vote_results list by adding the i-th name from the uniq_candidates list, followed by the # of votes he/she received
    votes = 0
    # reset the counter at 0 here because after each j loop before going to the next i we want to reset the votes counter
    # this is the vote_result ["O'Tooley", 105630, 'Khan', 2218231, 'Li', 492940, 'Correy', 704200]

def divide_chunks(l, n): # set up a function that takes requires the l and n parameters; # looping till length l 
    for i in range(0, len(l), n):  # for in in range from 0 to length of the "l"ist, 
        yield l[i: i + n] # from the l list, slice from i to (i+n); not including (i+n)

# because the vote_result from earlier is in a list with alternating names and # of votes, we want to create a list of lists from that, where each list will have two elements
n = 2 #each list will have two elements
name_and_votes = list(divide_chunks(vote_result, n)) 
# name_and_votes gives #[["O'Tooley", 105630], ['Khan', 2218231], ['Li', 492940], ['Correy', 704200]]

#results_sorted = sorted(x, key=lambda x: x[1], reverse=True) #reverse the sorting so it's in decreasing order
results_sorted = sorted(name_and_votes, key=lambda name_and_votes:name_and_votes[1], reverse=True)
# [['Khan', 2218231], ['Correy', 704200], ['Li', 492940], ["O'Tooley", 105630]]

# need to determine the number of summary rows for the loop function later that prints out the results for each candidate
summary_nrow = len(results_sorted)

# the following is used to sum up all the votes received by each candidate to obtain the all_votes (total)
all_votes = 0
for i in range(0, summary_nrow):
    all_votes = all_votes + results_sorted[i][1]

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

# create a csv output of the election results
output_path = os.path.join("..", "Results", "Election_result_output.csv")
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')  # Initialize csv.writer
    csvwriter.writerow(['Total votes', all_votes, '', ''])
    csvwriter.writerow([''])
    csvwriter.writerow(['Candidate', 'Number of votes received', 'Percentage of total votes', ''])
    for i in range(0, summary_nrow): # for each candidate print out the votes counted as well as the % votes received
        for j in range(0, 1):
            csvwriter.writerow([results_sorted[i][j], results_sorted[i][j+1], round(results_sorted[i][j+1]/all_votes*100,2),'']) 
    csvwriter.writerow([''])
    csvwriter.writerow(['Winner:', results_sorted[0][0], '', '']) # since already ranked in descending order, results_sorted [0][0] gives the winner

quit()