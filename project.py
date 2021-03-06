from math import e
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib
matplotlib.use("TkAgg")


#####################################################
# Variables are below
####################################################

proc_max = 7            # maximum number of processes supported
count = 0               # the number of processes entered
time = 0
time_max = 0
algos = ["SJN", "FCFS", "P", "RR"]
selected_algo = -1
data = []
# process queue - list of lists representing the state of the q at each time
proc_queue = []

# y values where labels should appear on the chart
y_points = [2, 6, 10, 14, 18, 22, 26]
# process names for the y-axis of the chart
y_labels = ['', '', '',
            '', '', '', '']
# values defining bar y positions and heights
y_ranges = [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4), (20, 4), (24, 4)]

# bar colors
colors = ['tab:blue', 'tab:green', 'tab:orange',
          'tab:red', 'tab:purple', 'tab:cyan', 'tab:pink']

# displayed text
message = "Instructions:\n\n 1. Select an algorithm\n 2. Enter process info\n 3. Press RUN"

# Plotting the graph inside a Figure
fig = Figure(figsize=(8.5, 2), dpi=100)
fig.patch.set_facecolor('xkcd:grey')
axes = fig.add_subplot(111)

axes.set_xlabel("Seconds")
axes.set_title("Process Execution Timeline")
axes.tick_params(left=False)      # no ticks on the vertical axis
x_ticks = np.arange(0, 61, 5)  # values for the x axis
axes.set_xticks(x_ticks)       # x values where numbers should be labeled
axes.set_ylim(0, 32)
axes.set_yticks(y_points)
axes.set_yticklabels(y_labels)


######################################################
# Code for the functions is below
######################################################


def add():
    # add process info to the table
    global count
    # prevent entering if required entries are blank
    if len(ent_name.get()) != 0 and len(ent_arrival.get()) != 0 and len(ent_burst.get()) != 0:
        try:
            int(ent_arrival.get())
            int(ent_burst.get())
        except Exception as ex :
            print(ex)
            message = "An Incorect value was entered"
            lbl_message_text.configure(text=message) 
            return
        if selected_algo == "P":
            try:
                int(ent_priority.get())
            except Exception as ex:
                print(ex)
                message = "An invalid priority was entered"
                lbl_message_text.configure(text=message) 
                return
        # if an algorithm is not selected, then do not add anything
        if selected_algo != -1:
            if(count < proc_max+1):
                table.insert(parent='', index='end', iid=count, text='', values=(
                    ent_name.get(), ent_arrival.get(), ent_burst.get(), ent_priority.get()))
                count += 1
                
                if(selected_algo == algos[0]):
                    # add data for shortest job next
                    data.append({"name": ent_name.get(), "arrival": int(ent_arrival.get()),
                                "burst": int(ent_burst.get())})

                elif(selected_algo == algos[1]):
                    # add data for FCFS
                    fin_time = int(ent_arrival.get()) + int(ent_burst.get())
                    data.append({"name": ent_name.get(), "arrival": int(ent_arrival.get()),
                                "burst": int(ent_burst.get())})
                elif (selected_algo == "P"):

                    data.append({"name": ent_name.get(), "arrival": int(ent_arrival.get()),
                                "burst": int(ent_burst.get()),'priority':int(ent_priority.get())})
                    # print(data)
                elif (selected_algo == "RR"):
                  data.append({"name": ent_name.get(), "arrival": int(ent_arrival.get()),
                                "burst": int(ent_burst.get())})
                ent_name.delete(0, tk.END)
                ent_arrival.delete(0, tk.END)
                ent_burst.delete(0, tk.END)
                ent_priority.delete(0, tk.END)
# END OF add


def remove():
    global count
    # remove selected process from table and from stored data
    global count

    selected = table.focus()
    # prevent trying to remove when nothing is slected in table
    if selected:
        # remove value from data list
        del data[int(selected)]
        table.delete(selected)

        count = count - 1

