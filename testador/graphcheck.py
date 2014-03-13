# encoding: utf-8

from collections import deque

class Graph:
    def __init__(self, V, E, directed=True):
        self.V = V
        self.E = E
        self.directed = directed
        self._cost = {}
        self._adj = {}
        for u in self.V:
            self._adj[u] = set()
        for u, v, w in self.E:
            self._cost[(u, v)] = w
            self._adj[u].add(v)
            if not directed:
                self._cost[(v, u)] = w
                self._adj[v].add(u)

    def adj(self, u):
        return self._adj[u]

    def cost(self, u, v):
        return self._cost[(u, v)]

    def is_adj(self, u, v):
        return (u, v) in self._cost

def parse_tgf(lines, directed=True):
    def edge(u, v, w = None):
        return u, v, (int(w) if w != None else None)
    sharp = lines.index('#')
    V = lines[:sharp]
    edges = [line.split() for line in lines[sharp + 1:]]
    E = set(edge(*e) for e in edges)
    return Graph(V, E, directed)

def parse_tgf_undirected(lines):
    return parse_tgf(lines, directed=False)

class ParseError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


# BFS
def bfs_parse(lines):
    d = {}
    for line in lines:
        values = line.split()
        if len(values) != 3:
            raise ParseError(u"formatação: linha não tem 3 valores: " + line)
        u, v, _d = values
        if (u, v) in d:
            raise ParseError(u"formatação: aresta repetida: " + u + " " + v)
        d[(u, v)] = _d
    return d

def bfs_check(test_result, expected, actual):
    if expected != actual:
        e = sorted(" ".join([e[0], e[1], d]) for e, d in expected.items())
        a = sorted(" ".join([e[0], e[1], d]) for e, d in actual.items())
        test_result.add_error(u"saída incorreta", e, a)

def bfs_main(test_result, case, expected, program_result):
    expected = bfs_parse(readlines(expected))
    try:
        actual = bfs_parse(program_result.out.splitlines())
        bfs_check(test_result, expected, actual)
    except ParseError as e:
        test_result.add_error(e.message)


# topological sort
def ts_check(test_result, g, actual):
    if set(g.V) != set(actual):
        test_result.add_error(u"a saída não tem os mesmos vértices do grafo de entrada")
    elif len(set(actual)) != len(actual):
        test_result.add_error(u"a saída contém vértices repetidos")
    else:
        pos = {v : p for p, v in enumerate(actual)}
        for u, v, w in g.E:
            if pos[u] > pos[v]:
                test_result.add_error(u"aresta da direita para esquerda encontrada: %s -> %s" %
                                      (u, v))

def ts_main(test_result, case, expected, program_result):
    g = parse_tgf(readlines(case))
    ts_check(test_result, g, program_result.out.splitlines())


# strongly connected components
def scc_normalize(sccs):
    return sorted(list([tuple(sorted(comp)) for comp in sccs]))

def scc_parse(lines):
    return [line.split() for line in lines]
 
def scc_check(test_result, expected, actual):
    vertices = set()
    for comp in actual:
        for v in comp:
            if v in vertices:
                test_result.add_error(u"vértice repetido: " + v)
            vertices.add(v)
    if not test_result.success(): return

    expected = scc_normalize(expected)
    actual = scc_normalize(actual)
    if expected != actual:
        e = [" ".join(comp) for comp in expected]
        a = [" ".join(comp) for comp in actual]
        test_result.add_error(u"saída incorreta", e, a)

def scc_main(test_result, case, expected, program_result):
    expected = scc_parse(readlines(expected))
    actual = scc_parse(program_result.out.splitlines())
    scc_check(test_result, expected, actual)


# shortest path
def sp_parse(lines):
    paths = {}
    for line in lines:
        values = line.split()
        if len(values) < 2:
            raise ParseError(u"formatação: linha não tem pelo menos 2 valores: " + line)
        path = values[:-1]
        s = path[0]
        u = path[-1]
        cost = int(values[-1])
        if (s, u) in paths:
            raise ParseError(u"formatação: caminho repetido: " + line)
        paths[(s, u)] = (path, cost)
    return paths

def is_path(g, path):
    for i in range(len(path) - 1):
        if not g.is_adj(path[i], path[i+1]):
            return False
    return True

def path_cost(g, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += g.cost(path[i], path[i+1])
    return cost

def sp_check(test_result, g, expected, actual):
    for su in expected:
        if su not in actual:
            test_result.add_error(u"caminho não encontrado: " + " ".join(su))
    for su in actual:
        if su not in expected:
            test_result.add_error(u"não deveria ter o caminho: " + " ".join(actual[su][0]))

    if not test_result.success(): return

    for su in actual:
        path, cost = actual[su]
        if not is_path(g, path):
            test_result.add_error(u"não é um caminho: " + " ".join(path))
        else:
            c = path_cost(g, path)
            if c != cost:
                test_result.add_error(u"custo do caminho '%s' calculado errado" % (" ".join(path)), c, cost)
            elif cost != expected[su][1]:
                test_result.add_error(u"caminho não é mínimo'%s'" % (" ".join(path)), expected[su][1], cost)

def sp_main(test_result, case, expected, program_result):
    g = parse_tgf(readlines(case))
    expected = sp_parse(readlines(expected))
    actual = None
    try:
        actual = sp_parse(program_result.out.splitlines())
    except ParseError as e:
        test_result.add_error(e.message)
        return
    sp_check(test_result, g, expected, actual)


# minimum spanning tree
def mst_parse_result(lines):
    tree = [tuple(line.split()) for line in lines]
    for e in tree:
        if len(e) != 2:
            raise ParseError(u"formatação: linha não tem 2 valores: " + " ".join(e))
    return tree

def find_reachable(g, s):
    Q = deque([s])
    reachable = set([s])
    while Q:
        u = Q.popleft()
        for v in g.adj(u):
            if v not in reachable:
                reachable.add(v)
                Q.append(v)
    return reachable

def mst_check(test_result, g, expected, actual):
    # invalid edges
    for u, v in actual:
        if not g.is_adj(u, v):
            test_result.add_error(u"aresta da árvore não está no grafo: " + u + " " + v)
    if not test_result.success(): return

    # invalid tree
    if len(g.V) - 1 != len(actual):
        test_result.add_error(u"não é uma árvore, número de arestas tem que ser |V| - 1",
                             len(g.V) - 1, len(actual))
    else:
        tree = Graph(g.V, [(u, v, None) for u, v in actual], directed=False)
        reachable = find_reachable(tree, actual[0][0])
        V = set(g.V)
        if V != reachable:
            r = " ".join(V - reachable)
            test_result.add_error(u"não é uma árvore, vértice não acessíveis: " + r)
    if not test_result.success(): return

    # wrong weight
    weight = sum(g.cost(u, v) for u, v in actual)
    if weight != expected:
        test_result.add_error(u"peso", expected, weight)

def mst_main(test_result, case, expected, program_result):
    g = parse_tgf_undirected(readlines(case))
    expected = int(readlines(expected)[0])
    actual = None
    try:
        actual = mst_parse_result(program_result.out.splitlines())
    except ParseError as e:
        test_result.add_error(e.message)
        return
    mst_check(test_result, g, expected, actual)


# utilities
def readlines(infile):
    with open(infile) as f:
        return f.read().splitlines()
