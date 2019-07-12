# this creates a .js file of the eva data
import sqlite3

conn = sqlite3.connect('eva.sqlite')
cur = conn.cursor()

print("Creating JSON output on eva.js...")

# select astronauts and total duration from totals table
cur.execute('SELECT astronaut, total_duration FROM totals ORDER BY total_duration DESC LIMIT 30')
# open eva.js for writing
fhand = open('eva.js', 'w')
fhand.write("evabar = [ ['Astronaut', 'Duration (Hours)']")
# in eva.js insert list of astronauts and total duration
for row in cur:
    astronaut = row[0]
    total_dur = row[1]
    fhand.write(",\n['"+astronaut+"', "+str(total_dur)+"]")

fhand.write( "\n];\n")
fhand.close()

print("Output written to eva.js")
print("Open eva.htm in a browser to see the vizualization")





# # select astronauts and total duration from totals table
# cur.execute('SELECT astronaut, total_duration FROM totals ORDER BY total_duration DESC')
# # open eva.js for writing
# fhand = open('eva.js', 'w')
# fhand.write("evabar = [")
# first = True
# # in eva.js insert dictionary of astronauts and total duration
# for row in cur:
#     # if it's not the first entry, put it on a new line
#     if not first: fhand.write( ",\n")
#     first = False
#     astronaut = row[0]
#     total_dur = row[1]
#     fhand.write("{astronaut: '"+astronaut+"', duration: "+str(total_dur)+"}")
# fhand.write( "\n];\n")
# fhand.close()
#
# print("Output written to eva.js")
# print("Open eva.htm in a browser to see the vizualization")
