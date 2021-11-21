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
proc_queue = []         # process queue
q_lineup = []           # process ids and their arrival times

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


# Plotting the graph inside a Figure
fig = Figure(figsize=(7.85, 2), dpi=100)
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

"""
# values for the animation
# xrange - (x-position of rectancle, width of rectangle)
# yrange - (y-position of rectancle, height of rectangle)
algo_values = [
    {"xranges": [(1, 1), (4, 0), (6, 2), (11, 5)], "yrange": (0, 4)},
    {"xranges": [(0, 5), (5, 0), (5, 0), (5, 0)], "yrange": (4, 4)},
    {"xranges": [(5, 2), (7, 2), (9, 2), (9, 0)], "yrange": (8, 4)},
    {"xranges": [(6, 4), (10, 0), (10, 0), (10, 2)], "yrange": (12, 4)},
    {"xranges": [(11, 4), (20, 2), (15, 6), (23, 5)], "yrange": (16, 4)},
    {"xranges": [(3, 1), (6, 2), (18, 10), (30, 1)], "yrange": (20, 4)},
    {"xranges": [(1, 4), (7, 15), (23, 2), (30, 10)], "yrange": (24, 4)}
]
"""

######################################################
# Code for the functions is below
######################################################


def add():
    # add process info to the table
    global count
    # prevent entering if required entries are blank
    if len(ent_name.get()) != 0 and  len(ent_arrival.get()) != 0 and len(ent_burst.get()) != 0: 
    #if an algorithm is not selected, then do not add anything
        if selected_algo != -1:
            if(count < proc_max+1):
                table.insert(parent='', index='end', iid=count, text='', values=(
                    ent_name.get(), ent_arrival.get(), ent_burst.get(), ent_priority.get()))
                count += 1

                if(selected_algo == algos[0]):
                    # add data for shortest job next
                    fin_time = int(ent_arrival.get()) + int(ent_burst.get())
                    data.append({"name": ent_name.get(), "arrival": int(ent_arrival.get()),
                                "burst": int(ent_burst.get())})
                    # print(data)

                ent_name.delete(0, tk.END)
                ent_arrival.delete(0, tk.END)
                ent_burst.delete(0, tk.END)
                ent_priority.delete(0, tk.END)


def remove():
    # remove selected process from table and from stored data
    
    selected = table.focus()
    # prevent trying to remove when nothing is slected in table
    if selected:
        # remove value from data list
        del data[int(selected)]
        table.delete(selected)
    


    


def run():
    if(selected_algo == algos[0]):
        total_time()
        shortest_job_next()


def animate(y_points, y_labels, animation):
    global axes

    ani_x_values = [[], [], [], [], [], [], []]

    for i in range(time_max):
        # for each time unit
        advance_time()

        for p in range(count):
            # for each process
            # TO DO remove finished process if fin value is eqal to i

            # values for the animation
            # xrange - (x-position of rectancle, width of rectangle)
            # yrange - (y-position of rectancle, height of rectangle)
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


def forget(widget):
  widget.grid_forget()
# shows relevant entry


def select_SJN_algo():
    global selected_algo

    selected_algo = "SJN"
    forget(ent_priority)
    forget(ent_time)
    forget(lbl_priority)
    forget(lbl_time)
    displaycolumns=[]
    for col in table["columns"]:
      if col != "priority":
        displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns
    
   

def select_RR_algo():
    global selected_algo


    selected_algo = "RR"
    forget(ent_priority)
    forget(lbl_priority)
    lbl_time.grid(row=0, column=4)
    ent_time.grid(row=1, column=4)
    displaycolumns=[]
    for col in table["columns"]:
      if col != "priority":
        displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns
    
    
    

def select_priority_algo():
    global selected_algo
    selected_algo = "P"
    ent_priority.grid(row=1, column=3)
    lbl_priority.grid(row=0, column=3)
    forget(lbl_time)
    forget(ent_time)
    displaycolumns=[]
    for col in table["columns"]:
      displaycolumns.append(col)
    table["displaycolumn"]=displaycolumns

def select_FcFs_algo():
  global selected_algo

  selected_algo = "FCFS"
  forget(ent_priority)
  forget(ent_time)
  forget(lbl_priority)
  forget(lbl_time)
  displaycolumns=[]
  for col in table["columns"]:
    if col != "priority":
      displaycolumns.append(col)
  table["displaycolumn"]=displaycolumnsk"


def advance_time():
    global time
    global q_lineup

    time += 1
    # TO DO update system clock display
    # TO DO add arriving process name to queue display
    # TO DO add arriving process number to proc_queue


def total_time():
    global time_max
    # store largest arrival time
    t = 0
    for p in range(len(data)):
        t += data[p]['burst']
    time_max = t


def add_to_queue(proc_name):
    global proc_queue
    # TO DO add process names to bottom of queue display based on time
    # TO DO add process number to proc_queue
    pass


def update_queue():
    global proc_queue
    # TO DO reorder queue disply according to priority when  new process arrives
    # TO DO remove finished processes based on their progress status from display as well as proc_queue
    pass


def is_queue_empty():
    return len(proc_queue) == 0


def calc_queue_lineup():
    global q_lineup
    # TO DO update q_lineup with sublists of arrival times and process numbers [ [0], [3,4] ]
    pass