def run():
    if(selected_algo == algos[0]):
        total_time()
        shortest_job_next()

# END OF run

    if(selected_algo == algos[1]):
        total_time()
        fcfs()
    if (selected_algo =="P"):
        total_time()
        prioritySchedule()


    elif(selected_algo == "RR"):
      total_time()
      roundrobin()
   
   

def animate(y_points, y_labels, animation):
    global axes

    ani_x_values = [[], [], [], [], [], [], []]

    #print(animation)

    for i in range(time_max):
        # for each time unit
        advance_time()
        update_queue_display(i)

        for p in range(count):
        
            # for each process

            # values for the animation
            # xrange - (x-position of rectancle, width of rectangle)
            # yrange - (y-position of rectancle, height of rectangle)

            #print(animation[p]["xranges"],i,animation[p]["xranges"][i])
            ani_x_values[p].append(tuple(animation[p]["xranges"][i]))
            axes.broken_barh(xranges=ani_x_values[p],
                             yrange=y_ranges[p], facecolors=colors[p])
        

        x_ticks = np.arange(0, 61, 5)  # values for the x axis
        axes.set_xticks(x_ticks)
        axes.set_xlim(0, 60)
        axes.set_ylim(0, 32)
        axes.set_yticks(y_points)
        axes.set_yticklabels(y_labels)

        plt.pause(1.0)  # pause for one second
        canvas.draw()
        canvas.flush_events()
# END OF animate


def forget(widget):
  widget.grid_forget()
# shows relevant entry


def select_SJN_algo():
    global selected_algo
  #change to algo[]
    selected_algo = algos[0]

   

    forget(ent_priority)
    forget(ent_time)
    forget(lbl_priority)
    forget(lbl_time)
    displaycolumns=[]
    for col in table["columns"]:
      if col != "priority":
        displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns
    btn_RR.config(bg="black")
    btn_SJN.config(bg="grey")
    btn_FCFS.config(bg="black")
    btn_P.config(bg="black")
    
    
   

def select_RR_algo():
    global selected_algo

    #change to algo[]
    selected_algo = algos[3]
    forget(ent_priority)
    forget(lbl_priority)
    lbl_time.grid(row=0, column=4)
    ent_time.grid(row=1, column=4)
    displaycolumns=[]
    for col in table["columns"]:
      if col != "priority":
        displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns
    btn_RR.config(bg="grey")
    btn_SJN.config(bg="black")
    btn_FCFS.config(bg="black")
    btn_P.config(bg="black")
    
    
    

def select_priority_algo():
    global selected_algo


    #change to algo[]
    selected_algo = algos[2]
    ent_priority.grid(row=1, column=3)
    lbl_priority.grid(row=0, column=3)
    forget(lbl_time)
    forget(ent_time)
    displaycolumns=[]
    for col in table["columns"]:
      displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns
    btn_RR.config(bg="black")
    btn_SJN.config(bg="black")
    btn_FCFS.config(bg="black")
    btn_P.config(bg="grey")

def select_FCFS_algo():
  global selected_algo
  #change to algo[]
  selected_algo = algos[1]
  forget(ent_priority)
  forget(ent_time)
  forget(lbl_priority)
  forget(lbl_time)
  displaycolumns=[]
  for col in table["columns"]:
    if col != "priority":
      displaycolumns.append(col)
  table["displaycolumn"]=displaycolumns
  btn_RR.config(bg="black") 
  btn_SJN.config(bg="black")
  btn_FCFS.config(bg="grey")
  btn_P.config(bg="black")
 
        

