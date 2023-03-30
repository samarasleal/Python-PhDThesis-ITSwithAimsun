# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:32:25 2017

@author: samara

"""

from __future__ import division 
from AAPI import *

from random import randrange
from math import *
from numpy import *
import dictionaries
import funcAimsun
import funcAE
import DE
import copy
import time
import funcCampo
import GA

##############################          Algoritmos Evolutivos          ##############################
evolut = 1                    # 1:AG; 2:DE
strategy = 1                  # 2:DE/best/1/exp; 1:DE/rand/1/exp 
POPSIZE = 50                  # Tamanho da população AG
INIT = True    
Fstep = 0                   # DE-stepsize
CR = 0.8                    # Probabilidade de Cruzamento
MT = 0.04                   # Probabilidade de Mutação
numberOfVarsToEvolve = -1

##############################          Aimsun          ##############################
controlType = 2             # 0:uncontrolled; 1:fixed; 2:external; 3:actuated 
netType = 2                 # 1:isolada, 2:Floresta e 3: Savassi
ACTIVE_CONTROL_ON = False    # True: Controle ativo ligado; False: Controle ativo desligado
dadosTV = False
MINSPLIT, MAXSPLIT = 15 , 99  
ctypeStr = ["uncontrolled","fixed","external","actuated"]
usedAggregInterval = 10
usedInstantInterval = 1
numOfJunctions = 0
theCycleTime = 90.0 
offset = 15.0
if netType == 2:
    listOffset = [15.0, 15.0,15.0]
else:
    listOffset = [15.0,15.0]
listIdPhases = [0]
TotalDelay = 0.0 
definirAtraso = False
otimizarModelo = True
funcAtraso = 4
nomeFuncao = "akcelik"
tempo = 90.0

##############################          Dicionário          ##############################
# Criar dicionários de dados: detectores, movimentos, fases, etc...
dictionaries.createDictionaries(netType, theCycleTime)
junctionsList = dictionaries.junctionsList
detectorInfo = dictionaries.detectorInfo
phaseFields = dictionaries.phaseFields
phaseParam = dictionaries.phaseParam
movementInfo = dictionaries.movementInfo 
nIntersections = dictionaries.nIntersections

##############################          Arquivo para informações sobre os detectores          ##############################
# Mac
dataFileName1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/DE.dat'
dataFileName2 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/AG.dat'
dataFileName4 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/dTotalCicloONBH.dat'
myFPDE = open(dataFileName1, 'w')
myFPAG = open(dataFileName2, 'w')

if dadosTV==True:
    ciclos = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ciclos.dat'
    myFPciclo = open(ciclos, 'w')
    if netType == 2: 
        # Interseção 01
        ID1Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase0.dat'
        ID1Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase1.dat'
        ID1Fase2 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase2.dat'
        myFPID1Fase0 = open(ID1Fase0, 'w')
        myFPID1Fase1 = open(ID1Fase1, 'w')
        myFPID1Fase2 = open(ID1Fase2, 'w')
        # Interseção 02
        ID2Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Fase0.dat'
        ID2Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Fase1.dat'
        ID2Def = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Def.dat'
        myFPID2Fase0 = open(ID2Fase0, 'w')
        myFPID2Fase1 = open(ID2Fase1, 'w')
        myFPID2Def = open(ID2Def, 'w')
        # Interseção 03
        ID3Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Fase0.dat'
        ID3Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Fase1.dat'
        ID3Def = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Def.dat'
        myFPID3Fase0 = open(ID3Fase0, 'w')
        myFPID3Fase1 = open(ID3Fase1, 'w')
        myFPID3Def = open(ID3Def, 'w')
        # Interseção 04
        ID4Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID4Fase0.dat'
        ID4Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID4Fase1.dat'
        ID4Def = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID4Def.dat'
        myFPID4Fase0 = open(ID4Fase0, 'w')
        myFPID4Fase1 = open(ID4Fase1, 'w')
        myFPID4Def = open(ID4Def, 'w')
    else:
        # Interseção 01
        ID1Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase0.dat'
        ID1Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase1.dat'
        ID1Fase2 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID1Fase2.dat'
        myFPID1Fase0 = open(ID1Fase0, 'w')
        myFPID1Fase1 = open(ID1Fase1, 'w')
        myFPID1Fase2 = open(ID1Fase2, 'w')
        # Interseção 02
        ID2Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Fase0.dat'
        ID2Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Fase1.dat'
        ID2Def = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID2Def.dat'
        myFPID2Fase0 = open(ID2Fase0, 'w')
        myFPID2Fase1 = open(ID2Fase1, 'w')
        myFPID2Def = open(ID2Def, 'w')
        # Interseção 03
        ID3Fase0 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Fase0.dat'
        ID3Fase1 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Fase1.dat'
        ID3Def = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/ID3Def.dat'
        myFPID3Fase0 = open(ID3Fase0, 'w')
        myFPID3Fase1 = open(ID3Fase1, 'w') 
        myFPID3Def = open(ID3Def, 'w')

	

##############################          Funções do Aimsun          ##############################
def AAPILoad():
	return 0

# Inicar a simulação e os modulos	
def AAPIInit():
    global junctionsList, detectorInfo, phaseFields, phaseParam, movementInfo, nIntersections, delayParamDefault
    global numberOfVarsToEvolve, chromosomeGroupSizes, usedAggregInterval, usedInstantInterval, theCycleTime, INIT, t 
    if nIntersections <= 0:
        AKIPrintString( "=> Erro: Intersecao nao encontrada. Finalizando..." )
        ANGSetSimulationOrder(3,0) 
    else:
        AKIPrintString("Numero de intersecoes = " + '%4d'%(nIntersections))
        initialSplitsByPhase, numberOfVarsToEvolve, chromosomeGroupSizes, theCycleTime = funcAimsun.getInfoFromAimsunNetwork(junctionsList, phaseParam, INIT, 0.0, phaseFields)
        for idxJunct,thisJunct in enumerate(junctionsList):
            nPhasesThisJunct = len(initialSplitsByPhase[idxJunct])
            thisJunctionSignals = ECIGetNumberSignalGroups(thisJunct)
            if thisJunctionSignals < 0:
                AKIPrintString( "=> Erro: Grupo semafórico não encontrado. Finalizando..." )                
                ANGSetSimulationOrder(3,0) 
            else:
                AKIPrintString( "=> " + '%d'%(thisJunctionSignals)+" grupos semaforicos na intersecao "+'%d'%(thisJunct))
                controlType = ECIGetControlType(thisJunct)
                AKIPrintString( "=> Tipo de Controle = " + ctypeStr[controlType]+", "+"%d"%(nPhasesThisJunct)+" fases")	
                myTimingsStr = '| '
                for thisPhase in range(nPhasesThisJunct):
                    myTimingsStr += " Fase "+'%2d'%(thisPhase+1)+": "+'%5d'%(initialSplitsByPhase[idxJunct][thisPhase])+"s |"
                print(" ")                
                AKIPrintString("+---------------------------------------------------------------------+")
                AKIPrintString(myTimingsStr)
                AKIPrintString("+---------------------------------------------------------------------+")
        AKIPrintString("Tempo de ciclo inicial igual para todas as intersecoes = %f" %(theCycleTime))        
    # Obter informações sobre detectores da rede
    usedAggregInterval = AKIDetGetIntervalDetection()
    usedInstantInterval = AKIDetGetCycleInstantDetection()    
    # Inicializar dados do detector, organizados por junções
    for indInter in range(len(detectorInfo)):
        for indDetector in range(len(detectorInfo[indInter])):
            detectorInfo[indInter][indDetector]['count'] = 0
            detectorInfo[indInter][indDetector]['speed'] = 0.0
            detectorInfo[indInter][indDetector]['denst'] = 0.0    
    # Atraso total inicial da rede obtido em campo - Método das placas
    delayParamDefault = funcCampo.getDelayFromField()              
    AKIPrintString( "My AAPIInit finalizada!" )
    return 0

# Chamada no inicío de cada passo de simulação
def AAPIManage(timeSim, timeSta, timeTrans, acycle):
    global junctionsList, idmeteringList, detectorInfo, phaseParam, movementInfo, nIntersections, phaseFields, usedInstantInterval
    global usedAggregInterval, theCycleTime, ACTIVE_CONTROL_ON, chromosomeGroupSizes, delayParamDefault
    global POPSIZE, numberOfVarsToEvolve, numberOfParamsToEvolve, decision_variableParam
    global TotalDelay, TotalStop, reactionT, reactionTS, reactionTL, vehMaxDSpeed, vehMaxAcceleration, vehSpeedAcceptance, vehMinDist, idVeh, listIdInter, listIdPhases, listOffset
    global myFPD, myFPDE, myFPAG, myNSGAatraso, myNSGAparada, simulationName, myFPAGPara, nomeFuncao
    global Fstep, CR, strategy, F, R, tempo
    global bestmen
    regime = [] 
    decision_variable = []
    numberOfVarsToEvolve = 6    
    # Salvar informações dos detectores 
    if (timeSim % 10) < 0.1:
        for indInter in range(len(detectorInfo)):
            for indDetector in range(len(detectorInfo[indInter])):
                detectorInfo[indInter][indDetector]['count'] += AKIDetGetCounterAggregatedbyId(detectorInfo[indInter][indDetector]['id'],0)
                detectorInfo[indInter][indDetector]['speed'] += AKIDetGetSpeedAggregatedbyId(detectorInfo[indInter][indDetector]['id'],0)
                detectorInfo[indInter][indDetector]['denst'] += AKIDetGetDensityAggregatedbyId(detectorInfo[indInter][indDetector]['id'],0)			              

    ##########           Definir função de atraso      ############
#    if (definirAtraso == True):
#        if (timeSim == 900):
#            decision_variable = funcAE.setPercentMovablePartitionFromSplits(nIntersections, phaseParam)
#            AKIPrintString( "Definição função de atraso - My AAPIManage: tempo = %s" %(timeSim))
#            retorno=funcAE.MANEFunction(decision_variable, nIntersections, theCycleTime, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, junctionsList, delayParamDefault, timeSim, nomeFuncao, chromosomeGroupSizes)   
#            print("MANE para função %s" %(nomeFuncao))
#            print(retorno)
    #########           AG - Funções de atraso para Otimização - Variáveis de Decisão       ############
    if (otimizarModelo == True):
        #if (( timeSim == 1800 ) or ( timeSim == 1890 )) and ( ( timeSim % theCycleTime ) < 0.1 ):
        if round(timeSim)== tempo:
            AKIPrintString( "AAPIManage: tempo = %s" %(timeSim))
            # Tempo de Verde na variável de decisão
            decision_variable = funcAE.setPercentMovablePartitionFromSplits(nIntersections, phaseParam)
            nGreenTimes = len(decision_variable)  
            nIntersetcionPhases = 0
            if ACTIVE_CONTROL_ON:                
                if (funcAtraso == 1):
                    numberOfVarsToEvolve = nGreenTimes
                    AKIPrintString("AG - Variável de decisão: tempo de verde")                    
                elif (funcAtraso == 2):
                    # Adicionar tempo de ciclo na variável de decisão
                    decision_variable.append(theCycleTime)                     
                    AKIPrintString("AG - Variável de decisão: tempo de verde e tempo de ciclo")
                elif(funcAtraso == 3):
                    decision_variable.append(theCycleTime) 
                    # Adicionar sequencia de fases na variável para interseções com mais de 3 fases
                    for thisInter in range(nIntersections):
                        nPhasesThisInter = ECIGetNumberPhases(junctionsList[thisInter]) 
                        if (nPhasesThisInter == 3):
                            numberOfVarsToEvolve+=1
                            conj3PhasesInd = randrange(0,5)
                            decision_variable.append(conj3PhasesInd) 
                            nIntersetcionPhases+=1                     
                    AKIPrintString("AG - Variável de decisão: tempo de verde, tempo de ciclo e sequência de fases")
                else:
                    decision_variable.append(theCycleTime) 
                    for thisInter in range(nIntersections):
                        nPhasesThisInter = ECIGetNumberPhases(junctionsList[thisInter]) 
                        if (nPhasesThisInter == 3):
                            numberOfVarsToEvolve+=1
                            conj3PhasesInd = randrange(0,5)
                            decision_variable.append(conj3PhasesInd) 
                            nIntersetcionPhases+=1
                    # Adicionar offset na variável de decisão (para cada interseção)
                    for thisInter in range(nIntersections-1):
                        numberOfVarsToEvolve+=1
                        decision_variable.append(offset)
                    AKIPrintString("Variável de decisão: tempo de verde, tempo de ciclo, sequência de fases e defasagem")                              
                
                # Varíaveis de decisão
                numberOfVarsToEvolve = len(decision_variable)
                AKIPrintString("Numero de variáveis de decisao " + '%4d'%(numberOfVarsToEvolve))
                print(decision_variable)
                if evolut == 1: 
                    GA.initGAEngine(decision_variable, POPSIZE, numberOfVarsToEvolve, nGreenTimes, nIntersetcionPhases, funcAtraso)                
                    print("Inicialização ok")
                    bestmen = GA.evolveGA(timeSim, myFPAG, chromosomeGroupSizes, POPSIZE, CR, MT, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, numberOfVarsToEvolve, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)  
                    print("Rotinas de otimização ok")
                
                if (funcAtraso == 1):
                    bestSplits = funcAE.getSplitsFromPercentMovablePartition(bestmen, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
                    print("Melhores tempos de verde - fases")
                    print(bestSplits)                                      
                if (funcAtraso == 2):
                    bestmen = bestmen.tolist()
                    theCycleTime = bestmen.pop(-1)
                    bestSplits = funcAE.getSplitsFromPercentMovablePartition(bestmen, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
                    print("Melhores tempos de verde")
                    print(bestSplits)
                    print("Melhor Ciclo:")
                    print(round(theCycleTime))
                               
                if (funcAtraso == 3):
                    bestmen = bestmen.tolist()                    
                    theCycleTime = bestmen.pop(-2)
                    listIdPhases = []
                    listIdPhases.append(int(bestmen.pop(-1))) 
                    bestSplits = funcAE.getSplitsFromPercentMovablePartition(bestmen, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
                    print("Melhores tempos de verde")
                    print(bestSplits)
                    print("Melhor Ciclo:")
                    print(round(theCycleTime))
                    print("Melhor Sequência de Fases")
                    conj3Phases = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
                    for id in listIdPhases:
                        print(conj3Phases[id])  
                    
                if (funcAtraso == 4):              
                    if evolut == 2:
                        print("DE")
                        DE.initDEEngine(decision_variable, POPSIZE, numberOfVarsToEvolve, nGreenTimes, nIntersetcionPhases)
                        print("Inicialização ok")
                        bestmen, cycleDelay = DE.evolveDE(timeSim, myFPDE, chromosomeGroupSizes, POPSIZE, strategy, Fstep, CR, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, numberOfVarsToEvolve, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso)
                        print("Rotinas de otimização ok")
                    bestmen = bestmen.tolist()
                    nPhase = 0
                    t = 0
                    ListGreenTimes = []
                    listIdPhases = []
                    listOffset = []
                    while t < numberOfVarsToEvolve:
                        if (t < nGreenTimes):
                            ListGreenTimes.append(bestmen[t])
                        elif (t == nGreenTimes):
                            theCycleTime = bestmen[t]
                        else:
                            if nPhase < nIntersetcionPhases:
                                listIdPhases.append(int(bestmen[t]))
                                nPhase+=1
                            else:                                
                                listOffset.append(bestmen[t])
                        t+=1
                    bestSplits = funcAE.getSplitsFromPercentMovablePartition(ListGreenTimes, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
                    print("Melhores tempos de verde - fases")
                    print(bestSplits)
                    if dadosTV==True:
                        if netType ==2:
                            # ID1
                            myFPID1Fase0.write('\n'+str(bestSplits[2][0]))
                            myFPID1Fase1.write('\n'+str(bestSplits[2][1]))
                            myFPID1Fase2.write('\n'+str(bestSplits[2][2]))
                            # ID2
                            myFPID2Fase0.write('\n'+str(bestSplits[0][0])) 
                            myFPID2Fase1.write('\n'+str(bestSplits[0][1]))
                            myFPID2Def.write('\n'+str(round(listOffset[0])))
                            # ID3
                            myFPID3Fase0.write('\n'+str(bestSplits[1][0])) 
                            myFPID3Fase1.write('\n'+str(bestSplits[1][1])) 
                            myFPID3Def.write('\n'+str(round(listOffset[1])))
                            # ID4
                            myFPID4Fase0.write('\n'+str(bestSplits[3][0])) 
                            myFPID4Fase1.write('\n'+str(bestSplits[3][1])) 
                            myFPID4Def.write('\n'+str(round(listOffset[2])))
                        else:
                            # ID1
                            myFPID1Fase0.write('\n'+str(bestSplits[0][0]))
                            myFPID1Fase1.write('\n'+str(bestSplits[0][1]))
                            myFPID1Fase2.write('\n'+str(bestSplits[0][2]))
                            # ID2
                            myFPID2Fase0.write('\n'+str(bestSplits[1][0])) 
                            myFPID2Fase1.write('\n'+str(bestSplits[1][1]))
                            myFPID2Def.write('\n'+str(round(listOffset[0])))
                            # ID3
                            myFPID3Fase0.write('\n'+str(bestSplits[2][0])) 
                            myFPID3Fase1.write('\n'+str(bestSplits[2][1])) 
                            myFPID3Def.write('\n'+str(round(listOffset[1])))
                        #Ciclo
                        myFPciclo.write('\n'+str(timeSim))
                    print("Melhor tempo de Ciclo:")
                    print(round(theCycleTime))
                    
                    print("Melhor Sequência de Fases")
                    conj3Phases = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
                    for id in listIdPhases:
                        print(conj3Phases[id])  
                    print("Melhor offset")
                    print(listOffset) 
            else:
                bestSplits = funcAE.getSplitsFromPercentMovablePartition(decision_variable, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
            funcAimsun.setInfoToAimsunNetwork(bestSplits, junctionsList, phaseParam, timeSta)
            
            # Estimar novo atraso do ciclo
            effectiveSplits = funcAE.getEffectiveSplitsByMovement(bestSplits, movementInfo)
            cycleDelay2 = funcAE.estimatedCycleDelayByPhaseSequenceOffsetAkcelik(effectiveSplits, theCycleTime, listIdPhases, regime, movementInfo, detectorInfo, junctionsList, listOffset)
            print('AAPIManage - Cycle Delay %f s'%(cycleDelay2))
            if cycleDelay2 > 0:
                TotalDelay += cycleDelay2
            tempo = tempo + theCycleTime
            tempo = round(tempo)
    #Resetar variáveis dos detectores
#    for indInter in range(len(detectorInfo)):
#        for indDetector in range(len(detectorInfo[indInter])):
#            detectorInfo[indInter][indDetector]['count'] = 0
#            detectorInfo[indInter][indDetector]['speed'] = 0.0
#            detectorInfo[indInter][indDetector]['denst'] = 0.0
        
    return timeSim
	
# Chamado no final de cada passo de simulação para obter informações
def AAPIPostManage(timeSim, timeSta, timeTrans, acycle):
    return 0

# Finalizar a simulação	
def AAPIFinish():
    global TotalDelay, TotalStop
    global myFPT, myFPDE, myFPAG, myNSGAparada, simulationName

    print("AAPIFinish Estim. Total Delay %f" %(TotalDelay))

    myFPT = open(dataFileName4, 'r')
    texto = myFPT.readlines()
    texto.append('\n'+str(TotalDelay))
    myFPT = open(dataFileName4, 'w')
    myFPT.writelines(texto)
    
    myFPT.close()  
    myFPDE.close()
    myFPAG.close()
    if dadosTV==True:    
        if netType ==2:
            myFPID1Fase0.close()
            myFPID1Fase1.close()
            myFPID1Fase2.close()
            
            myFPID2Fase0.close()
            myFPID2Fase1.close()
            myFPID2Def.close()
            
            myFPID3Fase0.close()
            myFPID3Fase1.close()
            myFPID3Def.close()
            
            myFPID4Fase0.close()
            myFPID4Fase1.close()
            myFPID4Def.close()
        else:
            myFPID1Fase0.close()
            myFPID1Fase1.close()
            myFPID1Fase2.close()
            
            myFPID2Fase0.close()
            myFPID2Fase1.close()
            myFPID2Def.close()
            
            myFPID3Fase0.close()
            myFPID3Fase1.close()
            myFPID3Def.close()
    
        myFPciclo.close()    

    return 0
	
def AAPIUnLoad():
	return 0
def AAPIEnterPedestrian(idPedestrian, originCentroid):
	return 0
def AAPIExitPedestrian(idPedestrian, destinationCentroid):
	return 0
def AAPIEnterVehicle(idveh, idsection):
	return 0
def AAPIExitVehicle(idveh, idsection):
	return 0
def AAPIEnterVehicleSection(idveh, idsection, atime):
	return 0
def AAPIExitVehicleSection(idveh, idsection, atime):
	return 0
def AAPIPreRouteChoiceCalculation(timeSim, timeSta):
	return 0