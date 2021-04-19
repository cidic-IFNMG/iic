import numpy as np
import pandas as pd
import matplotlib as plt


def triangular(x, parametros):
  a, b, c = parametros
  return max(min( ((x-a)/(b-a)), ((c-x)/(c-b)) ), 0)


def gaussiana(x, parametros):
  media, dp = parametros
  return np.exp((-(x - media)**2.0)/(2.0 * dp**2.0))


def singleton(x, parametro):
  return int(x == parametro)


class ConjuntoFuzzy(object):
  def __init__(self, nome, funcao, parametros, ponto_medio):
    self.nome = nome
    self.funcao = funcao
    self.parametros = parametros
    self.ponto_medio = ponto_medio

  def pertinencia(self, x):
    return self.funcao(x, self.parametros)

  def plot(self, ax, intervalo):
    ax.plot(intervalo, [self.pertinencia(k) for k in intervalo])

  def __str__(self):
    return "{}({})".format(self.nome, self.parametros)
  
 
class Composicao(ConjuntoFuzzy):
  def __init__(self, nome, conjuntos):
    super(Composicao, self).__init__(nome, None, None)
    self.conjuntos = conjuntos
    self.ponto_medio = np.max([k.ponto_medio for k in self.conjuntos])
    if nome is None:
      self.nome = str(self)
  
  def pertinencia(self, x):
    pertinencias = [conjunto.pertinencia(x) for conjunto in self.conjuntos]
    return np.max(pertinencias)
    
  def __str__(self):
    ret = ""
    for c in self.conjuntos:
      if len(ret) > 1: ret += " OU "
      ret += c.nome
    return ret

  
class Conjuncao(ConjuntoFuzzy):
  def __init__(self, conjuntos):
    super(Conjuncao, self).__init__(None, None, None)
    self.conjuntos = conjuntos
    self.ponto_medio = np.min([k.ponto_medio for k in self.conjuntos])
    if self.nome is None:
      self.nome = str(self)
        
  def pertinencia(self, x):
    pertinencias = [conjunto.pertinencia(x) for conjunto in self.conjuntos]
    return np.min(pertinencias)
    
  def __str__(self):
    ret = ""
    for c in self.conjuntos:
      if len(ret) > 1: ret += " E "
      ret += c.nome
    return ret


def plot_conjuntos(ax, conjuntos, intervalo):
  ticks = []
  tick_names = []
  for nome, conj in conjuntos.items():
    conj.plot(ax,intervalo)
    ticks.append(conj.ponto_medio)
    tick_names.append(str(round(conj.ponto_medio, 2)) + "\n" + nome)

  ax.set_xticks(ticks)
  ax.set_xticklabels(tick_names)
  
from itertools import product


def inducao(dados, X,Y,conjuntos):
  '''
  dados: Dataframe com todos os dados (X,Y)
  X: lista dos nomes dos atributos descritivos
  Y: o nome do atributo alvo
  conjuntos: dicionário contendo os conjuntos nebulosos de cada variável
  '''

  #ETAPA DE FUZZIFICAÇÃO

  dados_fuzzificados = []
  for indice in dados.index:              # Para cada registro do DataFrame
    linha = dados.loc[indice]             
    linha_fuzzy = {}
    for variavel in conjuntos.keys():     # Para cada variável
      linha_fuzzy[variavel] = []
      for nome, conj in conjuntos[variavel].items():  # Para cada conjunto de cada variável
        if conj.pertinencia(linha[variavel]) > 0:     # Se o valor do atributo pertencer ao conjunto nebuloso
          linha_fuzzy[variavel].append(nome)          # Adiciona à lista de conjuntos nebulosos
    
    dados_fuzzificados.append(linha_fuzzy)
  
  # ETAPA DE CRIAÇÃO DAS REGRAS

  regras = {}

  for linha in dados_fuzzificados:          
    x = [linha[k] for k in X]     # atributos descritivos
    y = linha[Y]                  # atributos alvo
    for precedente in product(*x):  # Combina todos os conjuntos nebulos dos atributos descritivos
      for consequente in y:
        if precedente not in regras:
          regras[precedente] = {consequente: 1}
        else:
          if consequente not in regras[precedente]:
            regras[precedente][consequente] = 1
          else:
            regras[precedente][consequente] += 1

  # NORMALIZAÇÃO DOS PESOS DAS REGRAS

  for precedente in regras.keys():
    total = np.sum([regras[precedente][k] for k in regras[precedente].keys()])
    for k in regras[precedente].keys():
      regras[precedente][k] = regras[precedente][k]/total
    

  return regras