def advance_time():
    global time

    time += 1

    minutes = str(time // 60).zfill(2)
    seconds = str(time % 60).zfill(2)
    lbl_clock.configure(text=minutes + " : " + seconds)

# END OF advance_time

    if time / 60 >= 1:
        minute = str(round(time/60))
        seconds = time % 60
        clock_time = str(minute) + ":" + str(seconds)
    else:
        if time > 9:
            clock_time = "0:" + str(time)
        else:
            clock_time = "0:0" + str(time)
    lbl_clock.config(text=str(clock_time))




def total_time():
    global time_max

    # accumulate the duration times for all processes
    t = 0
    for p in range(len(data)):
        t += data[p]['burst']

    # find latest end time
    ends = []
    for p in range(len(data)):
        ends.append(data[p]['burst'] + data[p]['arrival'])
    max_end = max(ends)

    if t > max_end:
        time_max = t
    else:
        time_max = max_end


def update_queue_display(time):
    # clear the queue display table
    for i in q.get_children():
        q.delete(i)
    #print(data,time)
    #print(proc_queue[time])
    # NOTE - proc_queue has the form [ [0,3], [3], ... ]
    #   with one inner list for each time, having index number and processes to be displayed
    for pos in range(len(proc_queue[time])):

        process_index = proc_queue[time][pos]
        #print(data[process_index]['name'])

        process_name = data[process_index]['name']

        q.insert(parent='', index='end', iid=pos,
                 text='', values=(process_name))
# END OF update_queue_display


def before_algorithm():
    global y_points
    global y_labels

    # update y_values according to number of processes
    #y_points = y_points[:count]

    # process names for the y-axis of the chart
    #y_labels = []
    for p in range(count):
        y_labels[p] = data[p]['name']
# END OF before_algorithm


def compute_x_values(proc):
    global proc_queue
    x_values = []

    for x in range(len(proc)):
        x_values.append([])

    # computing x_values based on state of queue at different times
    for q in range(len(proc_queue)):
        for p in range(len(proc)):

            # if the queue is not empty at this time
            if len(proc_queue[q]) > 0:
                # find process at top of the queue
                if proc_queue[q][0] == proc[p]['index']:
                    if proc[p]['progress'] == 0:
                        # if process is just starting
                        proc[p]['progress'] += 1
                        # store start as current time in the queue
                        proc[p]['start'] = q
                        x_values[p].append(
                            (proc[p]['start'], proc[p]['progress']))

                    elif 0 < proc[p]['progress'] < proc[p]['burst']:
                        # a process that has started and is not finished will increse in progress
                        proc[p]['progress'] += 1
                        x_values[p].append(
                            (proc[p]['start'], proc[p]['progress']))
                else:
                    # process that is not executing has its x_values repeated
                    x_values[p].append(
                        (proc[p]['start'], proc[p]['progress']))

            # if the queue is empty at this time
            else:
                # if the queue is empty at this time no process is executed
                # process that is not executing has its x_values repeated
                x_values[p].append((proc[p]['start'], proc[p]['progress']))

    return x_values

# END OF compute_x_values

def roundrobin():
    global y_points
    global proc_queue

    # update y_values according to number of processes
    y_points = y_points[:count]

    # process names for the y-axis of the chart
    y_labels = []
    for p in range(count):
        y_labels.append(data[p]['name'])

    animation = []
    x_values = []
    proc = []
    executing = -1
    last = -1
    try:
        timeslice = int(ent_time.get())
    except Exception as ex:
        print(ex)
        message = "A invalid time slice was entered"
        lbl_message_text.configure(text=message) 
        return

    # store process indices and burst times and arrival times
    for p in range(count):
        proc.append({"index": p, "burst": data[p]['burst'],
                    "arrival": data[p]['arrival'], "start": 0, "progress": 0})
    #print(proc)

    for t in range(time_max):
        if t == 0:
            proc_queue.append([])
        else:
            # copy previous state of the queue
            proc_queue.append(proc_queue[t-1][:])

        # add indices of arriving processes to the end of the queue
        for a in range(len(proc)):
            if proc[a]['arrival'] == t:
                proc_queue[t].append(a)

        # if process is currently being executed
        if executing != -1 and len(proc_queue[t]) > 0:
            proc[executing]['progress'] += 1

            # is process finihsed
            if proc[executing]['progress'] >= proc[executing]['burst']:
                proc_queue[t].pop(0)  # remove from top of queue
                executing = -1

            # if slice is finished and last process executed is still in queue
            if proc[executing]['progress'] % timeslice == 0 and executing != -1:
                #adds process to the end of the queue
                l=proc_queue[t].pop(0)
                proc_queue[t].append(l)

                # process in progress
                executing = proc_queue[t][0]
                last = executing

        if executing == -1 and len(proc_queue[t]) > 0:
            # process in progress
            executing = proc_queue[t][0]
            last = executing

        #print(t, executing)
   # print(proc_queue)

    for x in range(len(proc)):
        proc[x]['progress'] = 0     # reset progress values
        proc[x]['start'] = 0        # reset start values
        x_values.append([])

    start_track = 0
    # computing x_values based on state of queue at different times
    for q in range(len(proc_queue)):
        for p in range(len(proc)):

            # if the queue is not empty at this time
            if len(proc_queue[q]) > 0:
                # find process at top of the queue
                if proc_queue[q][0] == proc[p]['index']:
                    if proc[p]['progress'] == 0:
                        # if process is just starting
                        proc[p]['progress'] += 1
                        # store start as current time in the queue
                        proc[p]['start'] = q
                        x_values[p].append(
                            (proc[p]['start'], proc[p]['progress']))

                        start_track += 1

                    elif 0 < proc[p]['progress'] < proc[p]['burst']:
                        # a process that has started and is not finished will increse in progress

                        # a process starting the slice has its start at the end
                        #   end of the last process, and its progress at 0
                        if proc[p]['progress'] % timeslice == 0:
                            proc[p].update({'progress': 1})
                            proc[p].update({'start': start_track})
                            x_values[p].append(
                                (proc[p]['start'], proc[p]['progress']))

                            start_track += 1

                        else:
                            # a process in the slice uses its previous start
                            proc[p]['progress'] += 1
                            x_values[p].append(
                                (proc[p]['start'], proc[p]['progress']))

                            start_track += 1
                else:
                    # process that is not executing has its x_values repeated
                    x_values[p].append(
                        (proc[p]['start'], proc[p]['progress']))

            # if the queue is empty at this time
            else:
                # if the queue is empty at this time no process is executed
                # process that is not executing has its x_values repeated
                x_values[p].append((proc[p]['start'], proc[p]['progress']))

    #print(x_values)

    # for each process, add x-values and yrange
    for x in range(count):
        animation.append({"xranges": x_values[x], "yrange": y_ranges[x]})

    animate(y_points, y_labels, animation)
  

def shortest_job_next():
    global proc_queue

    # prepare the gantt chart axis
    before_algorithm()

    animation = []
    proc = []
    executing = -1

    # store process indices and burst times and arrival times
    for p in range(count):
        proc.append({"index": p, "burst": data[p]['burst'],
                    "arrival": data[p]['arrival'], "start": 0, "progress": 0})

    #print(proc)


    for t in range(time_max):
        if t == 0:
            proc_queue.append([])
        else:
            # copy previous state of the queue
            proc_queue.append(proc_queue[t-1][:])


        # add indices of arriving processes to the end of the queue

        for a in range(len(proc)):
            if proc[a]['arrival'] == t:
                proc_queue[t].append(a)

        # if process is currently being executed
        if executing != -1 and len(proc_queue[t]) > 0:
            proc[executing]['progress'] += 1

            # is process finihsed
            if proc[executing]['progress'] >= proc[executing]['burst']:
                proc_queue[t].pop(0)  # remove from top of queue
                executing = -1

        if executing == -1 and len(proc_queue[t]) > 0:
            # choose process with shortest burst time
            short = 0


            for i in range(len(proc_queue[t])):
                if proc[proc_queue[t][i]]['burst'] < proc[proc_queue[t][short]]['burst']:
                    short = i

            # move the shortest process to the top of the queue
            s = proc_queue[t].pop(short)
            proc_queue[t].insert(0, s)

            # process in progress
            executing = proc_queue[t][0]


    for x in range(len(proc)):
        proc[x]['progress'] = 0     # reset progress values
        proc[x]['start'] = 0        # reset start values

    # compute x values for gantt chart
    x_values = compute_x_values(proc)



    # for each process, add x-values and yrange
    for x in range(count):
        animation.append({"xranges": x_values[x], "yrange": y_ranges[x]})
    
    #print (animation)

    animate(y_points, y_labels, animation)

def arrivalSort(y):
    return y['arrival']    

def fcfs():

    global y_points

    # prepare the gantt chart axis
    before_algorithm()    

    # update y_values according to number of processes
    y_points = y_points[:count]

    # process names for the y-axis of the chart
    data.sort(key=arrivalSort)
    y_labels = []
    for p in range(count):
        y_labels.append(data[p]['name'])


    #print(data)
    animation = []
    x_values = []
    proc = []

    # store process indices and burst times
    for p in range(count):
        proc.append([p, data[p]['burst']])

    d = dict()
    
    for i in range(count):
        key = "P"+str(i+1)
        a = data[i]['arrival']#arrival time
        b = data[i]['burst'] #burst time
        l = []
        l.append(a)
        l.append(b)
        d[key] = l
    
    d = sorted(d.items(), key=lambda item: item[1][0])
    #print (d)
    
    ET = []
    for i in range(len(d)):
        # first process
        if(i==0):
            ET.append(d[i][1][1]+d[i][1][0])
    
    
        # get prevET + newBT
        else:
            diff=0
            if (d[i][1][0] >= ET[i-1]):

                diff = d[i][1][0]-ET[i-1]
            ET.append(ET[i-1] + d[i][1][1]+diff)


    gap = {}
    for y in range(count):

        proc_start = ET[y]-data[y]['burst']

        f=0
        gap[y] = []
        while f < proc_start:
        
            gap[y].append((0,0))
            if (y==0):

                proc_queue.append([])
            f+=1 

        for u in range(data[y]['burst']):
            proc_queue.append([y,y])

        for g in range(time_max):
            gap[y].append((proc_start,u+1))

    for x in range(count):
        animation.append({"xranges": gap[x], "yrange": y_ranges[x]})
    #print (animation)
     #   print([d[i][1][0],ET[x]])

    animate(y_points, y_labels, animation)

def prioritySchedule():
    proc = []
    animation = []
    global y_points
    x_values = []
    index={}
    executing = -1
    before_algorithm()

    #the process's burst time, arrival time, start time, progress and priority
    for i in range(count):
        proc.append({"index":i, "burst":data[i]['burst'], "arrival":data[i]['arrival'], "start":0, "progress":0, "priority":data[i] ["priority"]})
    

    for i in range(0, len(proc)-1):
        for j in range(0, len(proc)-i-1):
            if proc[j]['priority'] > proc[j+1]['priority']:
                proc[j], proc[j+1] = proc[j+1], proc[j]

    for t in range(time_max):
        if t == 0:
            proc_queue.append([])
        else:
            # copy previous state of the queue
            proc_queue.append(proc_queue[t-1][:])

        # add indices of arriving processes to the end of the queue
        for a in range(len(proc)):
            if proc[a]['arrival'] == t:
                proc_queue[t].append(a)

        # if process is currently being executed
        if executing != -1 and len(proc_queue[t]) > 0:
            proc[executing]['progress'] += 1

            # is process finihsed
            if proc[executing]['progress'] >= proc[executing]['burst']:
                proc_queue[t].pop(0)  # remove from top of queue
                executing = -1

        if executing == -1 and len(proc_queue[t]) > 0:
            # choose process with highest priority 
            priority = 0

            for i in range(len(proc_queue[t])):
                if proc[proc_queue[t][i]]['priority'] < proc[proc_queue[t][priority ]]['priority']:
                    priority  = i
            # move the shortest process to the top of the queue
            s = proc_queue[t].pop(priority )
            proc_queue[t].insert(0, s)

            # process in progress
            executing = proc_queue[t][0]

    print(proc_queue)

    for x in range(len(proc)):
        proc[x]['progress'] = 0     # reset progress values
        proc[x]['start'] = 0        # reset start values

    # compute x values for gantt chart
    x_values = compute_x_values(proc)

    print(x_values)

    # for each process, add x-values and yrange
    for x in range(count):
        animation.append({"xranges": x_values[x], "yrange": y_ranges[x]})

    animate(y_points, y_labels, animation)
# END OF shortest_job_next


def reset():
    global count
    global time
    global time_max
    global selected_algo
    global data
    global proc_queue

    global axes
    global y_points
    global y_labels
    global y_ranges
    #global x_ticks

    count = 0
    time = 0
    time_max = 0
    selected_algo = -1
    data = []
    proc_queue = []

    y_points = [2, 6, 10, 14, 18, 22, 26]
    y_labels = ['', '', '', '', '', '', '']
    y_ranges = [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4), (20, 4), (24, 4)]

    for i in table.get_children():
        table.delete(i)

    for i in q.get_children():
        q.delete(i)

    lbl_message_text.configure(text=message)
    lbl_clock.configure(text="00 : 00")

    axes.cla()
    axes.grid(True)
    axes.set_xlabel("Seconds")
    axes.set_title("Process Execution Timeline")
    axes.tick_params(left=False)
    x_ticks = np.arange(0, 61, 5)
    axes.set_xticks(x_ticks)
    axes.set_xlim(0, 60)
    axes.set_ylim(0, 32)
    axes.set_yticks(y_points)
    axes.set_yticklabels(y_labels)
    canvas.draw()
    canvas.flush_events()

    btn_SJN.config(relief="raised")
    btn_FCFS.config(relief="raised")
    btn_P.config(relief="raised")
    btn_RR.config(relief="raised")

    window.update()
