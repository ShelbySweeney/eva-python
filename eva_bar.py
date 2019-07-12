# this is to prepare data for a bar graph
import sqlite3

conn = sqlite3.connect('eva.sqlite')
cur = conn.cursor()

# make a list of dictionaries of data from Eva table
eva_list = []
cur.execute('SELECT astronaut, duration FROM Eva')
for row in cur:
    ret = {
        'astronaut': row[0],
        'duration': row[1],
    }
    eva_list.append(ret)

# make a list of astronauts from "Eva" table
astros = []
cur.execute('SELECT DISTINCT astronaut FROM Eva ORDER BY astronaut')
for row in cur:
    astros.append(row[0])


# make a list of astronauts and a list of durations for each astronaut
astronaut_durs = []
for astro in astros:
    dur_list = []
    # create a list of all duration entries for each astronaut
    for row in eva_list:
        if astro == row['astronaut']:
            dur_list.append(row['duration'])
    # create a list of each astronaut with a list of that astronauts durations
    ret = [astro, dur_list]
    astronaut_durs.append(ret)


# make a list of dictionaries where each dictionary has an astronaut name
# ..and the sum of all the duration entries for that astronaut
astro_total_durs = []
for row in astronaut_durs:
    astronaut = row[0]
    total_durs = sum(row[1])
    ret = {
        'astronaut': astronaut,
        'total_duration': total_durs,
    }
    astro_total_durs.append(ret)

# update totals table with data from astro_total_durs list
for item in astro_total_durs:
    cur.execute('UPDATE totals SET total_duration=? WHERE astronaut=?',
        (item['total_duration'], item['astronaut']))

# commit data when program ends
conn.commit()
cur.close()
