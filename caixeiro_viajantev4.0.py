#encoding: utf-8
import sys, random, math
from pyevolve import *


global plano, coordenadas
plano = []
coordenadas = []

def plano_cartesiano(coordenadas):
   """Matriz com as distâncias de cada coordenada"""
   matriz={}
   for i,(x1,y1) in enumerate(coordenadas):
      for j,(x2,y2) in enumerate(coordenadas):
        #Distância Euclidiana
        ((dx),(dy))=((x1-x2),(y1-y2))
        distancia=math.sqrt(dx*dx + dy*dy)
        """Matriz de genes == chromossomo"""
        matriz[i,j]=distancia
   return matriz


def ler_txt(arquivo):
   """ Lê as coordenadas do arquivo.txt """
   coordenadas=[]
   for linha in arquivo:
      x,y=linha.strip().split(",")
      coordenadas.append((float(x),float(y)))
   return coordenadas

def cria_txt(nome_arquivo, qnt_cidades, lim_X, lim_Y):
   """ Escreve posições de cidades randomicamente em um arquivo.txt"""
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
      j=(i+1)%num_cidades
      cidade_i=percurso[i]
      cidade_j=percurso[j]
      total= total + matriz[cidade_i,cidade_j]
   return total

def Inicia_Cromossomos(cromossomo, **args):

   cromossomo.clearList()
   lista = [i for i in xrange(cromossomo.getListSize())]

   for i in xrange(cromossomo.getListSize()):
      seleciona_gene = random.choice(lista)
      lista.remove(seleciona_gene)
      cromossomo.append(seleciona_gene)

def eval_func(chromossomo):
   """ Função de avaliação """
   global plano
   return comprimento_total_percurso(plano, chromossomo)


if __name__ == "__main__":


  # cria_txt(nomearquivo, qnt_cidades, limite_X, limite_Y)
  cria_txt("cidades.txt", qnt_cidades=30, lim_X=600, lim_Y=400)

  # Abri o arquivo
  arquivo = open("cidades.txt", "rw")
  coordenadas = ler_txt(arquivo)
  plano = plano_cartesiano(coordenadas)

  #Insere o número das cidades como genes
  alelo = GAllele.GAlleles(homogeneous=True)
  lista = [ i for i in xrange(len(coordenadas)) ]
  a = GAllele.GAlleleList(lista)
  alelo.add(a)

  cromossomo = G1DList.G1DList(len(coordenadas))
  cromossomo.setParams(allele=alelo)


  cromossomo.initializator.set(Inicia_Cromossomos)
  cromossomo.evaluator.set(eval_func)
  cromossomo.crossover.set(Crossovers.G1DListCrossoverOX)
  cromossomo.mutator.set(Mutators.G1DListMutatorSwap)


  #Instância cromossomo
  ga = GSimpleGA.GSimpleGA(cromossomo)

  #Tipos de seleção

  #ga.selector.set(Selectors.GRouletteWheel)
  #ga.selector.set(Selectors.GRankSelector)
  #ga.selector.set(Selectors.GRouletteWheel_PrepareWheel)
  #ga.selector.set(Selectors.GTournamentSelector)
  #ga.selector.set(Selectors.GTournamentSelectorAlternative)
  #ga.selector.set(Selectors.GUniformSelector)



  #Desativa Elitismo
  #ga.setElitism(False) ou ga.setElitism(0)
  #Seta o Número de indivíduos para passar para a próxima geração
  #ga.setElitismReplacement(2)

  #Tamanho Geração
  ga.setGenerations(1000)
  #Tamanho População== Quantidade de Indivíduos
  ga.setPopulationSize(60)
  #Taxa cruzamento
  ga.setCrossoverRate(1.0)
  #Taxa de Mutação
  ga.setMutationRate(0.04)  #freq_stats=0 acha o indivíduo "ótimo", demora muito a execução
  ga.evolve(freq_stats=100)


  #Melhor Indivíduo é o que tem o menor percurso total!
  ga.setMinimax(Consts.minimaxType["minimize"])
  melhor_individuo = ga.bestIndividual()
  print melhor_individuo
  print "/n Algorítmo executado com sucesso!"
