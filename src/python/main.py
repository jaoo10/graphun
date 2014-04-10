import sys
from collections import deque 

# Arquivo texto > listas
# Faz a abertura do arquivo e armazena os valores dos vertices e das arestas, separadamente.
def abreArquivo():
	global vertices
	global arestas
	arquivo = open(sys.argv[2],"r")
	arq = arquivo.readlines()
	arq = [(a.strip()) for a in arq]
	indice = arq.index("#")
	vertices = arq[:indice]
	arestas = arq[indice+1:]
	arestas = [(e.split(' ')) for e in arestas]

# Vertices/Arestas > Lista
# Constroi a hashmap de adjacencia do grafo correspondente.
def buildListaAdj():
	global listaAdj
	listaAdj = {}
	for v in vertices:
		listaAdj[v] = []
	for a in arestas:
		listaAdj[a[0]].append(a[1])

# Arestas > Pesos
# Armazena em uma nova hashmap os pesos de cada aresta.
def buildListaPesos():
	global listaPesos
	listaPesos = {}
	for a in arestas:
		listaPesos[(a[0],a[1])] = int(a[2])
	
# Vertices/Arestas > Vertice inicial(fixo) / Vertice final(variavel) / distancia
# Algoritmo de busca em largura. O grafo de entrada e orientado e as arestas nao tem peso. 
# O vertice de origem s e o primeiro vertice no arquivo de entrada. 
# Para cada vertice v acessivel a partir de s, uma linha deve ser escrita na saida contendo os vertice s e v e a distancia d entre s e v encontrada pelo algoritmo.
def bfs():
	listaCores = {}
	listaDist = {}
	for v in vertices:
		listaCores[v] = 'branco'
		listaDist[v] = 0
	listaCores[vertices[0]] = 'cinza'
	listaDist[vertices[0]] = 0
	fila = deque()
	fila.appendleft(vertices[0])
	while fila:
		primeiro = fila.popleft()
		for v in listaAdj[primeiro]:
			if listaCores[v] == 'branco':
				listaDist[v] = listaDist[primeiro] + 1
				listaCores[v] = 'cinza'
				fila.append(v)
		listaCores[primeiro] = 'preto'
	printBFS(listaDist)

# Lista de distancias > String
# Esta funcao tem como utilidade escrever a saida do BFS.
def printBFS(distancias):
	for v in vertices:
		if vertices[0] == v:
			print vertices[0] + ' ' + v + ' ' + str(distancias[v])
		elif distancias[v] != 0:
			print vertices[0] + ' ' + v + ' ' + str(distancias[v])


# Grafo > Vertice inicial / caminho(lista de vertices) / custo
# Algoritmo de Bellman-Ford para encontrar caminhos mais curtos.
# O grafo de entrada e orientado e as arestas tem peso.
# O vertice de origem s e o primeiro vertice no arquivo de entrada.
# Para cada vertice v acessivel a partir de s, uma linha deve ser escrita na saida contendo um caminho mais curto de s para v e o custo do caminho.
def bf(s):
# initialize_single_source(G,s)
	global predecessores
	global distancias
	distancias = {}
	predecessores = {}
	for v in vertices:
		if v == s:
			distancias[v] = 0
		else:
			distancias[v] = float("inf")
			predecessores[v] = None
# relax(u,v,w)
	for i in range(1,len(vertices)-1):
		for a in arestas:
			if distancias[a[0]] + listaPesos[a[0],a[1]] < distancias[a[1]]:
				distancias[a[1]] = distancias[a[0]] + listaPesos[a[0],a[1]]
				predecessores[a[1]] = a[0]
# checar para ciclos com peso negativo
	for a in arestas:
		if distancias[a[0]] + listaPesos[a[0],a[1]] < distancias[a[1]]:
			print 'Este grafo contem um ciclo de peso negativo'
# exibir a saida
	for v in vertices:
		printBF(s,v)
		if distancias[v] == float("inf"):
			None
		else:
			print(distancias[v])

# Grafo > caminhos
# Algoritmo bf executado com cada vertice do grafo como origem. 
# A entrada e a saida tem o mesmo formato do algoritmo bf.
def bfall():
	for v in vertices:
		bf(v)