# END OF reset

######################################################
# Code for the gui is below
######################################################
window = tk.Tk()
window.geometry('870x670')
window['bg'] = '#000000'

frm_banner = tk.Frame(master=window, height=100, bg="black")
lbl_title = tk.Label(
    master=frm_banner,
    text="CPU SCHEDULING ALGORITHMS",
    foreground="yellow",
    background="black",
    height=3,
    width=100
)
lbl_title.grid(row=0, column=0)

frm_banner.grid(row=0, column=0, padx=75, pady=10,
                columnspan=3, sticky=tk.W+tk.E)


# frame for the algorithm choice buttons
frm_algos = tk.Frame(master=window, height=100, bg="black")

btn_SJN = tk.Button(
    master=frm_algos,
    text="Shortest Job Next",
    width=28,
    height=2,
    bg="black",
    fg="white",
    command=select_SJN_algo
)
btn_SJN.grid(row=0, column=1)

btn_FCFS = tk.Button(
    master=frm_algos,
    text="First Come, First Serve",
    width=28,
    height=2,
    bg="black",
    fg="white",
    command = select_FCFS_algo
)
btn_FCFS.grid(row=0, column=2)

btn_P = tk.Button(
    master=frm_algos,
    text="Priority",
    width=28,
    height=2,
    bg="black",

    fg="white",
    command = select_priority_algo

)
btn_P.grid(row=0, column=3)

