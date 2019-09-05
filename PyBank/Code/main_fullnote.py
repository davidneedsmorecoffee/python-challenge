# importing the file via csv and os
import csv
import os
csvpath = os.path.join('..', 'Resources', 'budget_data.csv') 

with open(csvpath, "r") as f:
    reader = csv.reader(f,delimiter = ",")
    next(reader) # skip the first row
    data = list(reader) # make a list of lists
    row_count = len(data) # count the length of the list of lists
print("there are", row_count, "rows of data, excluding the header")

# https://stackoverflow.com/questions/13244466/in-python-how-do-i-delete-the-nth-list-item-from-a-list-of-lists-column-delete
# this removes the item[1] of all lists
    # for x in data_with_header:
    #     del x[1]

# quick test
# print(data)  # Starts with [['Jan-2010', '867884'], ['Feb-2010', '984655'], ['Mar-2010', '322013'],
# print((data[0][0])) #gives Jan-2010; first list's first item
# print((data[0][1]))  #gives 867884; first list's second item

total = 0 # first define total as 0
for i in range(0, row_count):
    total = total + int(data[i][1]) #sum through the "i"th list's item[1], which is the Profit/Losses values

# calculate the change from month to month
change = []
change.append(None)
for i in range(0, (row_count-1)):
    change.append(int(data[i+1][1]) - int(data[i][1])) # take the value from i+1 month and subtract from i month's profit/losses

# Quick check print(change)

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

n = 1 #each list will have 1 elements; this is so we can combine this list with the other one later
change_list = list(divide_chunks(change, n)) 

# quick check
# print(change_list)

# take the change_list and flatten it so we can zip it with the original columns of data later
flat_change_list = []
for sublist in change_list:
    for item in sublist:
        flat_change_list.append(item)
# quick check print(flat_change_list)

# append the flat_change_list to the existing data; essentially adding in the "third column", u.e., third item to each list/row
for x, y in zip(data, flat_change_list): 
    x.append(y)

# another quick check
# print(data)
# print(data[0])
# print(len(data)) 
# print(total) #38382578
# print((data[0][2]))

# calculate the total change by summing up all the month-to-month changes
total_change = 0
j=0
for j in range(1, row_count): #start with 1 instead of 0 because the first change is based on Feb - Jan 
    total_change = total_change + data[j][2]
# quick check
# print(total_change)  # -196785

# calculate the average of the month-to-month change
average = round((total_change / (len(data)-1)),2) #len(data)-1 because for Nth months there are Nth-1 changes between months
# quick check 
# print(len(data)-1) #85
# print(average) #-2315.12

# determine where the maximum month-to-month change occurs
maximum = int(data[1][2])
j=0
for j in range(1, row_count): # start with 1 because the first "month-to-month" change is based on Feb (change from Jan)
    if int(data[j][2]) > int(maximum): 
        maximum = data[j][2] # the 2-th item in the list (i.e., 3rd) is the change value
        maxrow = j
        maxdate = data[j][0] # the 0-th item in the list (i.e., 1st) is the date when the greatest change occurs

# quick check
# print(maximum)  # 1926159
# print(maxrow) # 25
# print(data[maxrow]) # ['Feb-2012', '1170593', 1926159]

# determine when the minimum month-to-month change occurs, i.e., greatest decrease
minimum = int(data[1][2])
k=0
for k in range(1, row_count):
    if int(data[k][2]) < int(minimum):
        minimum = data[k][2]
        minrow = k
        mindate = data[k][0]

# quickcheck
# print(minimum)  # -2196167
# print(minrow) # 44
# print(data[minrow]) # ['Sep-2013', '-1196225', -2196167]

# print out the results in the console
print(f"Financial Analyis \n\
---------------------- \n\
Total Months: {row_count} \n\
Total: ${total} \n\
Average change: ${average} \n\
Greatest Increase in Profits: {maxdate} (${maximum}) \n\
Greatest Decrease in Profits: {mindate} (${minimum})")

# print the results out as a csv file
# the csvwriter.writerow lines are used to format the .csv file, each "row"/list has 4 items.
output_path = os.path.join("..", "Results", "PyBank_results.csv")
# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')  # Initialize csv.writer
    csvwriter.writerow(['Financial Report', 'Date', 'Unit', 'Value'])  # Write the first row (column headers)
    #csvwriter.writerow(['----------------------', '', '', ''])
    csvwriter.writerow(['Total Months', '', '$', row_count])
    csvwriter.writerow(['Total', '', '$', total])
    csvwriter.writerow(['Greatest Increase in Profits', maxdate, '$', maximum])
    csvwriter.writerow(['Greatest Decrease in Profits', mindate, '$', minimum])
quit()
