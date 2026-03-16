import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time
import threading

SIZE = 4

goal = (1,2,3,4,
        5,6,7,8,
        9,10,11,12,
        13,14,15,16)


# ---------------- HEURISTIC ----------------
def manhattan(state):

    distance = 0

    for i in range(16):

        value = state[i]
        goal_index = goal.index(value)

        x1,y1 = divmod(i,4)
        x2,y2 = divmod(goal_index,4)

        distance += abs(x1-x2)+abs(y1-y2)

    return distance


# ---------------- ROTATIONS ----------------
def rotate_row_left(state,row):

    s=list(state)
    start=row*4

    r=s[start:start+4]
    r=r[1:]+r[:1]

    s[start:start+4]=r

    return tuple(s)


def rotate_row_right(state,row):

    s=list(state)
    start=row*4

    r=s[start:start+4]
    r=r[-1:]+r[:-1]

    s[start:start+4]=r

    return tuple(s)


def rotate_col_up(state,col):

    s=list(state)

    c=[s[col+i*4] for i in range(4)]
    c=c[1:]+c[:1]

    for i in range(4):
        s[col+i*4]=c[i]

    return tuple(s)


def rotate_col_down(state,col):

    s=list(state)

    c=[s[col+i*4] for i in range(4)]
    c=c[-1:]+c[:-1]

    for i in range(4):
        s[col+i*4]=c[i]

    return tuple(s)


# ---------------- NEIGHBORS ----------------
def neighbors(state):

    moves=[]

    for r in range(4):
        moves.append(rotate_row_left(state,r))
        moves.append(rotate_row_right(state,r))

    for c in range(4):
        moves.append(rotate_col_up(state,c))
        moves.append(rotate_col_down(state,c))

    return moves


# ---------------- A* SEARCH ----------------
def astar(start):

    pq=[]
    heapq.heappush(pq,(0,start,[]))

    visited=set()

    while pq:

        cost,state,path=heapq.heappop(pq)

        if state==goal:
            return path

        if state in visited:
            continue

        visited.add(state)

        for n in neighbors(state):

            new_cost=len(path)+1
            priority=new_cost+manhattan(n)

            heapq.heappush(pq,(priority,n,path+[n]))

    return None


# ---------------- PUZZLE CLASS ----------------
class Puzzle:

    def __init__(self,root):

        self.root=root
        self.root.title("Sixteen Puzzle")

        self.board=list(goal)

        random.shuffle(self.board)

        self.steps=0

        self.start_time=None
        self.timer_running=False
        self.elapsed_time=0

        top=tk.Frame(root)
        top.pack(pady=10)

        self.info=tk.Label(top,text="Steps: 0 | Time: 0s",font=("Arial",14))
        self.info.pack()

        self.frame=tk.Frame(root)
        self.frame.pack()

        self.cells=[]

        for r in range(4):

            row=[]

            tk.Button(self.frame,text="←",width=3,
                      command=lambda r=r:self.row_left(r)).grid(row=r+1,column=0)

            for c in range(4):

                label=tk.Label(
                    self.frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial",20),
                    bg="#d9e6f2",
                    borderwidth=2,
                    relief="solid"
                )

                label.grid(row=r+1,column=c+1,padx=3,pady=3)

                row.append(label)

            tk.Button(self.frame,text="→",width=3,
                      command=lambda r=r:self.row_right(r)).grid(row=r+1,column=5)

            self.cells.append(row)

        for c in range(4):

            tk.Button(self.frame,text="↑",width=3,
                      command=lambda c=c:self.col_up(c)).grid(row=0,column=c+1)

            tk.Button(self.frame,text="↓",width=3,
                      command=lambda c=c:self.col_down(c)).grid(row=5,column=c+1)

        controls=tk.Frame(root)
        controls.pack(pady=10)

        tk.Button(controls,text="Shuffle",width=10,
                  command=self.shuffle).grid(row=0,column=0,padx=5)

        tk.Button(controls,text="AI Solve",width=10,
                  command=self.start_ai_thread).grid(row=0,column=1,padx=5)

        self.draw()
        self.update_timer()


# ---------------- DRAW ----------------
    def draw(self):

        for i in range(16):

            r=i//4
            c=i%4

            self.cells[r][c]["text"]=self.board[i]


# ---------------- TIMER ----------------
    def update_timer(self):

        if self.timer_running and self.start_time is not None:
            self.elapsed_time=int(time.time()-self.start_time)

        self.info.config(text=f"Steps: {self.steps} | Time: {self.elapsed_time}s")

        self.root.after(1000,self.update_timer)


# ---------------- START TIMER ----------------
    def start_timer_if_needed(self):

        if not self.timer_running:

            self.start_time=time.time()
            self.timer_running=True


# ---------------- CHECK SOLVED ----------------
    def check_solved(self):

        if tuple(self.board)==goal:

            if self.timer_running:
                self.elapsed_time=int(time.time()-self.start_time)

            self.timer_running=False

            messagebox.showinfo(
                "Puzzle Solved",
                f"Human solved puzzle!\n\nSteps: {self.steps}\nTime: {self.elapsed_time}s"
            )


# ---------------- MOVES ----------------
    def row_left(self,r):

        self.start_timer_if_needed()

        start=r*4
        row=self.board[start:start+4]

        row=row[1:]+row[:1]

        self.board[start:start+4]=row

        self.steps+=1

        self.draw()
        self.check_solved()


    def row_right(self,r):

        self.start_timer_if_needed()

        start=r*4
        row=self.board[start:start+4]

        row=row[-1:]+row[:-1]

        self.board[start:start+4]=row

        self.steps+=1

        self.draw()
        self.check_solved()


    def col_up(self,c):

        self.start_timer_if_needed()

        col=[self.board[c+i*4] for i in range(4)]

        col=col[1:]+col[:1]

        for i in range(4):
            self.board[c+i*4]=col[i]

        self.steps+=1

        self.draw()
        self.check_solved()


    def col_down(self,c):

        self.start_timer_if_needed()

        col=[self.board[c+i*4] for i in range(4)]

        col=col[-1:]+col[:-1]

        for i in range(4):
            self.board[c+i*4]=col[i]

        self.steps+=1

        self.draw()
        self.check_solved()


# ---------------- SHUFFLE ----------------
    def shuffle(self):

        random.shuffle(self.board)

        self.steps=0
        self.start_time=None
        self.timer_running=False
        self.elapsed_time=0

        self.draw()


# ---------------- AI THREAD START ----------------
    def start_ai_thread(self):

        thread=threading.Thread(target=self.solve_ai)
        thread.start()


# ---------------- AI SOLVE ----------------
    def solve_ai(self):

        start=tuple(self.board)

        ai_start=time.time()

        path=astar(start)

        if path:

            ai_steps=len(path)

            for state in path:

                self.board=list(state)

                self.draw()
                self.root.update()
                self.root.after(200)

            ai_time=int(time.time()-ai_start)

            messagebox.showinfo(
                "AI Solved",
                f"AI solved puzzle!\n\nSteps: {ai_steps}\nTime: {ai_time}s"
            )


# ---------------- MAIN ----------------
root=tk.Tk()
game=Puzzle(root)
root.mainloop()