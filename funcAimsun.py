# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:32:25 2017

@author: samara

"""
from __future__ import division 
from AAPI import *
INIT = True
##############################          Funções criadas para o Aimsun          ############################## 
# Obter o valor dos parâmetros da rede por interseção
def getParametersFromAimsunNetwork(intersectionsList):
    nIntersect = len(intersectionsList)
    reactionT = []
    reactionTS = []
    reactionTL = []
    vehMaxDSpeed = []
    vehMaxDeceleration = []
    vehSpeedAcceptance = []
    vehMinDist = [] 
    idVeh = []
    listIdInter = []
    i=0
    while (i<nIntersect):
        idInter = AKIInfNetGetJunctionId(i)
        numVeic = AKIVehStateGetNbVehiclesJunction(idInter)
        j=0
        while (j<numVeic):
            infVeh = AKIVehGetVehicleStaticInfJunction(idInter,j)
            if (infVeh.report==0):
                #astring = "Vehicle " + str(infVeh.idVeh) + ", Intersection ID " + str(idInter) + ", Reaction Time " + str(infVeh.reactionTime) + " , Reaction Time at Stop " + str(infVeh.reactionTimeAtStop) + ", Reaction Time At Traffic Light " + str(infVeh.reactionTimeAtTrafficLight) + ", Maximum Desired Speed " +str(infVeh.maxDesiredSpeed) + ", Maximum Deceleration " + str(infVeh.vehMaxDeceleration) + ", Speed Acceptance " + str(infVeh.speedAcceptance) + ", Minimun Distance " + str(infVeh.minDistanceVeh) 
                #AKIPrintString(astring)
                listIdInter.append(idInter)
                idVeh.append(infVeh.idVeh)
                reactionT.append(infVeh.reactionTime)
                reactionTS.append(infVeh.reactionTimeAtStop)
                reactionTL.append(infVeh.reactionTimeAtTrafficLight)
                vehMaxDSpeed.append(infVeh.maxDesiredSpeed)
                vehMaxDeceleration.append(infVeh.maxDeceleration)
                vehSpeedAcceptance.append(infVeh.speedAcceptance)
                vehMinDist.append(infVeh.minDistanceVeh)
            else:
                AKIPrintString("Erro ao obter informações da interseção")
            j+=1
        i+=1  
    return reactionT, reactionTS, reactionTL, vehMaxDSpeed, vehMaxDeceleration, vehSpeedAcceptance, vehMinDist, idVeh, listIdInter

# Setar o valor dos parâmetros da rede por interseção
def setParametersToAimsunNetwork(intersectionsList, reactionT, reactionTS, reactionTL, vehMaxSpeed, vehMaxDecel, vehSpeedAccep, vehMinDist, idVehList, idInterList):
    nIntersect = len(intersectionsList)
    i=0
    while (i<nIntersect):
        idInter = AKIInfNetGetJunctionId(i)
        numVeic = AKIVehStateGetNbVehiclesJunction(idInter)
        j=0
        while (j<numVeic):
            infVeh = AKIVehGetVehicleStaticInfJunction(idInter,j)
            if (infVeh.report==0):
                #astring = "Vehicle " + str(infVeh.idVeh) + ", Intersection ID " + str(idInter) + ", Reaction Time " + str(infVeh.reactionTime) + " , Reaction Time at Stop " + str(infVeh.reactionTimeAtStop) + ", Reaction Time At Traffic Light " + str(infVeh.reactionTimeAtTrafficLight) + ", Maximum Desired Speed " +str(infVeh.maxDesiredSpeed) + ", Maximum Deceleration " + str(infVeh.maxDeceleration) + ", Speed Acceptance " + str(infVeh.speedAcceptance) + ", Minimun Distance " + str(infVeh.minDistanceVeh) 
                #AKIPrintString(astring)
                idL=0
                while (idL < len(idInterList)):
                    if idInter == idInterList[idL]:
                        infVeh.reactionTime = reactionT[idL]
                        infVeh.reactionTimeAtStop = reactionTS[idL]
                        infVeh.reactionTimeAtTrafficLight = reactionTL[idL]
                        infVeh.maxDesiredSpeed = vehMaxSpeed[idL]
                        infVeh.maxDeceleration = vehMaxDecel[idL]
                        infVeh.speedAcceptance = vehSpeedAccep[idL]
                        infVeh.minDistanceVeh = vehMinDist[idL]
                        retornoSet = AKIVehSetVehicleStaticInfJunction(idInter, j, infVeh)    
                        if (retornoSet==0):
                            infVeh2 = AKIVehGetVehicleStaticInfJunction(idInter,j)
                            #print("Parâmetros foram setados")
                            #astring = "Vehicle " + str(infVeh2.idVeh) + ", Intersection ID " + str(idInter) + ", Reaction Time " + str(infVeh2.reactionTime) + " , Reaction Time at Stop " + str(infVeh2.reactionTimeAtStop) + ", Reaction Time At Traffic Light " + str(infVeh2.reactionTimeAtTrafficLight) + ", Maximum Desired Speed " +str(infVeh2.maxDesiredSpeed) + ", Maximum Acceleration " + str(infVeh2.maxAcceleration) + ", Speed Acceptance " + str(infVeh2.speedAcceptance) + ", Minimun Distance " + str(infVeh2.minDistanceVeh) 
                            #AKIPrintString(astring)
                        else:
                            print("Erro ao setar informações da interseção")
                            print(retornoSet)
                    idL+=1
            else:
                AKIPrintString("Erro ao obter informações da interseção")
            j+=1
        i+=1  

def getDelayFromAimsunNetwork(timeSta):
    estad = AKIEstGetParcialStatisticsSystem(timeSta,0)
    if estad.report == 0:
        delay = estad.DTa
    elif estad.report == -6002:
        AKIPrintString("==> Error: Não há informação estatística disponível")
        ANGSetSimulationOrder(3,0) # 3: Para a simulação
    else:
        AKIPrintString("==> Error: Não foi possível obter o delay do AIMSUN")
        ANGSetSimulationOrder(3,0) # 3: Para a simulação 
    return delay

# Obter splits por fase	
def getInfoFromAimsunNetwork(intersectionsList, phasesInfo, mode, timeSta, phaseFields):
    durPt = doublep()
    maxPt = doublep()
    minPt = doublep()    
    thisSigVal = [0.0,0.0,0.0,0.0]
    nIntersect = len(intersectionsList)
    splitsByPhase = [] 
    vars2Evolve = 0
    chromoGroupSizes = []
    for thisInter in range(nIntersect):
        splitsByPhase.append([])
        nPhasesThisInter = ECIGetNumberPhases(intersectionsList[thisInter]) 
        # AG: Encontrar tamanho de cada grupo de partições dentro do cromossomo (cada grupo de partições = nPhases -1)
        chromoGroupSizes.append(nPhasesThisInter - 1)
        thisPhaseCycleTime = 0
        for thisPhase in range(nPhasesThisInter):
            # Obter informações atuais do split através do Aimsun
            returnError = 0	
            returnError = ECIGetDurationsPhase(intersectionsList[thisInter], thisPhase+1, \
            timeSta, durPt, maxPt, minPt)
            if returnError < 0:
                AKIPrintString( "==> Error: Param do sinal nao encontrado. Finalizando..." )
                ANGSetSimulationOrder(3,0) # 3: Para a simulação 
            else:
                thisSigVal[0] = timeSta
                thisSigVal[1] = durPt.value()
                thisSigVal[2] = maxPt.value()
                thisSigVal[3] = minPt.value()                
                thisPhaseCycleTime += thisSigVal[1]                
                # Criar/Modificar estrutura da phasesInfo
                if mode==True:
                    phasesInfo[thisInter]['phases'].append(dict(zip(phaseFields,thisSigVal)))
                else:
                    phasesInfo[thisInter]['phases'][thisPhase] = dict(zip(phaseFields,thisSigVal))
                # Update lista de novos splits por fase
                splitsByPhase[thisInter].append(thisSigVal[1])
                vars2Evolve += 1
        phasesInfo[thisInter]['cycleTime'] = thisPhaseCycleTime
        vars2Evolve -= 1  # AG: Para cada interseção, vars2Evolve = nPhases -1, porcausa das partições móveis
    # Tempo de ciclo será parte do indivíduo (1 variável a mais em var2evolve)
    vars2Evolve = vars2Evolve + 1   
    return splitsByPhase, vars2Evolve, chromoGroupSizes, thisPhaseCycleTime

# Setar novos splits	
def setInfoToAimsunNetwork(newSplits, intersectionsList, phasesInfo, timeSim):
    nIntersect = len(intersectionsList)
    returnErrorVec = [0] * nIntersect
    for thisInter in range(nIntersect):
        nPhasesThisInter = len(phasesInfo[thisInter]['phases'])
        for thisPhase in range(nPhasesThisInter):
            phasesInfo[thisInter]['phases'][thisPhase]['dur'] = newSplits[thisInter][thisPhase]
            returnErrorVec[thisInter] += ECIChangeTimingPhase(intersectionsList[thisInter],thisPhase+1,newSplits[thisInter][thisPhase],timeSim)
            if sum(returnErrorVec) != 0:
                print("ERROR changing splits in the AIMSUN network!!!")
    return returnErrorVec