btn_RR = tk.Button(
    master=frm_algos,
    text="Round Robin",
    width=28,
    height=2,
    bg="black",
    fg="white",
    command = select_RR_algo
)
btn_RR.grid(row=0, column=4)

frm_algos.grid(row=1, column=0, padx=24, pady=10,
               columnspan=3, sticky=tk.W+tk.E)


# table  for inputs
table = ttk.Treeview(window, height=7)
table.grid(row=2, column=0, pady=10, padx=30)

table['columns'] = ('name', 'arrival', 'burst', 'priority')

table.column("#0", width=0, stretch='no')
table.column("name", anchor='center', width=90)
table.column("arrival", anchor='center', width=90)
table.column("burst", anchor='center', width=90)
table.column("priority", anchor='center', width=90)

table.heading("#0", text="", anchor='center')
table.heading("name", text="Process name", anchor='center')
table.heading("arrival", text="Arrival time", anchor='center')
table.heading("burst", text="Burst time", anchor='center')
table.heading("priority", text="Priority", anchor='center')

frm_input = tk.Frame(master=window, height=5, bg="black")
frm_input.grid(row=3, column=0, pady=10)

# labels
lbl_name = tk.Label(master=frm_input, text="Process name",
                    fg="yellow", bg="black", width=13)
lbl_name.grid(row=0, column=0)

