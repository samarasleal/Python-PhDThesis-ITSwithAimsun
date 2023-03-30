# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:32:25 2017

@author: samara

"""
from random import randrange
from math import *
from numpy import *
import funcAE

# Inicializa DE	
def initDEEngine(decision_variable, POPSIZE, numberOfVarsToEvolve, nGreenTimes, nIntersetcionPhases):
    global popDE, bestmenit, bestmen, val, popOld, pm1, pm2, pm3
    global bm, ui, mui, mpo, rot, rotd, rt, rtd, a1, a2, a3, a4, a5, ind
    
    # Inicializar população com valores aleatórios entre 0 e 90s
    popDE = zeros((POPSIZE,numberOfVarsToEvolve))
    i=0
    while (i < POPSIZE):
        j=0
        nPhase=0
        while (j < numberOfVarsToEvolve):
            if (j < nGreenTimes):
                #  Valores aleatórios para as fases
                popDE[i,j]= random.uniform(15, 90)
            elif (j == nGreenTimes):
                # Valores aleatórios para o ciclo
                popDE[i,j]= random.uniform(90, 140)
            else:
                # Caso tenha mais de 1 interseção com 3 fases
                if nPhase < nIntersetcionPhases:
                    # Valores de 0 a 5 que representa um tipo da lista de sequência de fases (conj3Phases)
                    popDE[i,j]= randrange(0,5)
                    nPhase+=1
                else:
                    # Valores aleatórios para o offset
                    popDE[i,j]= random.uniform(0, 20)
            j+=1
        i+=1
        
    popOld = zeros((POPSIZE,numberOfVarsToEvolve))
    
    # Inicializar variáveis    
    val       = zeros(POPSIZE)                  # criar e resetar a "matriz de custo"
    bestmen   = zeros(numberOfVarsToEvolve)     # best population member ever 
    bestmenit = zeros(numberOfVarsToEvolve)     # melhor indivíduo na população da iteracao
    
    pm1 = zeros((POPSIZE,numberOfVarsToEvolve))              # inicialize a populacao da matriz 1
    pm2 = zeros((POPSIZE,numberOfVarsToEvolve))              # inicialize a populacao da matriz 2
    pm3 = zeros((POPSIZE,numberOfVarsToEvolve))              # inicialize a populacao da matriz 3
    bm  = zeros((POPSIZE,numberOfVarsToEvolve))              # inicialize o melhor individuo da matriz
    ui  = zeros((POPSIZE,numberOfVarsToEvolve))              # populacao intermediaria dos vetores pertubados
    mui = zeros((POPSIZE,numberOfVarsToEvolve))              # mascara para a populacao intermediaria
    mpo = zeros((POPSIZE,numberOfVarsToEvolve))              # mascara para a populacao antiga
    rot = arange(POPSIZE)                                        # rotacionando o indice da matriz (tamanho POPSIZE)
    rotd= arange(numberOfVarsToEvolve)                           # rotacionando o indice da matriz (tamanho numberOfVarsToEvolve)
    rt  = zeros((POPSIZE,POPSIZE))                               # rotacionando o indice de uma outra matriz
    rtd = zeros((numberOfVarsToEvolve,numberOfVarsToEvolve))     # rotacionando o indice da matriz para cruzamento exponencial
    a1  = zeros((POPSIZE,POPSIZE))                  # indice da matriz 
    a2  = zeros((POPSIZE,POPSIZE))                  # indice da matriz
    a3  = zeros((POPSIZE,POPSIZE))                  # indice da matriz
    ind = zeros((4,4));      

    # Inicialiar parte da população do DE com valores atuais 
    randomIndividual = randrange(0,POPSIZE)  
    popDE[randomIndividual] = decision_variable

def evolveDE(timeSim, myFPDE, chromosomeGroupSizes, POPSIZE, strategy, Fstep, CR, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, numberOfVarsToEvolve, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso):
    global popDE, bestmenit, bestmen, val, popOld, pm1, pm2, pm3
    global bm, ui, mui, mpo, rot, rotd, rt, rtd, a1, a2, a3, a4, a5, ind
    # Avaliando o melhor indivíduo após a inicialização
    ibest = 0                     # inicializacao com o primeiro individuo da populacao
    val[0]  = funcAE.delayFitnessFunc(popDE[ibest,:], chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)
    bestval = val[0]              # melhor valor da funcao objetivo ate agora    
    # Verificando os individuos restantes
    i = 1
    while (i < POPSIZE):
        val[i] = funcAE.delayFitnessFunc(popDE[i,:], chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)              
        if (val[i] < bestval):             # se o individuo eh o melhor
            ibest   = i                    # salvar a sua localizacao
            bestval = val[i] 
        i+=1
    bestmenit = popDE[ibest,:]      # melhor individuo da iteracao atual 
    bestmen = bestmenit             # melhor individuo sempre 
    # Rotinas de Otimização    
    # Critério de parada: Convergência da função de avaliação
    contConv = 0
    bestvalAnt = bestval
    while (bestval != bestvalAnt) or (contConv < 120):
        popOld = popDE;                                    # guardando o populacao antiga                    
        ind = random.permutation([1,2,3,4])                # indice do ponteiro da matriz                   
        a1  = random.permutation(POPSIZE)                  # locais aleatorios do vetor        
        rt = (rot+ind[0]) % POPSIZE                        # rotacionando as posicoes dos indices de ind(1) 
        rt = rt.astype(int)
        a2 = a1[rt]                                        # rotacionando o vetor de localizacoes
        rt = (rot+ind[1]) % POPSIZE
        rt = rt.astype(int)
        a3  = a2[rt]                         
        pm1 = popOld[a1,:]             # embaralhando a populacao 1        
        pm2 = popOld[a2,:]             # embaralhando a populacao 2
        pm3 = popOld[a3,:]             # embaralhando a populacao 3
        
        # populacao preenchida com o melhor individuo da ultima iteracao
        i=0
        while (i < POPSIZE):        
            bm[i,:] = bestmenit      
            i+=1
        mui = random.rand(POPSIZE,numberOfVarsToEvolve) < CR    
        mui = mui.astype(int)
        # Cruzamento        
        if (strategy > 5):
            st = strategy-5;		                   # cruzamento binomial 
        else:
            st = strategy;		                        # cruzamento exponential            
            mui=sort(mui.conj().transpose())	          # escolhendo o primeiro de cada coluna da transposta
            i=0
            while (i < POPSIZE):
                n=floor(random.rand()*numberOfVarsToEvolve)
                if (n > 0):
                    rtd = (rotd+n) % numberOfVarsToEvolve
                    rtd = rtd.astype(int)  
                    mui[:,i] = mui[rtd,i]            # rotacionando a coluna i por n
                i+=1
            mui = mui.conj().transpose()	            # transpor novamente
        mpo = mui < 0.5                              # mascara inversa de mui    
        
        ui = popOld
        # DE/best/1
        #if (st > 1): 
        uiParte = bm + Fstep*(pm1 - pm2)
        uiTemp = popOld*mpo + uiParte*mui
        m = 0
        while m < POPSIZE:
            j = 0 
            nPhase = 0
            while (j < numberOfVarsToEvolve):
                if (j < nGreenTimes) and (15 <= uiTemp[m,j] < 90):
                    ui[m,j] = uiTemp[m,j]
                elif (j == nGreenTimes) and (90 <= uiTemp[m,j] <= 140):
                    ui[m,j] = uiTemp[m,j]
                elif (j > nGreenTimes):
                    if (nPhase < nIntersetcionPhases) and (0 <= uiTemp[m,j] <= 5):
                        ui[m,j] = randrange(0,5)
                        nPhase+=1
                    elif (nPhase >= nIntersetcionPhases) and (0 <= uiTemp[m,j] <= 20):
                        ui[m,j] = uiTemp[m,j]
                j+=1 
            m+=1
        # DE/rand/1
#        else:                 
#            ui = pm3 + Fstep*(pm1 - pm2)       
#            ui = popOld*mpo + ui*mui 
        bestvalAnt = bestval
        # Selecionando quais vetores são autorizados a entrar na nova população
        l=0 
        while (l < POPSIZE):
            tempval = funcAE.delayFitnessFunc(ui[l,:], chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)  
            if (tempval <= val[l]):          # se concorrente é melhor do que o valor da "matriz de custo"
                popDE[l,:] = ui[l,:]         # substitua o vetor antigo por um novo (para a nova iteracao)
                val[l]   = tempval           # salve o valor na "matriz de custo"
                # Atualizando bestval apenas no caso de sucesso para economizar tempo
                if (tempval < bestval):      # se o concorrente for melhor que o melhor individuo sempre
                    bestval = tempval        # bestval recebe um novo valor
                    bestmen = ui[l,:]        # novo valor de parametro de melhor vetor sempre
            l+=1
        # guardar o melhor individuo desta iteracao para a proxima iteracao. 
        bestmenit = bestmen     
        # Resultados otimizados atuais                        
        myFPDE.write('\n'+str(bestval))
        if bestval == bestvalAnt:
            contConv+=1
        else:
            contConv = 0
    return bestmen, bestval                