def formata_regras(regras, X, Y):
  for precedente, consequente in regras.items():
    regra = "SE "
    for ct, x in enumerate(X):
      if ct > 0:
        regra += " E "
      regra += "{} = {}".format(x, precedente[ct])
    regra += " ENTÃO {} = ".format(Y)
    for ct, conjunto in enumerate(consequente.keys()):
      if ct > 0:
        regra += " + "
      regra +=  "{}({})".format(conjunto, round(consequente[conjunto],2))
    print(regra)


def inferencia_regressao(dado, X, Y, conjuntos, regras):
  
  # FUZZYFICAÇÃO

  xfuzzy = {}
  for variavel in X:
    xfuzzy[variavel] = {}
    for nome, conj in conjuntos[variavel].items():
      pert = conj.pertinencia(dado[variavel])
      if pert > 0:
        xfuzzy[variavel][nome] = pert
  
  # CASAMENTO DE REGRAS
  
  regras_ativadas = {}

  conj = []
  for variavel in X:
    conj.append([k for k in xfuzzy[variavel].keys()])

  for precedente in product(*conj):
    if precedente in regras:
      
      consequente = 0
      regras_ativadas[precedente] = {}
      for yfuzzy in regras[precedente].keys():
        consequente += conjuntos[Y][yfuzzy].ponto_medio * regras[precedente][yfuzzy]
      regras_ativadas[precedente]['centro'] = consequente
      
      ativacao = []
      for contador, conjunto in enumerate(precedente):
        ativacao.append(xfuzzy[ X[contador] ][ conjunto ])
      regras_ativadas[precedente]['ativacao'] = np.min(ativacao)


  # DEFUZZIFICAÇÃO

  denominador = 0
  numerador = 0

  for regra in regras_ativadas.keys():
    denominador += regras_ativadas[regra]['ativacao']
    numerador += regras_ativadas[regra]['ativacao'] * regras_ativadas[regra]['centro']

  return numerador / denominador


def inferencia_classificacao(dados, X, Y, conjuntos, regras, distribuicao=False):
  
  # FUZZYFICAÇÃO

  xfuzzy = {}
  for variavel in X:
    xfuzzy[variavel] = {}
    for nome, conj in conjuntos[variavel].items():
      pert = conj.pertinencia(dados[variavel])
      if pert > 0:
        xfuzzy[variavel][nome] = pert
  
  # CASAMENTO DE REGRAS
  
  regras_ativadas = {}

  conj = []
  for variavel in X:
    conj.append([k for k in xfuzzy[variavel].keys()])

  for precedente in product(*conj):
    if precedente in regras:
      
      regras_ativadas[precedente] = regras[precedente]
      
      ativacao = []
      for contador, conjunto in enumerate(precedente):
        ativacao.append( xfuzzy[ X[contador] ][ conjunto ] )
      regras_ativadas[precedente]['ativacao'] = np.min(ativacao)


  # DEFUZZIFICAÇÃO

  classificacao = {}
  normalizacao = 0.0

  for precedente, consequente in regras_ativadas.items():
    normalizacao += regras_ativadas[precedente]['ativacao']
    for classe, peso in consequente.items():
      if classe != 'ativacao':
        if classe not in classificacao:
          classificacao[classe] = peso * regras_ativadas[precedente]['ativacao']
        else: 
          classificacao[classe] += peso * regras_ativadas[precedente]['ativacao']

  for classe in classificacao.keys():
    classificacao[classe] = classificacao[classe]/normalizacao

  if distribuicao:
    return classificacao
  else:
    return max(classificacao, key=lambda k: classificacao[k])
