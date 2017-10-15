from geometry import *
import random
import math

class node:
    def __init__(self, label):
        self.label = label
        self.pos = zerovector()
        self.visiblerefs = 0
        self.depth = 0
        self.children = []
        self.parents = []
        self.bounceguard = 1
    def add_child(self,c):
        self.children.append(c)
    def add_parent(self,p):
        self.parents.append(p)
    def calc_depth(self):
        best = self.depth
        for p in self.parents:
            if best < p.depth + 1:
                best = p.depth + 1
        res = self.depth == best
        self.depth = best
        return res
    def calc_position(self,dist):
        if len(self.parents) == 0:
            self.visiblerefs = max(self.visiblerefs, 1)
            return
        ref = self.parents[0]
        for p in self.parents:
            if p.visiblerefs > 0:
                ref = p
        self.pos = vector(ref.pos[0] + random.random()*dist*0.5, ref.pos[1] + dist + random.random()*dist*0.2)

class clockwork:
    def sanitize(rsn, a):
        if math.isnan(a[0]) or math.isnan(a[1]):
            return zerovector()
        return a
    def too_near(cf, a, b, dist):
        vec = b.pos - a.pos
        l = length(vec)
        if l < dist:
            desiredlength = (dist - l)*cf
            return clockwork.sanitize("too near", scale_to(vec, desiredlength))
        return zerovector()
    def too_far(cf, a, b, dist):
        maxdist = math.sqrt(len(a.children))*2*dist
        vec = b.pos - a.pos
        l = length(vec)
        if l > maxdist:
            desiredlength = (l - maxdist)*cf
            return clockwork.sanitize("too far", -scale_to(vec, desiredlength))
        return zerovector()
    def spring(cf, a, b, dist):
        vec = b.pos - a.pos
        l = length(vec)
        desiredpos = scale_to(vec, dist)
        res = (desiredpos - vec)*(float(cf))
        return clockwork.sanitize("spring", res)
    def order(cf,a, b, dist):
        if a.pos[1] + dist > b.pos[1]:
            return clockwork.sanitize("order", vector(0.0, a.pos[1] + dist - b.pos[1])*cf)
        return zerovector()
    def new_position(nodes, n, cf, dist, clamp):
        acum = zerovector()
        for p in n.parents:
            if p.visiblerefs > 0:
                acum += clockwork.too_far(cf, p, n, dist)*0
                acum += clockwork.spring(cf, p, n, dist)*0.2
                acum += clockwork.order(cf, p, n, dist)
        for c in n.children:
            if c.visiblerefs > 0:
                acum += clockwork.spring(cf, c, n, dist)*0.4
        for m in nodes:
            if m.visiblerefs > 0:
                acum += clockwork.too_near(cf, m, n, dist)*0.4
        l = len(acum)
        if l > clamp :
            return scale_to(acum, clamp)
        return acum


class digraph:
    def __init__(self):
        self.mapping = {}
        self.nodes = []
        self.edges = []
        self.selectednode = None
        return
    def add_node(self, name):
        if name not in self.mapping:
            n = node(name)
            self.mapping[name] = n
            self.nodes.append(n)
    def add_edge(self, a, b):
        self.add_node(a)
        self.add_node(b)
        self.edges.append([self.mapping[a],self.mapping[b]])
        self.mapping[a].add_child(self.mapping[b])
        self.mapping[b].add_parent(self.mapping[a])
    def init_depth(self,dist):
        for i in range(20):
            for n in self.nodes:
                n.calc_depth()
                n.calc_position(dist)
    def select(self,pos):
        bestnode = None
        bestdist = 1000000000
        for n in self.nodes:
            dist = length(pos - n.pos)
            if dist < bestdist and n.visiblerefs > 0:
                bestdist = dist
                bestnode = n
        self.selectednode = bestnode
    def foldat(self, n, by, depth):
        if depth > 0:
            n.visiblerefs = max(0, n.visiblerefs + by)
            for i in range(len(n.children)):
                m = n.children[i]
                if by > 0 and m.visiblerefs == 0:
                    m.pos = n.pos + vector(depth*5*i,20)
                self.foldat(m, by, depth - 1)
    def fold(self, d):
        self.foldat(self.selectednode, -1, 1000)
        self.selectednode.visiblerefs += 1
    def unfold(self, d):
        self.selectednode.bounceguard = 0.1
        self.foldat(self.selectednode, 1, d+1)
        self.selectednode.visiblerefs -= 1
    def from_file(self, fn):
        with open(fn) as f:
            lines = f.read().splitlines()
        for line in lines:
            if line.find("->") >= 0:
                tokens = line.replace("\"","").replace(" ","").split("->")
                for i in range(len(tokens)-1):
                    self.add_edge(tokens[i], tokens[i+1])
    def reposition(self, dist, cf, clamp):
        for n in self.nodes:
            if n.visiblerefs > 0 and len(n.parents) != 0:
                n.pos += n.bounceguard*clockwork.new_position(self.nodes, n, cf, dist, clamp)
                n.bounceguard = (n.bounceguard + 1)/2

def test_graph(dist):
    g = digraph()
    g.add_edge("a", "b")
    g.init_depth(dist)
    return g