def shortest_job_next():
    global y_points

    # update y_values according to number of processes
    y_points = y_points[:count]

    # process names for the y-axis of the chart
    y_labels = []
    for p in range(count):
        y_labels.append(data[p]['name'])

    animation = []
    x_values = []
    proc = []

    # store process indices and burst times
    for p in range(count):
        proc.append([p, data[p]['burst']])

    # sort processes based on burst times using bubble sort
    for i in range(0, len(proc)-1):
        for j in range(0, len(proc)-i-1):
            if proc[j][1] > proc[j+1][1]:
                proc[j], proc[j+1] = proc[j+1], proc[j]

    # calculate new start and end times
    new_times = []
    start = 0
    for r in range(len(proc)):
        # [process index, start, end]
        if r == 0:
            new_times.append([proc[r][0], 0, proc[r][1]])
            start = proc[r][1]    # add first processes end time
        else:
            end = start + proc[r][1]
            new_times.append([proc[r][0], start, end])
            start = end

    print(new_times)

    # compute list of x values for the animation
    for x in range(len(proc)):
        # for each process
        p = []
        steps = 1
        for t in range(1, time_max + 1):
            # for each time unit
            if t <= new_times[x][1]:
                # process has not arrived
                p.append((0, 0))
            elif t == new_times[x][1]:
                # process has arrived

                p.append((t, steps))
                steps += 1
            elif t > new_times[x][1]:
                if t <= new_times[x][2]:
                    # process in progress

                    p.append((new_times[x][1], steps))
                    steps += 1
                elif t > new_times[x][2]:
                    # process is finished
                    p.append((new_times[x][1], new_times[x][2]))

        x_values.append(p)

    print(x_values)

    # for each process, add x-values and yrange
    for x in range(count):
        animation.append({"xranges": x_values[x], "yrange": y_ranges[x]})

    animate(y_points, y_labels, animation)


######################################################
# Code for the gui is below
######################################################
window = tk.Tk()
window.geometry('800x670')
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

frm_banner.grid(row=0, column=0, padx=30, pady=10,
                columnspan=2, sticky=tk.W+tk.E)


# frame for the algorithm choice buttons
frm_algos = tk.Frame(master=window, height=100, bg="black")

btn_SJN = tk.Button(
    master=frm_algos,
    text="Shortest Job Next",
    width=25,
    height=2,
    bg="black",
    fg="white",
    command=select_SJN_algo
)
btn_SJN.grid(row=0, column=1)

btn_FCFS = tk.Button(
    master=frm_algos,
    text="First Come, First Serve",
    width=25,
    height=2,
    bg="black",
    fg="white",
    command=select_FcFs_algo
)
btn_FCFS.grid(row=0, column=2)

btn_P = tk.Button(
    master=frm_algos,
    text="Priority",
    width=25,
    height=2,
    bg="black",
    fg="white",
    command=select_priority_algo
)
btn_P.grid(row=0, column=3)

btn_RR = tk.Button(
    master=frm_algos,
    text="Round Robin",
    width=25,
    height=2,
    bg="black",
    fg="white",
    command=select_RR_algo
)
btn_RR.grid(row=0, column=4)

frm_algos.grid(row=1, column=0, padx=30, pady=10,
               columnspan=2, sticky=tk.W+tk.E)


# table  for inputs
table = ttk.Treeview(window, height=7)
table.grid(row=2, column=0, pady=10)

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
                    fg="black", bg="white", width=13)
lbl_name.grid(row=0, column=0)

lbl_arrival = tk.Label(master=frm_input, text="Arrival time",
                       fg="black", bg="white", width=13)
lbl_arrival.grid(row=0, column=1)

lbl_burst = tk.Label(master=frm_input, text="Burst time",
                     fg="black", bg="white", width=13)
lbl_burst.grid(row=0, column=2)

lbl_priority = tk.Label(master=frm_input, text="Priority",
                        fg="black", bg="white", width=13)
lbl_priority.grid(row=0, column=3)

# entry fields
ent_name = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_name.grid(row=1, column=0)

ent_arrival = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_arrival.grid(row=1, column=1)

ent_burst = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_burst.grid(row=1, column=2)

ent_priority = tk.Entry(master=frm_input, fg="black", bg="white", width=10)
ent_priority.grid(row=1, column=3)


# frame for control buttons
frm_btns = tk.Frame()

btn_add = tk.Button(
    master=frm_btns,
    text="ADD",
    width=10,
    height=1,
    bg="yellow",
    fg="black",
    command=add
)
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_remove = tk.Button(
    master=frm_btns,
    text="REMOVE",
    width=10,
    height=1,
    bg="yellow",
    fg="black",
    command=remove
)
btn_remove.grid(row=0, column=1, padx=5, pady=5)

btn_run = tk.Button(
    master=frm_btns,
    text="RUN",
    width=10,
    height=1,
    bg="yellow",
    fg="black",
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
lbl_clock_title = tk.Label(
    text="SYSTEM CLOCK",
    foreground="black",
    background="yellow",
    height=2,
    width=20
)
lbl_clock_title.grid(row=3, column=1, pady=10)

lbl_clock = tk.Label(
    text="time",
    foreground="yellow",
    background="black",
    height=2,
    width=20
)
lbl_clock.grid(row=4, column=1, pady=10)


# frame for timeline for process execution
frm_timeline = tk.Frame(master=window, bg="black")

axes.grid()
# embed our figure to the frame
canvas = FigureCanvasTkAgg(fig, frm_timeline)
canvas.get_tk_widget().grid(row=0, column=0)

frm_timeline.grid(row=5, column=0, columnspan=2,
                  sticky=tk.W+tk.E, pady=10, padx=7)


window.mainloop()
