import sys
 

def abreArquivo():
	global vertices
	global arestas
	arquivo = open(sys.argv[1],"r")
	arq = arquivo.readlines()
	arq = [(a.strip()) for a in arq]
	indice = arq.index("#")
	vertices = arq[:indice]
	arestas = arq[indice+1:]
	arestas = [(e.split(' ')) for e in arestas]

def buildListaAdj():
	global listaAdj
	listaAdj = {}
	for v in vertices:
		listaAdj[v] = []
	for a in arestas:
		listaAdj[a[0]].append(a[1])

def buildListaPesos():
	global listaPesos
	listaPesos = {}
	for a in arestas:
		listaPesos[(a[0],a[1])] = a[2]
	
def bfs():
	listaCores = []
	listaDist = []
	for v in vertices:
		listaCores.append('branco')
		listaDist.append(0)
	listaCores[0] = 'cinza'
	listaDist[0] = 0
	fila = []
	fila.append(vertices[0])
	while fila != []:
		primeiro = fila.pop(0)
		for v in listaAdj[primeiro]:
			if listaCores[vertices.index(v)] == 'branco':
				listaDist[vertices.index(v)] = listaDist[vertices.index(primeiro)] + 1
				listaCores[vertices.index(v)] = 'cinza'
				fila.append(v)
		listaCores[vertices.index(primeiro)] = 'preto'
	printBFS(listaDist)

def printBFS(distancias):
	for v in vertices:
		print vertices[0] + ' ' + v + ' ' + str(distancias[vertices.index(v)])


def main():
	print "parametros:"
	for s in sys.argv[1:]:
		print s
	print
	abreArquivo()
	buildListaAdj()
	bfs()


if __name__ == "__main__":
	main()



