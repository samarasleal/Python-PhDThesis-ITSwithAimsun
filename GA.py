#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:59:44 2017

@author: samara
""" 
from random import randrange
from math import *
from numpy import *
import funcAE

def initGAEngine(decision_variable, POPSIZE, numberOfVarsToEvolve, nGreenTimes, nIntersetcionPhases, funcAtraso):
    global pop, fpop
    pop = zeros((POPSIZE,numberOfVarsToEvolve))
    fpop = zeros(POPSIZE) 
    i=0
    while (i < POPSIZE):
        j = 0
        if funcAtraso == 1:
            while (j < numberOfVarsToEvolve):
                pop[i,j]=random.uniform(15, 90)
                j+=1  
        elif funcAtraso == 2:
            while (j < numberOfVarsToEvolve):
                if j < (numberOfVarsToEvolve-1):
                    #  Valores aleatórios para as fases
                    pop[i,j]=random.uniform(15, 90)
                else:
                    # Valores aleatórios para o ciclo
                    pop[i,j]=random.uniform(90, 140)
                j+=1
        elif funcAtraso == 3:
            while (j < numberOfVarsToEvolve):
                if (j < nGreenTimes):
                    #  Valores aleatórios para as fases
                    pop[i,j]= random.uniform(15, 90)
                elif (j == nGreenTimes):
                    # Valores aleatórios para o ciclo
                    pop[i,j]= random.uniform(90, 140)
                else:
                    # Valores de 0 a 5 que representa um índica da lista de sequência de fases (conj3Phases)
                    pop[i,j]= randrange(0,5)
                j+=1 
        else:
            nPhase=0
            while (j < numberOfVarsToEvolve):
                if (j < nGreenTimes):
                    #  Valores aleatórios para as fases
                    pop[i,j]= random.uniform(15, 90)
                elif (j == nGreenTimes):
                    # Valores aleatórios para o ciclo
                    pop[i,j]= random.uniform(90, 140)
                else:
                    # Caso tenha mais de 1 interseção com 3 fases
                    if nPhase < nIntersetcionPhases:
                        # Valores de 0 a 5 que representa um tipo da lista de sequência de fases (conj3Phases)
                        pop[i,j]= randrange(0,5)
                        nPhase+=1
                    else:
                        # Valores aleatórios para o offset
                        pop[i,j]= random.uniform(0, 20)
                j+=1
        i+=1        
    randomIndividual = randrange(0,POPSIZE)  
    pop[randomIndividual] = decision_variable

def torneio(POPSIZE, fpop):
    k = 0.55
    candidatos = array([fpop[randrange(0,POPSIZE)], fpop[randrange(0,POPSIZE)]]) 
    r = random.uniform(0,1)
    if (r < k):
        solucao = min(candidatos) 
        ind = candidatos.tolist().index(solucao)
    else:
        solucao = max(candidatos)
        ind = candidatos.tolist().index(solucao)
    return ind

def crossoverInterpolacao(pai1, pai2):
    alfa = random.uniform(0,1)
    filho1 =  (alfa * pai1) + ((1 - alfa)* pai2)
    filho2 =  (alfa * pai2) + ((1 - alfa)* pai1)
    return filho1, filho2 

def crossover1PontodeCorte(pai1, pai2, numberOfVarsToEvolve):
    pontoDeCorte = randrange(1,numberOfVarsToEvolve-1)
    filho1 = []
    filho2 = []
    for i in range(numberOfVarsToEvolve):
        if (i < pontoDeCorte):
            filho1.append(pai1[i])
            filho2.append(pai2[i])
        else:
            filho1.append(pai2[i])
            filho2.append(pai1[i])
    filho1 = array(filho1)
    filho1 = array(filho1)
    return filho1, filho2  

def mutacaoGaussiana(s, numberOfVarsToEvolve, MT, nGreenTimes, nIntersetcionPhases, funcAtraso):
    j = 0 
    if funcAtraso == 1:
        while j < numberOfVarsToEvolve:
            sNova = s[j] + abs(random.randn())
            if (random.uniform(0,1) < MT) and (15 <= sNova < 90 ):
                s[j] = sNova
            j+=1
    elif funcAtraso == 2:
        while (j < numberOfVarsToEvolve):
            sNova = s[j] + abs(random.randn())
            if (random.uniform(0,1) < MT):
                if (j < (numberOfVarsToEvolve-1)) and (15 <= sNova < 90 ):
                    s[j] = sNova
                elif (j >= (numberOfVarsToEvolve-1)) and (90 <= sNova <= 140 ):
                    s[j] = sNova
            j+=1            
    elif funcAtraso == 3:
        while j < numberOfVarsToEvolve:
            sNova = s[j] + abs(random.randn())
            if (random.uniform(0,1) < MT):
                if (j < nGreenTimes+1) and (15 <= sNova < 90):
                    s[j] = sNova
                elif (j == nGreenTimes) and (90 <= sNova <= 140):
                    s[j] = sNova
                else:
                    s[j] = randrange(0,5)
            j+=1
    else:
        nPhase = 0
        while (j < numberOfVarsToEvolve):
            sNova = s[j] + abs(random.randn())
            if (random.uniform(0,1) < MT):
                if (j < nGreenTimes) and (15 <= sNova < 90):
                    s[j] = sNova
                elif (j == nGreenTimes) and (90 <= sNova <= 140):
                    s[j] = sNova
                elif (j > nGreenTimes):
                    if (nPhase < nIntersetcionPhases) and (0 <= sNova <= 5):
                        s[j] = randrange(0,5)
                        nPhase+=1
                    elif (nPhase >= nIntersetcionPhases) and (0 <= sNova <= 20):
                        s[j] = sNova
            j+=1        
    return s
              
def evolveGA(timeSim, myFPAG, chromosomeGroupSizes, POPSIZE, CR, MT, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, numberOfVarsToEvolve, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso):
    global pop, fpop
    # Avaliando os individuos 
    i = 0
    while (i < POPSIZE):
        fpop[i] = funcAE.delayFitnessFunc(pop[i,:], chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)                   
        i+=1
    solucaoElite = min(fpop)
    indElite = where(fpop == solucaoElite)[0][0]
    bestmen = pop[indElite,:]
    contConv = 0
    solucaoEliteAnt = solucaoElite
    # Rotinas de Otimização
    # Critério de parada: Convergência da função de avaliação
    while (solucaoElite != solucaoEliteAnt) or (contConv < 250):
    # Inicializacoes
        qtdeFilhos=0
        filhos = zeros((POPSIZE,numberOfVarsToEvolve))
        # Seleção por torneio
        while (qtdeFilhos < POPSIZE):
            indPai1 = torneio(POPSIZE, fpop)
            indPai2 = torneio(POPSIZE, fpop)
            # Cruzamento 
            if (random.uniform(0,1) < CR):
                filhosCR = crossover1PontodeCorte(pop[indPai1,:], pop[indPai2,:], numberOfVarsToEvolve)
                filhos[qtdeFilhos,:] = filhosCR[0]
                filhos[qtdeFilhos+1,:] = filhosCR[1]
                qtdeFilhos = qtdeFilhos + 2
        # Mutação 
        j = 0
        while (j < POPSIZE):
            filhos[j,:] = mutacaoGaussiana(filhos[j,:], numberOfVarsToEvolve, MT, nGreenTimes, nIntersetcionPhases, funcAtraso)
            j+=1  
        # Avaliando os filhos
        t = 0
        ffilhos = zeros(POPSIZE)
        while (t < POPSIZE):
            ffilhos[t] = funcAE.delayFitnessFunc(filhos[t,:], chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)   
            t+=1
        # Elitismo considerando apenas melhor individio da geracao atual: Troca o melhor individuo da geração atual com o pior da geração criada na iteração  
        
        # Pior solução da geração de filhos
        piorSolucao = max(ffilhos)
        indPior = where(ffilhos == piorSolucao)[0][0]
        
        # Colocar melhor indivíduo da geração de pais no lugar do pior da geração de filhos
        filhos[indPior,:] = pop[indElite,:]
        ffilhos[indPior] = solucaoElite
        # Definir a populacao sobrevivente  - Filhos Substituem Pais
        pop = filhos
        fpop = ffilhos
        
        solucaoEliteAnt = solucaoElite
        solucaoElite = min(fpop)
        indElite = where(fpop == solucaoElite)[0][0]
        bestmen = pop[indElite,:]

        # Resultados otimizados atuais 
        myFPAG.write('\n'+str(solucaoElite)) 
        if solucaoElite == solucaoEliteAnt:
            contConv+=1
        else:
            contConv = 0
    return bestmen
