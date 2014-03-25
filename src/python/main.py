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


def bf():
# initialize_single_source(G,s)
	global listaDist
	listaDist = {}
	global listaPi
	listaPi = {}
	for v in vertices:
		listaDist[v] = 0
		listaPi[v] = []
	listaDist[vertices[0]] = 0
#----------------------------------------
	i = 1
	if i < len(vertices):
		for b in arestas:
			relax(b[0],b[1],listaPesos[b[0],b[1]])
	for a in arestas:
		if listaDist[a[1]] > listaDist[a[0]] + listaPesos[a[0],a[1]]:
			print 'erro'
	for v in vertices:
		printBF(listaPi,v)


def relax(u,v,w):
	if listaDist[v] > listaDist[u] + w:
		listaDist[v] = listaDist[u] + w
		listaPi[v].append(u)		

def printBF(caminho,vertice):
	for a in listaDist:
		if a == vertice:
			print vertice + vertice + '0'
		else:
			for d in listaDist:
				print " ".join([str(x) for x in caminho] ) + ' ' + d
	


def main():
	if sys.argv[1] == 'bfs':
		abreArquivo()
		buildListaAdj()
		bfs()
	elif sys.argv[1] == 'bf':
		abreArquivo()
		buildListaPesos()
		bf()

#
if __name__ == "__main__":
	main()



