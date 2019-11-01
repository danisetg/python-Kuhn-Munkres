from queue import Queue
class Khun:
    def __init__(self, n, g):
        #quantity of nodes
        self.n = n
        #adjacence matrix
        self.g = g
        #Tags array for Xs and Ys
        self.lx = list()
        self.ly = list()
        #graph in the same form that g, but keeping just the edges where l[x] + l[y] == a[x][y]
        self.gl = list()
        #matching array in the form of m[a] = b
        self.m = list()
        #boolean array of saturated nodes
        self.saturated = list()
        #set s for the kuhn algorithm
        self.s = list()
        #set t for the kuhn algorithm
        self.t = list()
        #initialize all values
        for i in range(self.n):
            self.lx.append(0)
            self.ly.append(0)
            self.gl.append(list())
            self.saturated.append(False)
            self.saturated.append(False)
            self.m.append(-1)
            self.m.append(-1)

    #solve the problem
    def solve(self):
        self.initTagNodes()
        self.buildGl()
        self.buildRandomM()
        return self.step1()

    #tags the node with the maximum cost of its edges if belongs to X
    def initTagNodes(self):
        for x in range(self.n):
            self.lx[x] = max(self.g[x])
    
    #Builds the array Gl
    def buildGl(self):
        self.gl = list()
        for x in range (self.n):
            self.gl.append(list())
            for y in range(self.n):
                if self.lx[x] + self.ly[y] == self.g[x][y]:
                    self.gl[x].append(y + self.n)
    
    def buildRandomM(self):
        self.saturated = [False]*(2*self.n)
        self.m = [-1]*(2*self.n)
        for x in range(self.n):
            for y in self.gl[x]:
                if not self.saturated[y]:
                    self.saturated[x] = True
                    self.saturated[y] = True
                    self.m[x] = y
                    self.m[y] = x
                    break
    
    def step1(self):
        #if the matching is m-saturated, then it's perfect and the solution is in m
        if self.isMSaturated():
            return self.m
        self.t = list()
        self.s = list()
        for x in range(self.n):
            if not self.saturated[x]:
                self.s.append(x)
                break
        return self.step2()
    
    def step2(self):
        if set(self.t) == set(self.findNeighbors()):
            alpha = self.calculateAlpha()
            self.recalculateL(alpha)
            self.buildGl()
            self.buildRandomM()
            return self.step1()
        return self.step3()
        
    def step3(self):
        for x in self.s:
            for y in self.gl[x]:
                if not y in self.t:
                    self.t.append(y)
                    if not self.m[y] in self.s:
                        self.s.append(self.m[y])
                    if self.saturated[y]:
                        return self.step2()
                    else:
                        self.getAugmentingPath(y)
                        return self.step1()

        

    def isMSaturated(self):
        for x in range(self.n):
            if not self.saturated[x]:
                return False
        return True

    def findNeighbors(self):
        n = list()
        taken = [False]*(2*self.n)
        for x in self.s:
            for y in self.gl[x]:
                if not taken[y]:
                    n.append(y)
                    taken[y] = True
        return n
    
    def calculateAlpha(self):
        alpha = 999999999
        for x in self.s:
            for y in range(self.n):
                if not (y+self.n) in self.t:
                    alpha = min(alpha, self.lx[x] + self.ly[y] - self.g[x][y])
        return alpha
    
    def recalculateL(self, alpha):
        for x in self.s:
            self.lx[x] -= alpha
        for y in self.t:
            self.ly[y-self.n] += alpha

    def getAugmentingPath(self, y):
        parent = [-1]*(2*self.n)
        visited = [False]*(2*self.n)
        queue = Queue(2*self.n)
        visited[self.s[0]] = True
        queue.put(self.s[0])
        while not queue.empty():
            v = queue.get()
            if v >= self.n:
                if not visited[self.m[v]]:
                    queue.put(self.m[v])
                    visited[self.m[v]] = True
                    parent[self.m[v]] = v
            else:
                for node in self.gl[v]:
                    if not visited[node]:
                        visited[node] = True
                        parent[node] = v
                        queue.put(node)
                        if node == y:
                            while not parent[node] == -1:
                                if node >= self.n:
                                    self.m[parent[node]] = node
                                    self.saturated[parent[node]] = True
                                    self.saturated[node] = True
                                node = parent[node]
                            return

        