lbl_arrival = tk.Label(master=frm_input, text="Arrival time",
                       fg="yellow", bg="black", width=13)
lbl_arrival.grid(row=0, column=1)

lbl_burst = tk.Label(master=frm_input, text="Burst time",
                     fg="yellow", bg="black", width=13)
lbl_burst.grid(row=0, column=2)

lbl_priority = tk.Label(master=frm_input, text="Priority",
                        fg="yellow", bg="black", width=13)
lbl_priority.grid(row=0, column=3)

lbl_time = tk.Label(master=frm_input, text="Time Slice",
                        fg="yellow", bg="black", width=13)
lbl_time.grid(row=0, column=4)
# entry fields
ent_name = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_name.grid(row=1, column=0)

ent_arrival = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_arrival.grid(row=1, column=1)

ent_burst = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_burst.grid(row=1, column=2)

ent_priority = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_priority.grid(row=1, column=3)
ent_time = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_time.grid(row=1, column=4)


# frame for control buttons
frm_btns = tk.Frame(master=window)

btn_add = ttk.Button(
    master=frm_btns,
    text="ADD",
    command=add
)
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_remove = ttk.Button(
    master=frm_btns,
    text="REMOVE",
    command=remove
)
btn_remove.grid(row=0, column=1, padx=5, pady=5)