# Lista de custos, Lista de predecessores > caminho / custo
# Esta funcao tem como utilidade escrever a saida do BF/BFall.
def printBF(s,v):
	if v == s:
		print s,
	elif predecessores[v] == None:
		None
	else:
		printBF(s,predecessores[v])
		print v,


def fw():
	global matriz
	matriz = {}
	for u in vertices:
		for v in vertices:
			matriz[u,v] = float("inf")
	for v in vertices:
		matriz[v,v] = 0
	for u in vertices:
		for v in vertices:
			if (u != v) and (u,v) in listaPesos.keys():
				matriz[u,v] = listaPesos[u,v]
	buildListaProx()
	for k in range(0,len(vertices)-1):
		for i in range(0,len(vertices)-1):
			for j in range(0,len(vertices)-1):
				if i != j:
					if matriz[vertices[i],vertices[j]] > matriz[vertices[i],vertices[k]] + matriz[vertices[k],vertices[j]]:
						matriz[vertices[i],vertices[j]] = matriz[vertices[i],vertices[k]] + matriz[vertices[k],vertices[j]]
						listaProx[vertices[i],vertices[j]] = listaProx[vertices[k],vertices[j]]
	for u in vertices:
		for v in vertices:
			printFW(u,v)


def buildListaProx():
	global listaProx
	listaProx = {}
	for u in vertices:
		for v in vertices:
			listaProx[u,v] = None
	for i in range(0,len(vertices)-1):
		for j in range(0,len(vertices)-1):
			if i == j or matriz[vertices[i],vertices[j]] == float("inf"):
				listaProx[vertices[i],vertices[j]] = 0
			else:
				listaProx[vertices[i],vertices[j]] = vertices[i]
	

def printFW(u,v):
	if u ==v or matriz[u,v] == float("inf"):
		print " "
	else:
		caminho = listaProx[u,v]
		if caminho == u:
			print " "
		else:
			print str(printFW(u,caminho)) + caminho + str(printFW(caminho,v))


def dfs(vertice,adj):
	global tempo
	global topologic
	topologic = deque()
	tempo = 0
	global listaCores
	listaCores = {}
	for v in vertice:
		listaCores[v] = 'branco'
	for v in vertice:
		if listaCores[v] == 'branco':
			dfs_visit(v,vertice,adj,topologic)
	

def dfs_visit(u,vert,adja,topologica):
	global tempo
	tempo += 1
	listaCores[u] = 'cinza'
	global listaTempo
	listaTempo = {}
	for v in vert:
		listaTempo[v] = 0
	listaTempo[u] = tempo
	for v in adja[u]:
		if listaCores[v] == 'branco':
			dfs_visit(v,vert,adja,topologica)
	listaCores[u] = 'preto'
	topologica.appendleft(u)
	tempo += 1
	listaTempo[u] = tempo
	
def grafo_transposto():
	global gT
	gT = {}
	for v in vertices:
		gT[v] = []
	for u in vertices:
		for v in listaAdj[u]:
			gT[v].append(u)

def scc():
	dfs(vertices,listaAdj)
	top1 = topologic
	grafo_transposto()
	vertices2 = []
	tempos = list(reversed(sorted(listaTempo.values())))
	for t in tempos:
		for v in vertices:
			if t == listaTempo[v]:
				vertices2.append(v)
	dfs(vertices2,gT)
	top2 = topologic
	print top1
	print top2
	

def fw():
	
	
	

def main():
	if sys.argv[1] == 'bfs':
		abreArquivo()
		buildListaAdj()
		bfs()
	elif sys.argv[1] == 'bf':
		abreArquivo()
		buildListaPesos()
		v = vertices[0]
		bf(v)
	elif sys.argv[1] == 'bfall':
		abreArquivo()
		buildListaPesos()
		bfall()
	elif sys.argv[1] == 'fw':
		abreArquivo()
		buildListaPesos()
		fw()
	elif sys.argv[1] == 'dfs':
		abreArquivo()
		buildListaAdj()
		dfs(vertices,listaAdj)
	elif sys.argv[1] == 'scc':
		abreArquivo()
		buildListaAdj()
		scc()

#
if __name__ == "__main__":
	main()



