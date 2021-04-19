import numpy as np
import pandas as pd

class Individuo(object):
  
  def __init__(self):
    self.cromossomos = []
    self.fitness = 0.0

  def __str__(self):
    return str(self.cromossomos)
  
  from copy import deepcopy

# Classe que implementa o algoritmo genérico
class AlgoritmoGenetico(object):

  # Método construtor
  def __init__(self, **kwargs):

    # o número de indivíduos da população
    self.populacao_tamanho = kwargs.get('populacao_tamanho', 100)

    # a quantidade de cromossomos de cada indivíduo
    self.numero_cromossomos = kwargs.get('numero_cromossomos', 50)

    # a quantidade de vezes que o ciclo evolutivo será repetido
    self.quantidade_geracoes = kwargs.get('quantidade_geracoes', 500)

    # % da população que será selecionada para a próxima geração
    self.taxa_selecao = kwargs.get('taxa_selecao', .5)

    # probabilidade do indivíduo mais apto ser escolhido durante a seleção
    self.probabilidade_selecao = kwargs.get('probabilidade_selecao', .7)

    # % da população que será gerada através de cruzamento
    self.taxa_cruzamento = kwargs.get('taxa_cruzamento', .5)

    # probabilidade do indivíduo mais apto ter a maior parte dos genes selecionada
    self.probabilidade_cruzamento = kwargs.get('probabilidade_cruzamento', .70)

    # % da população que poderá sofrer mutação 
    self.taxa_mutacao = kwargs.get('taxa_mutacao', .1)

    # probabilidade de um gene qualquer ser mutado
    self.probabilidade_mutacao = kwargs.get('probabilidade_mutacao', .05)

    # a população é uma lista(array) de indivíduos
    self.populacao = [] 

  def criar_populacao_inicial(self):
    pass

  def avaliar(self, individuo):
    pass

  def selecionar(self, individuos):
    pass

  def cruzar(self, individuos):
    pass

  def mutar(self, individuo):
    pass

  def gerar_estatisticas(self):
    fitness = [k.fitness for k in self.populacao]
    melhor = np.min(fitness)
    media = np.median(fitness)
    pior = np.max(fitness)
    return melhor, media, pior


  def executar(self, imprimir=True):

    self.criar_populacao_inicial()

    historico = {'melhor': [], 'media': [], 'pior': []}

    geracoes = 0

    melhor = self.populacao[np.random.randint(self.populacao_tamanho)]

    melhor.fitness = self.avaliar(melhor)

    #Loop principal

    while geracoes < self.quantidade_geracoes:

      geracoes += 1

      ## AVALIAÇÃO
      for individuo in self.populacao:
        individuo.fitness = self.avaliar(individuo)
        if melhor.fitness >= individuo.fitness:
          melhor = deepcopy(individuo)

      self.populacao = sorted(self.populacao, key=lambda k: k.fitness)
      self.populacao = self.populacao[:self.populacao_tamanho]

      fmelhor, fmedio, fpior = self.gerar_estatisticas()
      historico['melhor'].append(fmelhor)
      historico['media'].append(fmedio)
      historico['pior'].append(fpior)

      if imprimir:
        print("Geração:",geracoes," Aptidão:", fmelhor)

      nova_populacao = [deepcopy(melhor)]

      ## SELEÇÃO

      #calcula a quantidade de indivíduos que será selecionada
      quantidade_selecionados = self.populacao_tamanho * self.taxa_selecao

      #repete a seleção para quantidade_selecionados
      for i in np.arange(0,quantidade_selecionados):
        individuos = [self.populacao[ np.random.randint(self.populacao_tamanho)] for k in range(2)]
        nova_populacao.append( self.selecionar(individuos) )

      ## CRUZAMENTO

      #calcula a quantidade de indivíduos que será selecionada
      quantidade_cruzamentos = self.populacao_tamanho * self.taxa_cruzamento

      #repete a seleção para quantidade_selecionados
      for i in np.arange(0,quantidade_cruzamentos):
        individuos = [self.populacao[ np.random.randint(self.populacao_tamanho)] for k in range(2)]
        nova_populacao.append( self.cruzar(individuos) )

      ## MUTAÇÃO

      #calcula a quantidade de indivíduos que será selecionada
      quantidade_mutacoes = self.populacao_tamanho * self.taxa_mutacao

      for i in np.arange(0,quantidade_mutacoes):
        indice = np.random.randint(self.populacao_tamanho)
        individuo = nova_populacao[ indice ]
        individuo = self.mutar(individuo)
        nova_populacao[ indice ] = individuo

      self.populacao = nova_populacao
      
    
    return melhor, historico