btn_run = ttk.Button(
    master=frm_btns,
    text="RUN",
    command=run
)
btn_run.grid(row=0, column=2, padx=5, pady=5)

frm_btns.grid(row=4, column=0, pady=10)


# table  for process queue
q = ttk.Treeview(window, height=7)
q.grid(row=2, column=1, pady=10)

q['columns'] = ('process')

q.column("#0", width=0, stretch='no')
q.column("process", anchor='center', width=100)

q.heading("#0", text="", anchor='center')
q.heading("process", text="Process Queue", anchor='center')


# system clock
lbl_clock = tk.Label(
    text="00 : 00",
    foreground="yellow",
    background="black",
    height=2,
    width=20
)
lbl_clock.grid(row=4, column=1, pady=10)
lbl_clock.config(font=('Helvetica bold', 15))

# message area
frm_message = tk.Frame(master=window, bg="black")

frm_message.grid(row=2, column=2, pady=10, sticky=tk.W+tk.N)

lbl_message_text = tk.Message(
    master=frm_message,
    text=message,
    foreground="yellow",
    background='black'
)
lbl_message_text.grid(row=0, column=0)

# reset button
btn_reset = ttk.Button(
    text="RESET",
    command=reset
)
btn_reset.grid(row=3, column=2)


# frame for timeline for process execution
frm_timeline = tk.Frame(master=window, bg="black")

axes.grid()
# embed our figure to the frame
canvas = FigureCanvasTkAgg(fig, frm_timeline)
canvas.get_tk_widget().grid(row=0, column=0)

frm_timeline.grid(row=5, column=0, columnspan=3,
                  sticky=tk.W+tk.E, pady=10, padx=9)

####### STYLE #######
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='yellow', foreground='black',
                width=10, height=1, borderwidth=2, focusthickness=3, focuscolor='none')

window.mainloop()
