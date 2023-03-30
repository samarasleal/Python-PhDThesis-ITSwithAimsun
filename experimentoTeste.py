# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 10:27:00 2016

@author: samara
"""

import numpy as np
#import random 

theCycleTime = 90.0 
#### Dicionário para salvar informações sobre detectores
detectorFields = ['id','count','speed','denst','aggregCount','aggregSpeed','aggregDenst']

#### Dicionário para salvar informações sobre movimentos de cada detector correspondente
movemFields = ['id','connPhases','cycle','satFlow','arrivFlow','queueLength', 'delay']

junctionsList = [749,741] 
networkDetectors = [[900,901,903,904],[878,879,882]]  
detectorInfo = []
for idx,thisIntersectionDetectors in enumerate(networkDetectors):
    detectorInfo.append([])
    for detector in thisIntersectionDetectors:
        detectorInfo[idx].append(dict(zip(detectorFields,[detector,0.0,0.0,0.0,0.0,0.0])))   
#
### Interseção 749 
#
movementInfo = []
movementInfo.append([])
correspDetectorId = detectorInfo[0][0]['id']
connectedPhases = [0] # movement from S to W
movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))

correspDetectorId = detectorInfo[0][1]['id']
connectedPhases = [1] # movement from E to W
movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
 
correspDetectorId = detectorInfo[0][2]['id']
connectedPhases = [2] # movement from W to N
movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))

correspDetectorId = detectorInfo[0][3]['id']
connectedPhases = [0,2] # movement from W to S
movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
#
### Interseção 741
#
movementInfo.append([])
correspDetectorId = detectorInfo[1][0]['id']
connectedPhases = [0] # movement from W to E
movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))

correspDetectorId = detectorInfo[1][1]['id']
connectedPhases = [0] # movement from E to W
movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
	
correspDetectorId = detectorInfo[1][2]['id']
connectedPhases = [1] # movement from N to S
movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	
#

# Exemplo para os movimentos acima:
splitsByMoveNow = [[[45],[55],[35],[15,30]],[[15],[25],[35]]]

detectorInfo[0][0]['count'] = 5
detectorInfo[0][1]['count'] = 6
detectorInfo[0][2]['count'] = 7
detectorInfo[0][3]['count'] = 8

detectorInfo[1][0]['count'] = 5
detectorInfo[1][1]['count'] = 6
detectorInfo[1][2]['count'] = 7


#phaseSequence = [1,0,2]
conj3PhasesIndList = [2]

# 1 offset por interseção
offset = [15,20]

def estimatedCycleDelayBHTrans(splitsByMoveNow, theCycleTime, regime, movementInfo, detectorInfo): 
    print(detectorInfo)
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
atraso = estimatedCycleDelayBHTrans(splitsByMoveNow, theCycleTime, [], movementInfo, detectorInfo)
print("Atraso")
print(atraso)

def estimatedCycleDelayByPhaseSequenceOffsetHCM(splitsByMoveNow, theCycleTime, conj3PhasesIndList, regime, movementInfo, detectorInfo, junctionsList, offset):   
    T = theCycleTime/3600
    calcDelay = 0
    D = []
    G = []
    delay = 0.0
    Dseq = 0.0
    
    ### Conjunto de possíveis sequências de fases para semáforos de 3 fases (Índice de 0 a 5 - conj3PhasesInd)
    conj3Phases = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]
    l=0
    
    nPhasesThisInter = [3,2]
    
    for id,junction in enumerate(junctionsList):
        #nPhasesThisInter = ECIGetNumberPhases(junction)
        #if (nPhasesThisInter == 3): 
        if (nPhasesThisInter[id] == 3): 
            # Calcular atraso por sequência de fases
            ind = int(conj3PhasesIndList[l])
            # Sequência de fases ex = [0,1,2]
            phaseSequence = conj3Phases[ind]
            l+=1
            for seq in range(len(phaseSequence)):
                effectGreenByPhase = 0
                flow = 0
                delayPhase = 0
                intersectMovements = movementInfo[id]
                for idxMove,move in enumerate(intersectMovements):
                    for phase in range(len(move['connPhases'])):
                        if (phaseSequence[seq] == move['connPhases'][phase]):
                            effectGreenByPhase += splitsByMoveNow[id][idxMove][phase]
                            move['arrivFlow'] = detectorInfo[id][idxMove]['count']
                            flow += move['arrivFlow']                
                proportGreen = (1.0 * effectGreenByPhase)/ theCycleTime			
                if proportGreen != 0.0:  	  				
                    capacity = ((move['satFlow']*theCycleTime)/3600.0) * proportGreen	 
                else:
                    capacity = ((move['satFlow']*theCycleTime)/3600.0) / 10.0
    
                degreeOfSat = flow / capacity
                 
                # d1 HCM Uniform Delay (Webster)
                d1 = (0.50*move['cycle']*(1 - proportGreen)**2) / ( 1 - ( np.min([1,degreeOfSat])*proportGreen ) )
        
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
                if capacity!=0.0 and T!=0.0:
                    d2 = 900 * T * ((degreeOfSat - 1) + np.sqrt((degreeOfSat - 1)**2 + ((8*k*i*degreeOfSat)/(capacity*T))))
                else:
                    d2=0
                # d3 HCM Delay Initial Queue for fully saturated period (degreeOfSat = 1.0)
                if degreeOfSat==1.0:
                    Qb = 3                    # AIMSUN - Obter Veículos no início da fila
                    u = 1.0
                    t = T
                    d3 = (1800*Qb*(1+u)*t) / (capacity*T)
                else:
                    d3 = 0
                calcDelay = ( d1 *PF )+ d2 + d3	
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
            print('Atraso total da sequencia de fases %s = %.2f da Interseção %d' %(phaseSequence,Dseq,junction))
        else: 
            # Calcular atraso por movimento
            intersectMovements = movementInfo[id]
            for idxMove,move in enumerate(intersectMovements):
                effectGreen = 0.0
                for phase in range(len(move['connPhases'])):
                    effectGreen += splitsByMoveNow[id][idxMove][phase]		      
                move['arrivFlow'] = detectorInfo[id][idxMove]['count']
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
                if capacity!=0.0 and T!=0.0:
                    d2 = 900 * T * ((degreeOfSat - 1) + np.sqrt((degreeOfSat - 1)**2 + ((8*k*i*degreeOfSat)/(capacity*T))))
                else:
                    d2=0
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
                #print("Atraso movimento %d igual a %f"%(idxMove,delayMove))
                move['delay'] = delayMove if (delayMove > 0.0) else 0.0
                delay += move['delay']	
            delay = delay + offset[id]
            print('Atraso total dos movimentos %.2f da Interseção %d' %(delay,junction))
    totalDelay = delay+Dseq 
    print("Atraso total da rede = %f"%(totalDelay))                              
    return totalDelay
estimatedCycleDelayByPhaseSequenceOffsetHCM(splitsByMoveNow, theCycleTime, conj3PhasesIndList, 0, movementInfo, detectorInfo, junctionsList, offset)                         
print('-------- || -----------')

def estimatedCycleDelayByPhaseSequenceHCM(splitsByMoveNow, regime, movementInfo, detectorInfo, phaseSequence):   
    T = theCycleTime/3600
    calcDelay = 0
    D = []
    G = []
    for seq in range(len(phaseSequence)):
        effectGreenByPhase = 0
        flow = 0
        delayPhase = 0
        for idxInt,intersectMovements in enumerate(movementInfo):
            for idxMove,move in enumerate(intersectMovements):
                for phase in range(len(move['connPhases'])):
                    if (phaseSequence[seq] == move['connPhases'][phase]):
                        effectGreenByPhase += splitsByMoveNow[idxInt][idxMove][phase]
                        move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']
                        flow += move['arrivFlow']
        # Proportion of green
        proportGreen = (1.0 * effectGreenByPhase)/ move['cycle']

        # Capacity and degreeOfSat
        capacityLane = move['satFlow'] *  proportGreen   # In hours	
        capacity = capacityLane*T                        # In hours  -> Seconds
        degreeOfSat = flow / capacity
        
        # d1 HCM Uniform Delay (Webster)
        d1 = (0.50*move['cycle']*(1 - proportGreen)**2) / ( 1 - ( np.min([1,degreeOfSat])*proportGreen ) )

        Rp = 1      # Arrival Type = 3
        P = Rp * proportGreen
        fpa = 1     # Arrival Type = 3
        PF = ( (1 - P)*fpa ) / ( 1 -  proportGreen)

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
        delayPhase += calcDelay if (calcDelay > 0.0) else 0.0
        D.append(delayPhase)
        G.append(effectGreenByPhase)
        print('Atraso phase %d igual a %.2f' %(phaseSequence[seq], delayPhase))
    
    # Dseq = D[0] + ( D[1] + (D[1]*G[0]) ) + ( D[2] + (D[2]*(G[0]+G[1])) )
    Dseq = D[0]
    i = 1
    g = 0
    j = 0
    while i < len(phaseSequence):
        while j < i:
            g = g + G[j]    
            j+=1
        Dseq = Dseq + ( D[i] + (D[i]*g) )  
        i+=1
    print('Atraso total da sequencia de fases %s = %.2f' %(phaseSequence,Dseq))

    return Dseq

#estimatedCycleDelayByPhaseSequenceHCM(splitsByMoveNow, 0, movementInfo, detectorInfo, phaseSequence)                           
#print('-------- || -----------')

def estimatedCycleDelayHCMByMov(splitsByMoveNow, regime, movementInfo, detectorInfo): 
    delay = 0.0
    T = theCycleTime/3600              # In hours -> To Seconds (For each cycle)
    delayMoveTOTAL = 0
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]
            
            print(effectGreen)	
                            
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']	
            print(move['arrivFlow'])
            
            # Proportion of green
            proportGreen = (1.0 * effectGreen)/ move['cycle']

            # Capacity and degreeOfSat
            capacityLane = move['satFlow'] *  proportGreen   # In hours	
            capacity = capacityLane*T                        # In hours  -> Seconds
            degreeOfSat = move['arrivFlow'] / capacity
            
            # d1 HCM Uniform Delay (Webster)
            d1 = (0.50*move['cycle']*(1 - proportGreen)**2) / ( 1 - ( np.min([1,degreeOfSat])*proportGreen ) )

            Rp = 1      # Arrival Type = 3
            P = Rp * proportGreen
            fpa = 1     # Arrival Type = 3
            PF = ( (1 - P)*fpa ) / ( 1 -  proportGreen)

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
            print('Atraso movimento %d igual a %f' %(idxMove, delayMove))
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delayMoveTOTAL += move['delay']
    print('Atraso total HCM %f'%(delayMoveTOTAL))	                                

    return delay
#estimatedCycleDelayHCMByMov(splitsByMoveNow, 0, movementInfo, detectorInfo)
    
def estimatedCycleDelayAkcelikByMov(splitsByMoveNow, regime, movementInfo, detectorInfo): 
    delay = 0.0
    T = theCycleTime/3600              # In hours -> To Seconds (For each cycle)
    delayMoveTOTAL = 0
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]
            
            print(effectGreen)	
                            
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']	
            print(move['arrivFlow'])
            
            # Proportion of green
            proportGreen = (1.0 * effectGreen)/ move['cycle']

            # Capacity and degreeOfSat
            capacityLane = move['satFlow'] *  proportGreen   # In hours	
            capacity = capacityLane*T                        # In hours  -> Seconds
            degreeOfSat = move['arrivFlow'] / capacity
            
            d1 = (move['cycle']*(1-proportGreen)**2) / (2*(1-proportGreen*degreeOfSat))
            
            x0 = capacity/ move['cycle']
            r = (degreeOfSat - 1)**2 + 12 * ((degreeOfSat-x0)/(capacity*T))
            calcDelay = d1 + 900 * T * ( (degreeOfSat-1)+  np.sqrt(r) )
            
            delayMove = calcDelay
            print('Atraso movimento %d igual a %f' %(idxMove, delayMove))
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delayMoveTOTAL += move['delay']
    print('Atraso total Akcelik %f'%(delayMoveTOTAL))	                                

    return delay
#estimatedCycleDelayAkcelikByMov(splitsByMoveNow, 0, movementInfo, detectorInfo)

def estimatedCycleDelayCanadianByMov(splitsByMoveNow, regime, movementInfo, detectorInfo): 
    delay = 0.0
    T = theCycleTime/3600              # In hours -> To Seconds (For each cycle)
    delayMoveTOTAL = 0
    for idxInt,intersectMovements in enumerate(movementInfo):
        for idxMove,move in enumerate(intersectMovements):
            effectGreen = 0.0
            for phase in range(len(move['connPhases'])):
                effectGreen += splitsByMoveNow[idxInt][idxMove][phase]
            
            print(effectGreen)	
                            
            move['arrivFlow'] = detectorInfo[idxInt][idxMove]['count']	
            print(move['arrivFlow'])
            
            # Proportion of green
            proportGreen = (1.0 * effectGreen)/ move['cycle']

            # Capacity and degreeOfSat
            capacityLane = move['satFlow'] *  proportGreen   # In hours	
            capacity = capacityLane*T                        # In hours  -> Seconds
            degreeOfSat = move['arrivFlow'] / capacity
            
            d1 = (move['cycle']*(1-proportGreen)**2) / (2*(1-proportGreen*degreeOfSat))
            
            r = (degreeOfSat - 1)**2 + ((4*degreeOfSat)/(capacity*T))
            calcDelay = d1 + 900 * T * ( (degreeOfSat-1)+  np.sqrt(r) )
            
            delayMove = calcDelay
            print('Atraso movimento %d igual a %f' %(idxMove, delayMove))
            move['delay'] = delayMove if (delayMove > 0.0) else 0.0
            delayMoveTOTAL += move['delay']
    print('Atraso total Canadian %f'%(delayMoveTOTAL))	                                

    return delay
#estimatedCycleDelayCanadianByMov(splitsByMoveNow, 0, movementInfo, detectorInfo)