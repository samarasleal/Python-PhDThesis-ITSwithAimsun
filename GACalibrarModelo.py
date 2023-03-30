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

def initGAEngine(decision_variable, POPSIZE, numberOfVarsToEvolve):
    global pop, fpop, filhos, ffilhos
    # Inicializar população (Váriavel de Decisão: [[reactionT1,reactionT2,reactionT3...], [reactionTS, reactionTS1, reactionTS2...], [], ...])
    sizeParam = len(decision_variable[0])
    pop = zeros((POPSIZE,numberOfVarsToEvolve,sizeParam))
    filhos = zeros((POPSIZE,numberOfVarsToEvolve,sizeParam))
    
    fpop = zeros(POPSIZE)
    ffilhos = zeros(POPSIZE)
    i=0
    while (i < POPSIZE):
        j=0
        while (j < numberOfVarsToEvolve):
            k=0               
            if (j == 1 or j == 2):
                while (k < sizeParam):
                    # Valores aleatórios para reactionTS ou reactionTL
                    pop[i,j,k]= random.uniform(0.7, 3.0)
                    k+=1
            elif (j == 3):
                while (k < sizeParam):
                    # Valores aleatórios para vehMaxDSpeed
                    pop[i,j,k]= random.uniform(50, 180)
                    k+=1
            elif (j == 4):
                while (k < sizeParam):
                    # Valores aleatórios para vehMaxDeceleration
                    pop[i,j,k]= random.uniform(4.0, 7.0)
                    k+=1
            elif (j==0 or j == 5 or j == 6):
                while (k < sizeParam):
                    # Valores aleatórios para reactionT ou vehSpeedAcceptance ou vehMinDist
                    pop[i,j,k]= random.uniform(0.5, 2.0)
                    k+=1
            j+=1
        i+=1
    # Inicialiar parte da população do GA com valores atuais 
    randomIndividual = randrange(0,POPSIZE)  
    pop[randomIndividual] = decision_variable
    return pop, fpop, filhos, ffilhos

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

def crossover1PontodeCorte(pai1, pai2, numberOfVarsToEvolve):
    pontoDeCorte = randrange(1,numberOfVarsToEvolve)
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

def mutacaoGaussiana(s,numberOfVarsToEvolve,MT):
    j = 0
    while j < numberOfVarsToEvolve:
        if (random.uniform(0,1) < MT):
            s[j] = s[j] + random.randn()
        j+=1
    return s
 
def evolveGA(indElite, solucaoElite, qtdeFilhos, pop, fpop, filhos, ffilhos, i, t, timeSim, timeSta, refresh, myFPAG, POPSIZE, CR, MT, numberOfVarsToEvolve, junctionsList, delayParamDefault, decision_variable, idVehList, idInter):  
    # Avaliando os individuos
    bestmen = 0
    if (timeSim < timeSim+POPSIZE-i) and ((timeSim % 1) < 0.1):
        fpop[i] = funcAE.MANEParam(junctionsList, delayParamDefault, timeSta, pop[i,0], pop[i,1], pop[i,2], pop[i,3], pop[i,4], pop[i,5], pop[i,6], idVehList, idInter)
        i+=1
    elif (timeSim == timeSim+POPSIZE-i):
        solucaoElite = min(fpop)
        indElite = where(fpop == solucaoElite)[0][0]
        bestmen = pop[indElite,:]
        i = 51
    else:       
        # Rotinas de Otimização
        if (timeSim < 3600) and ((timeSim % 1) < 0.1):
            # Inicializacoes        
            if (timeSim < timeSim+POPSIZE-t) and ((timeSim % 1) < 0.1):
                # Seleção por torneio
                indPai1 = torneio(POPSIZE, fpop)
                indPai2 = torneio(POPSIZE, fpop)
                # Cruzamento 
                if (random.uniform(0,1) < CR):
                    filhosCR = crossover1PontodeCorte(pop[indPai1,:], pop[indPai2,:], numberOfVarsToEvolve)
                    filhos[qtdeFilhos,:] = filhosCR[0]
                    filhos[qtdeFilhos+1,:] = filhosCR[1]
                    qtdeFilhos = qtdeFilhos + 2 
                if qtdeFilhos == 50:
                    qtdeFilhos = 0
                # Mutação
                filhos[t,:] = mutacaoGaussiana(filhos[t,:],numberOfVarsToEvolve,MT)
                # Avaliação
                ffilhos[t] = funcAE.MANEParam(junctionsList, delayParamDefault, timeSta, filhos[t,0], filhos[t,1], filhos[t,2], filhos[t,3], filhos[t,4], filhos[t,5], filhos[t,6], idVehList, idInter)                               
                t+=1
            else:         
                piorSolucao = max(ffilhos)
                indPior = where(ffilhos == piorSolucao)[0][0]
                
                # Colocar melhor indivíduo da geração de pais no lugar do pior da geração de filhos
                filhos[indPior,:] = pop[indElite,:]
                ffilhos[indPior] = solucaoElite
                      
                # Filhos Substituem Pais
                pop = filhos
                fpop = ffilhos
                
                solucaoElite = min(fpop)
                indElite = where(fpop == solucaoElite)[0][0]
                bestmen = pop[indElite,:]

                # Resultados otimizados atuais 
                myFPAG.write('\n'+str(solucaoElite)) 
                t=0
                qtdeFilhos = 0
    return (bestmen, i, t, pop, fpop, filhos, ffilhos, qtdeFilhos, solucaoElite, indElite)