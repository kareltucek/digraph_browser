from tkinter import *
import numpy as np
import math
from geometry import *
from graph import *
from functions import *
import time

graph_noderadius = 70
graph_nodewidth = 50
graph_nodeoffset = 3*graph_noderadius
graph_arrowheadradius = 5
graph_folddepth = 2
graph_maxstep = 5
graph_stepratio = 0.2

width = 1000
height = 1000

viewpos = zerovector()
viewscale = 1
current_mousepos = zerovector()
mousepos = zerovector()

loaded_graph = test_graph(graph_nodeoffset)

def key(event):
    print("key fired")
    if e.char == 'r':
        reposition()

def mouse_motion(event):
    global current_mousepos
    current_mousepos = vector(event.x, event.y)

def mouse_down_middle(event):
    global mousepos
    mousepos = vector(event.x, event.y)

def mouse_down_left(event):
    global mousepos
    mousepos = vector(event.x, event.y)
    center = vector(width/2, height/2)
    worldpos = viewpos + (mousepos-center)/viewscale
    loaded_graph.select(worldpos)
    loaded_graph.unfold(graph_folddepth)
    full_redraw()
    reposition()

def mouse_down_right(event):
    global mousepos
    mousepos = vector(event.x, event.y)
    center = vector(width/2, height/2)
    worldpos = viewpos + (mousepos-center)/viewscale
    loaded_graph.select(worldpos)
    loaded_graph.fold(graph_folddepth)
    full_redraw()
    reposition()

def mouse_wheel(event):
    global viewpos
    global viewscale
    global mousepos
    global current_mousepos
    center = vector(width/2, height/2)
    oldpos = viewpos + (current_mousepos-center)/viewscale
    if event.num == 5 or event.delta == -120:
        viewscale /= 1.3
    if event.num == 4 or event.delta == 120:
        viewscale *= 1.3
    newpos = viewpos + (current_mousepos-center)/viewscale
    viewpos = viewpos - (newpos - oldpos)
    full_redraw()

def mouse_move(event):
    global viewpos
    global viewscale
    global mousepos
    lastpos = mousepos
    mousepos = vector(event.x, event.y)
    diff = mousepos - lastpos
    viewpos = -diff/viewscale + viewpos
    full_redraw()

def show_window():
    master = Tk()
    w = Canvas(master, 
               width=width,
               height=height)
    w.bind("<Button-1>", mouse_down_left)
    w.bind("<Button-2>", mouse_down_middle)
    w.bind("<Button-3>", mouse_down_right)
    #w.bind("<Button-3>", reset)
    w.bind("<Motion>", mouse_motion)
    w.bind("<B2-Motion>", mouse_move)
    #w.bind("<B2-Motion>", mouse_rot)
    w.bind("<MouseWheel>", mouse_wheel)
    w.bind("<Button-4>", mouse_wheel)
    w.bind("<Button-5>", mouse_wheel)
    w.bind("<Key>", key)
    w.pack()
    w.create_line(1, 1, width, 1)
    w.create_line(1, height, width, height)
    w.create_line(1, 1, 1, height)
    w.create_line(width, 1, width, height)
    return w

def flipy(y):
    global viewpos
    global viewscale
    return height/2 + (y - viewpos[1])*viewscale

def flipx(x):
    global viewpos
    global viewscale
    return width/2 + (x - viewpos[0])*viewscale

def draw_segment(fr, to, c = "black"):
    w.create_line(flipx(fr[0]), flipy(fr[1]), flipx(to[0]), flipy(to[1]), fill=c)

def draw_circle(pt, rad, c = "black"):
    w.create_oval(flipx(pt[0]-rad), flipy(pt[1]-rad), flipx(pt[0]+rad), flipy(pt[1]+rad), outline=c)

def draw_pt(pt, rad, c = "black"):
    w.create_oval(flipx(pt[0])-rad, flipy(pt[1])-rad, flipx(pt[0])+rad, flipy(pt[1])+rad, outline=c)

def clear():
    w.delete("all")

def draw_edge(a, b):
    vec = b.pos - a.pos
    rad = scale_to(vec, graph_noderadius)
    p1 = a.pos + rad
    p2 = b.pos - rad
    draw_circle(p2, graph_arrowheadradius)
    draw_segment(p1, p2, "black")

def draw_node(n):
    global viewscale
    if n.visiblerefs > 0:
        hasinvisible = False
        for m in n.children:
            if m.visiblerefs > 0:
                draw_edge(n, m)
            else:
                hasinvisible = True
        color = fold(hasinvisible, "black", "red")
        draw_circle(n.pos, graph_noderadius, color);
        w.create_text(flipx(n.pos[0]), flipy(n.pos[1]), text=n.label, width=graph_nodewidth*viewscale)

def draw_graph(graph):
    for n in graph.nodes:
        draw_node(n)

def clear():
    w.delete("all")

def full_redraw():
    global loaded_graph
    clear()
    draw_graph(loaded_graph)
	
def init_window():
    global w
    w = show_window()
    full_redraw()

def load_graph(fn):
    global loaded_graph
    loaded_graph = digraph()
    loaded_graph.from_file(fn)
    loaded_graph.init_depth(graph_nodeoffset)
    
def reposition():
    print("repositioning")
    for i in range(40):
        loaded_graph.reposition(graph_nodeoffset, graph_stepratio, graph_maxstep)
        full_redraw()
        w.update()
        time.sleep(1/10)

