# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:32:25 2017

@author: samara

"""

from __future__ import division 
from AAPI import *
import funcAimsun
from random import randrange
from math import *
import numpy as np

##############################          Funções criadas para os alg.Evolutivos          ############################## 
# Obter splits efetivos por movimento: ciclo -> fases -> estagios (split: estágio de verde da fase)
def getEffectiveSplitsByMovement(splitsByPhase, movementInfo):
    effectiveSplits = []
    for thisIntersec in range(len(splitsByPhase)):
        effectiveSplits.append([])
        for link in movementInfo[thisIntersec]:
            thisSplits = []
            for phases in link['connPhases']:
                thisSplits.append(splitsByPhase[thisIntersec][phases])
            effectiveSplits[thisIntersec].append(thisSplits)
    return effectiveSplits

# Check por partições (prateleira) identicas
def checkForIdenticalPartitions(partitionsThisIntersection, MINSPLIT, MAXSPLIT):
	for idx in range(len(partitionsThisIntersection)-1):
		if partitionsThisIntersection[idx] == partitionsThisIntersection[idx+1]:
			if partitionsThisIntersection[idx] > MINSPLIT:
				partitionsThisIntersection[idx] -= 1
			elif partitionsThisIntersection[idx] < MAXSPLIT:
				partitionsThisIntersection[idx]  += 1
	return partitionsThisIntersection
		
# Corrigir o arredondamento das fases para ficar igual ao tempo do ciclo		
def correctRoundedPhases2meetCycleTime(splitsList, desiredCycleTime):
	delta = sum(splitsList) - desiredCycleTime
	maxSplit = max(splitsList)
	posMax =  splitsList.index(maxSplit)
	if abs(delta) == 1:
		splitsList[posMax] -= delta
		splitsList[posMax] = int(splitsList[posMax])
	else:
		correctionTimes = min( len(splitsList),abs(delta) )
		clone = splitsList[:]  
		clone.remove(maxSplit)
		splitsList[posMax] -= delta/correctionTimes
		splitsList[posMax] = int(splitsList[posMax])
		for idx in range(correctionTimes - 1):
			maxClone = max(clone)
			posMax = splitsList.index(maxClone)
			splitsList[posMax] -= delta/correctionTimes
			splitsList[posMax] = int(splitsList[posMax])
			clone.remove(maxClone)
	return splitsList
	
# Obter splits através do percentual da partição móvel	
def getSplitsFromPercentMovablePartition(flatPartitionsNow, nIntersect, phasesInfo, MINSPLIT, MAXSPLIT, theCycleTime):
    splitsNow = []
    flatIdx = 0
    flatPartSize = len(flatPartitionsNow)
    cycleTimeThisInter = round(theCycleTime)
    for thisInter in range(nIntersect):
        # Divindo o cromossomo pela informação da fase, para cada interseção
        nPartitionsThisInter = len(phasesInfo[thisInter]['phases']) - 1
        if flatIdx < flatPartSize:
            partitionsThisInter = sorted(flatPartitionsNow[flatIdx:flatIdx+nPartitionsThisInter])
        else:
            partitionsThisInter = [ flatPartitionsNow[flatIdx] ]
        partitionsThisInter = checkForIdenticalPartitions(partitionsThisInter, MINSPLIT, MAXSPLIT)
        flatIdx += nPartitionsThisInter
        # Obter splits da partição
        cycleInSeconds = 0
        for idx in range(nPartitionsThisInter):
            if idx == 0:
                splitsNow.append([])
                thisSplitInSeconds = int(round( float(cycleTimeThisInter) * float(partitionsThisInter[0]) / 100.0 ))
                splitsNow[thisInter].append( thisSplitInSeconds )
            else:
                thisSplitInSeconds = int(round( float(cycleTimeThisInter) * float(partitionsThisInter[idx] - partitionsThisInter[idx - 1]) / 100.0 ))
                splitsNow[thisInter].append( thisSplitInSeconds )
            cycleInSeconds += thisSplitInSeconds
        lastSplitInSeconds = int(round( float(cycleTimeThisInter) * float(100 - partitionsThisInter[nPartitionsThisInter-1]) / 100.0 ))
        splitsNow[thisInter].append( lastSplitInSeconds )
        cycleInSeconds += lastSplitInSeconds
        if cycleTimeThisInter != cycleInSeconds:
            splitsNow[thisInter] = correctRoundedPhases2meetCycleTime(splitsNow[thisInter], cycleTimeThisInter)
    return splitsNow

# Setar o percentual da partição movel do split	
def setPercentMovablePartitionFromSplits(nIntersect, phasesInfo):
    flatPartitions = []
    for thisInter in range(nIntersect):
        nPhasesThisInter = len(phasesInfo[thisInter]['phases'])
        for thisPhase in range(nPhasesThisInter - 1):
            if thisPhase == 0:
                percentPartition = ( float(phasesInfo[thisInter]['phases'][thisPhase]['dur']) 
                                   / float(phasesInfo[thisInter]['cycleTime']) * 100 )
            else:
                percentPartition = ( ( float(phasesInfo[thisInter]['phases'][thisPhase]['dur'] + phasesInfo[thisInter]['phases'][thisPhase-1]['dur']) ) 
                                     / float(phasesInfo[thisInter]['cycleTime']) * 100 )
            flatPartitions.append( percentPartition )
    return flatPartitions

# Penaliza sequência de partições repetidas
def penaltyScore(chromosome, chromosomeGroupSizes):
    partitionsList = chromosome
    repeatedPartit = 0
    shift = 0
    for thisInter in range(len(chromosomeGroupSizes)):
        lastPosThisInter = shift + chromosomeGroupSizes[thisInter]
        partitionsThisInter = sorted( partitionsList[shift:lastPosThisInter] )
        for idx in range(lastPosThisInter - 1):
            if (partitionsThisInter[idx] - partitionsThisInter[idx+1]) < 1.0:
                repeatedPartit += 1
    return repeatedPartit

def estimatedCycleDelayByPhaseSequenceOffsetAkcelik(splitsByMoveNow, theCycleTime, conj3PhasesIndList, regime, movementInfo, detectorInfo, junctionsList, offset):   
    T = theCycleTime/3600
    calcDelay = 0
    totalDelay = 0
    D = []
    G = []
    Dseq = 0.0        
    ### Conjunto de possíveis sequências de fases para semáforos de 3 fases (Índice de 0 a 5 - conj3PhasesInd)
    conj3Phases = [[0,2,1],[0,1,2],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
    l=0
    offset.insert(0,0.0)    
    for id,junction in enumerate(junctionsList):
        nPhasesThisInter = ECIGetNumberPhases(junction)
        if (nPhasesThisInter == 3): 
            ind = int(conj3PhasesIndList[l])
            phaseSequence = conj3Phases[ind]
            l+=1
        else:
            # Padrão para semáforo de 2 fases
            phaseSequence = [0,1] 
        for idd, seq in enumerate(phaseSequence):
            effectGreenByPhase = 0
            flow = 0
            delayPhase = 0
            intersectMovements = movementInfo[id]
            for idxMove,move in enumerate(intersectMovements):
                for phase in range(len(move['connPhases'])):
                    if (phaseSequence[idd] == move['connPhases'][phase]):
                        effectGreenByPhase += splitsByMoveNow[id][idxMove][phase]
                        move['arrivFlow'] = detectorInfo[id][idxMove]['count']
                        flow += move['arrivFlow']
            proportGreen = (1.0 * effectGreenByPhase)/ theCycleTime			
            if proportGreen != 0.0:  	  				
                capacity = ((move['satFlow']*theCycleTime)/3600.0) * proportGreen	 
            else:
                capacity = ((move['satFlow']*theCycleTime)/3600.0) / 10.0
            
            degreeOfSat = flow / capacity
            x0 = capacity/ theCycleTime
            r = abs((degreeOfSat**2) + ((12 * (degreeOfSat-x0))/(capacity*T)))
            s = 1550
            if degreeOfSat > x0:
                No = ((capacity * T)/4) * (degreeOfSat + np.sqrt(r))
            else:
                No = 0
            d = (((move['arrivFlow']*theCycleTime)*(1-proportGreen)**2) / (2*(1 - (move['arrivFlow']/s)))) + (No*degreeOfSat)
            if move['arrivFlow'] != 0.0:
                calcDelay = d/move['arrivFlow']
            else:
                calcDelay = d                     	
            delayPhase += calcDelay if (calcDelay > 0.0) else 0.0
            D.append(delayPhase)
            G.append(effectGreenByPhase)
        #print('Atraso phase %d igual a %.2f' %(phaseSequence[seq], delayPhase))            
        # Dseq = D[0] + ( D[1] + (D[1]*G[0]) ) + ( D[2] + (D[2]*(G[0]+G[1])) )
        Dseq = D[0]
        i = 1
        g = 0
        j = 0
        while i < len(phaseSequence):
            while j < i:
                g = g + G[j]    
                j+=1
            # Atraso com offset
            Dseq = Dseq + ( D[i] + (D[i]*(g+offset[id])) )  
            i+=1
        #print('Atraso total da sequencia de fases %s = %.2f da Interseção %d' %(phaseSequence,Dseq,junction))
        D = []
        G = []
        totalDelay+=Dseq   
    #print("Atraso total da rede = %f"%(totalDelay))                              
    return totalDelay

def estimatedCycleDelayHCMByMov(splitsByMoveNow, theCycleTime, regime, movementInfo, detectorInfo): 
    T = theCycleTime/3600.0              # In hours -> To Seconds (For each cycle)
    delay = 0.0
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]		      
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']
            proportGreen = (1.0 * effectGreen)/ theCycleTime			
            if proportGreen != 0.0:  	  				
                capacity = ((move['satFlow']*theCycleTime)/3600.0) * proportGreen	 
            else:
                capacity = ((move['satFlow']*theCycleTime)/3600.0) / 10.0
            degreeOfSat = move['arrivFlow'] / capacity                              
            # d1 HCM Uniform Delay (Webster)
            d1 = (0.50*theCycleTime*(1 - proportGreen)**2) / ( 1 - ( np.min([1,degreeOfSat])*proportGreen ) )
            Rp = 1      # Arrival Type = 3
            P = Rp * proportGreen
            fpa = 1     # Arrival Type = 3
            if proportGreen!=1.0:
                PF = ( (1 - P)*fpa ) / ( 1 -  proportGreen)
            else:
                PF = 1
            # d2 HCM Incremental Delay (Akcelik)
            k = 0.5                   # For pretimed signals
            i = 1.0                   # For isolated intersections
            # For coordinated intersections and not pretimed singal, the values of i and k are given by degreeOfSat
            # Unit Extension = 3.0
            if (round(degreeOfSat,1) == 0.4):
                i = 0.922
                k = 0.11
            elif (round(degreeOfSat,1) == 0.5):
                i = 0.858
                k = 0.11
            elif (round(degreeOfSat,1) == 0.6):
                i = 0.769
                k = 0.19
            elif (round(degreeOfSat,1) == 0.7):
                i = 0.650
                k = 0.27
            elif (round(degreeOfSat,1) == 0.8):
                i = 0.5
                k = 0.34
            elif (round(degreeOfSat,1) == 0.9):
                i = 0.314
                k = 0.42
            elif (round(degreeOfSat,1) >= 1.0):
                i = 0.090
                k = 0.5
            d2 = 900 * T * ((degreeOfSat - 1) + np.sqrt((degreeOfSat - 1)**2 + ((8*k*i*degreeOfSat)/(capacity*T))))
            # d3 HCM Delay Initial Queue for fully saturated period (degreeOfSat = 1.0)
            if degreeOfSat==1.0:
                Qb = 3                    # AIMSUN - Obter Veículos no início da fila
                u = 1.0
                t = T
                d3 = (1800*Qb*(1+u)*t) / (capacity*T)
            else:
                d3 = 0
            calcDelay = ( d1 *PF )+ d2 + d3
            delayMove = calcDelay
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delay += move['delay']	                                
    return delay

def estimatedCycleDelayAkcelikByMov(splitsByMoveNow, theCycleTime, regime, movementInfo, detectorInfo): 
    delay = 0.0
    T = theCycleTime/3600              # In hours -> To Seconds (For each cycle)
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]		      
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']
            proportGreen = (1.0 * effectGreen)/ theCycleTime				
            if proportGreen != 0.0:  	  				
                capacity = ((move['satFlow']*theCycleTime)/3600.0) * proportGreen	 
            else:
                capacity = ((move['satFlow']*theCycleTime)/3600.0) / 10.0

            degreeOfSat = move['arrivFlow'] / capacity          
            x0 = capacity/ theCycleTime
            r = abs((degreeOfSat**2) + ((12 * (degreeOfSat-x0))/(capacity*T)))
            s = 1550
            if degreeOfSat > x0:
                No = ((capacity * T)/4) * (degreeOfSat + np.sqrt(r))
            else:
                No = 0
            D = (((move['arrivFlow']*theCycleTime)*(1-proportGreen)**2) / (2*(1- (move['arrivFlow']/s)))) + (No*degreeOfSat)
            calcDelay = D/move['arrivFlow']
            
            delayMove = calcDelay
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delay += move['delay']
    return delay

def estimatedCycleDelayCanadianByMov(splitsByMoveNow, theCycleTime, regime, movementInfo, detectorInfo): 
    delay = 0.0
    T = theCycleTime/3600              # In hours -> To Seconds (For each cycle)
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]		      
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']
            proportGreen = (1.0 * effectGreen)/ theCycleTime			
            if proportGreen != 0.0:  	  				
                capacity = ((move['satFlow']*theCycleTime)/3600.0) * proportGreen	 
            else:
                capacity = ((move['satFlow']*theCycleTime)/3600.0) / 10.0

            degreeOfSat = move['arrivFlow'] / capacity
            
            d1 = (theCycleTime*(1-proportGreen)**2) / (2*(1-proportGreen*degreeOfSat))
            
            r = abs((degreeOfSat - 1)**2 + ((4*degreeOfSat)/(capacity*T)))
            calcDelay = d1 + 900 * T * ( (degreeOfSat-1)+  np.sqrt(r) )
            
            delayMove = calcDelay
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delay += move['delay']
    return delay

def estimatedCycleDelayBHTrans(splitsByMoveNow, theCycleTime, regime, movementInfo, detectorInfo): 
    delay = 0.0
    degreeOfSat = 0.0
    capacity = 0.0
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]		      
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']		
            proportGreen = (1.0 * effectGreen)/ move['cycle']				
            if proportGreen != 0.0:  	  				
                capacity = ((move['satFlow']*move['cycle'])/3600) * proportGreen	 
            else:
                capacity = ((move['satFlow']*move['cycle'])/3600) / 10.0
            # Grau de saturação de 0.0 a 1.2
            degreeOfSat = move['arrivFlow'] / capacity						

            calcDelay = (move['cycle'] * (1 - proportGreen)**2) / (2 * (1-(proportGreen*degreeOfSat)))                        
            move['delay'] = calcDelay if (calcDelay > 0.0) else 0.0				
            delay += move['delay']
    return delay

def delayFitnessFunc(chromosome, chromosomeGroupSizes, nIntersections, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, nGreenTimes, junctionsList, nIntersetcionPhases, funcAtraso):
    Kp = 0.1			
    scoreDelay = 0
    evolvedPartitionsNow = []
    regime = []
    theCycleTime = 90.0
    offset = [15.0, 15.0 ,15.0 ,15.0]
    conj3PhasesIndList = [0]
    i = 0
    if funcAtraso == 1:
        for value in chromosome:
            evolvedPartitionsNow.append(value)
    elif funcAtraso == 2:
        for value in chromosome:
            evolvedPartitionsNow.append(value)
        theCycleTime = evolvedPartitionsNow.pop(-1)
    elif funcAtraso == 3:
        conj3PhasesIndList = []
        while i < nGreenTimes:
            evolvedPartitionsNow.append(chromosome[i])
            i+=1        
        theCycleTime = chromosome[nGreenTimes]
        j=nGreenTimes+1
        while j < np.size(chromosome):
            conj3PhasesIndList.append(chromosome[j])
            j+=1 
    else:
        conj3PhasesIndList = []
        offset = []
        while i < nGreenTimes:
            evolvedPartitionsNow.append(chromosome[i])
            i+=1        
        theCycleTime = chromosome[nGreenTimes]
        j=nGreenTimes+1
        nPhase = 0
        while j < np.size(chromosome):
            if nPhase < nIntersetcionPhases:
                conj3PhasesIndList.append(chromosome[j])
                nPhase+=1
            else:
                offset.append(chromosome[j])
            j+=1        
    evolvedSplitsNow = getSplitsFromPercentMovablePartition(evolvedPartitionsNow, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
    splitsByMov = getEffectiveSplitsByMovement(evolvedSplitsNow, movementInfo)
    scoreDelay = estimatedCycleDelayByPhaseSequenceOffsetAkcelik(splitsByMov, theCycleTime, conj3PhasesIndList, regime, movementInfo, detectorInfo, junctionsList, offset) + Kp * penaltyScore(evolvedPartitionsNow, chromosomeGroupSizes)
    return scoreDelay

def MANEParam(intersectionsList, delayParamDefault, timeSta, reactionT, reactionTS, reactionTL, vehMaxSpeed, vehMaxDecel, vehSpeedAccep, vehMinDist, idVehList, idInter):
    delayParamDefault = np.asarray(delayParamDefault).astype(float)
    # setar os novos valores dos parâmetros na rede
    funcAimsun.setParametersToAimsunNetwork(intersectionsList, reactionT, reactionTS, reactionTL, vehMaxSpeed, vehMaxDecel, vehSpeedAccep, vehMinDist, idVehList, idInter) 
    
    delay = funcAimsun.getDelayFromAimsunNetwork(timeSta) 
    delay = np.asarray(delay).astype(float)
    
    mane = ((delayParamDefault - delay )/ delayParamDefault) / 2
    mane = mane if mane > 0.0 else -(mane)

    return mane

def MANEFunction(evolvedPartitionsNow, nIntersections, theCycleTime, movementInfo, detectorInfo, phaseParam, MINSPLIT, MAXSPLIT, intersectionsList, delayParamDefault, timeSim, nomeFuncao, chromosomeGroupSizes):
    Kp = 0.1			
    regime = []
    delayParamDefault = np.asarray(delayParamDefault).astype(float)
    
    evolvedSplitsNow = getSplitsFromPercentMovablePartition(evolvedPartitionsNow, nIntersections, phaseParam, MINSPLIT, MAXSPLIT, theCycleTime)
    splitsByMov = getEffectiveSplitsByMovement(evolvedSplitsNow, movementInfo)
    
    if nomeFuncao == "canadian":
        delayFunc = estimatedCycleDelayCanadianByMov(splitsByMov, theCycleTime, regime, movementInfo, detectorInfo) + Kp * penaltyScore(evolvedPartitionsNow, chromosomeGroupSizes)
        print("Mane - Canadian")
    elif nomeFuncao == "HCM":
        delayFunc = estimatedCycleDelayHCMByMov(splitsByMov, theCycleTime, regime, movementInfo, detectorInfo) + Kp * penaltyScore(evolvedPartitionsNow, chromosomeGroupSizes)
        print("Mane - HCM")
    else:
        delayFunc = estimatedCycleDelayAkcelikByMov(splitsByMov, theCycleTime, regime, movementInfo, detectorInfo) + Kp * penaltyScore(evolvedPartitionsNow, chromosomeGroupSizes)
        print("Mane - Akcelik")
  
    delayFunc = np.asarray(delayFunc).astype(float)
    mane = ((delayParamDefault - delayFunc )/ delayParamDefault) / 2
    mane = mane if mane > 0.0 else -(mane)
    print(mane)
    return mane
