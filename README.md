This project crawls a NASA dataset online and uses that data to determine which
astronaut spent the most time performing extra-vehicular activities in outer space.

In eva_data.py:
      I used the API to get raw NASA data for "Extra-vehicular Activity (EVA) - US
  and Russia" (6/3/1965-8/22/2013) (https://data.nasa.gov/resource/q8u9-7uq7.json)
      I normalized the formatting of the names and fixed spelling errors
      I converted the duration from hh:mm to a decimal value of hours
      I split the entries with multiple crew members into one entry per crew member
      I created a sqlite database and created a table called Eva that contains the
  crew members and the duration for each excursion.
      I created a second database table called "totals" and inserted distinct
  astronauts as primary keys. I also created a column for total_duration to store
  the sum of duration for each astronaut

In eva_bar.py:
      I created a list (called "eva_list") of dictionaries of the data from the Eva
  sqlite table
      I created a list (called "astros") of distinct astronauts from the Eva sqlite
  table
      Using the eva_list and astros lists I created a list (called "astronaut_durs")
  where each item has an astronaut and a list of all the duration entries for that
  astronaut
      Using astronaut_durs I created a list of dictionaries where each dictionary
  has an astronaut name and the sum of all the duration entries for that astronaut
      I took the data from astronaut_durs and inserted it into the totals sqlite table

In eva_json.py:
      I selected the data from totals table (sorting from highest to lowest duration),
  limiting it to the 30 astronauts with the longest duration
      I opened a write file handle to eva.js and inserted the data into it

In eva.htm:
      I used https://www.gstatic.com/charts/loader.js to create a bar chart of the data
