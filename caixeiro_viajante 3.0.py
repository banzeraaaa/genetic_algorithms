import sys, random
from math import sqrt
from pyevolve import *


global plano, coordenadas
PILHA_AUX = None

try:
   from PIL import Image, ImageDraw, ImageFont
   PILHA_AUX = True
except:
   PILHA_AUX = False

def plano_cartesiano(coordenadas):
   """Matriz com as distancias de cada coordenada"""
   matriz={}
   for i,(x1,y1) in enumerate(coordenadas):
      for j,(x2,y2) in enumerate(coordenadas):
        """vetor resultante"""
        ((dx),(dy))=((x1-x2),(y1-y2))
        dist=sqrt(dx*dx + dy*dy)
        """Comentar tbm"""
        matriz[i,j]=dist
   return matriz


def ler_txt(arquivo):
   """ Le as coordenadas do arquivo.txt """
   coordenadas=[]
   for linha in arquivo:
      x,y=linha.strip().split(",")
      coordenadas.append((float(x),float(y)))
   return coordenadas

def cria_txt(nome_arquivo, qnt_cidades, lim_X=800, lim_Y=600):
   """ Escreve posicoes de cidades randomicamente em um arquivo.txt"""
   arquivo = open(nome_arquivo, "w")
   for i in xrange(qnt_cidades):
      x = random.randint(0, lim_X)
      y = random.randint(0, lim_Y)
      arquivo.write("%d,%d\n" % (x,y))
   arquivo.close()

def comprimento_total_percurso(matriz, percurso):
   """ Retorna o comprimento do percurso total """
   total=0
   num_cidades=len(percurso)
   for i in range(num_cidades):
      """Tenho q comentar isso"""
      j=(i+1)%num_cidades
      cidade_i=percurso[i]
      cidade_j=percurso[j]
      total= total + matriz[cidade_i,cidade_j]
   return total

def Inicia_Cromossomos(cromossomo, **args):

   cromossomo.clearList()
   lista = [i for i in xrange(cromossomo.getListSize())]

   for i in xrange(cromossomo.getListSize()):
      choice = random.choice(lista)
      lista.remove(choice)
      cromossomo.append(choice)


plano = []
coordenadas = []

def eval_func(chromossomo):
   """ Funcao de avaliacao """
   global plano
   return comprimento_total_percurso(plano, chromossomo)


def plot_graph(coordenadas, percurso, img_file):
   """ The function to plot the graph """
   padding=20
   coordenadas=[(x+padding,y+padding) for (x,y) in coordenadas]
   maxx,maxy=0,0
   for x,y in coordenadas:
      maxx=max(x,maxx)
      maxy=max(y,maxy)
   maxx+=padding
   maxy+=padding
   img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))
   font=ImageFont.load_default()
   d=ImageDraw.Draw(img);
   num_cidades=len(percurso)
   for i in range(num_cidades):
      j=(i+1)%num_cidades
      cidade_i=percurso[i]
      cidade_j=percurso[j]
      x1,y1=coordenadas[cidade_i]
      x2,y2=coordenadas[cidade_j]
      d.linha((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
      d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))

      for x,y in coordenadas:
       """Desenha circulo nos pontos"""
      x,y=int(x),int(y)
      d.ellipse((x-5,y-5,x+5,y+5),outlinha=(0,0,0),fill=(196,196,196))
   del d
   img.save(img_file, "PNG")
   print "A plotagem foi salva no arquivo!." % (img_file,)



if __name__ == "__main__":


  # cria_txt(nomearquivo, qnt_cidades, limite_X, limite_Y)
  cria_txt("pos_cidades.txt", 30, 600, 400)

  # Abri o arquivo
  arquivo = open("pos_cidades.txt", "rw")
  coordenadas = ler_txt(arquivo)
  plano = plano_cartesiano(coordenadas)

  #Insere o numero das cidades como genes
  genes = GAllele.GAlleles(homogeneous=True)
  lista = [ i for i in xrange(len(coordenadas)) ]
  a = GAllele.GAlleleList(lista)
  genes.add(a)

  cromossomo = G1DList.G1DList(len(coordenadas))
  cromossomo.setParams(allele=genes)

  cromossomo.initializator.set(Inicia_Cromossomos)
  cromossomo.crossover.set(Crossovers.G1DListCrossoverOX)
  cromossomo.mutator.set(Mutators.G1DListMutatorSwap)
  cromossomo.evaluator.set(eval_func)


  ga = GSimpleGA.GSimpleGA(cromossomo)
  ga.setGenerations(1000)
  ga.setPopulationSize(60)
  ga.setCrossoverRate(1.0)
  ga.setMutationRate(0.04)
  ga.evolve(freq_stats=100)
  ga.setMinimax(Consts.minimaxType["minimize"])
  melhor_individuo = ga.bestIndividual()
  print melhor_individuo

  sqlite_adapter =
  DBAdapters.DBSQLite(identify="Problema Caixeiro Viajante",
  commit_freq=1000, frequency=500)
  ga.setDBAdapter(sqlite_adapter)

  if PILHA_AUX:
     plot_graph(coordenadas, melhor_individuo, "resultado.png")
  else:
     print "Pilha nao detectada,nao foi possivel plotar o grafico!"
