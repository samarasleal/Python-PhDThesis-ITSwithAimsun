# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:32:25 2017

@author: samara

"""

global detectorFields, detectorInfo, movemFields, movementInfo, phaseFields, phaseParam, nIntersections, junctionsList, idmeteringList, conj3PhasesInd, conj3Phases, idSectionList

def createDictionaries(netType, theCycleTime):
    global detectorFields, detectorInfo, movemFields, movementInfo, phaseFields, phaseParam, nIntersections, junctionsList, idmeteringList, conj3PhasesInd, conj3Phases, idSectionList 

    #### Dicionário para salvar informações sobre detectores
    detectorFields = ['id','count','speed','denst','aggregCount','aggregSpeed','aggregDenst']

    #### Dicionário para salvar informações sobre movimentos de cada detector correspondente
    movemFields = ['id','connPhases','cycle','satFlow','arrivFlow','queueLength', 'delay']
    
    #### Lista para salvar informações sobre detectores de atraso (estão próximos aos detectores acima)
    idmeteringList = [1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099]
    
    #### Lista de seções
    idSectionList = [427, 333, 344, 345, 356, 394, 908, 402, 448, 401, 428, 924, 718, 972, 966, 955]

    # Interseção Isolada
    if netType==1:
        junctionsList = [741] 
    
        networkDetectors = [[878,879,882]]  
        detectorInfo = []
        for idx,thisIntersectionDetectors in enumerate(networkDetectors):
            detectorInfo.append([])
            for detector in thisIntersectionDetectors:
                detectorInfo[idx].append(dict(zip(detectorFields,[detector,0.0,0.0,0.0,0.0,0.0])))   
        movementInfo = []
        #
        ### Interseção 741
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[0][0]['id']
        connectedPhases = [0] # movement from W to E
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[0][1]['id']
        connectedPhases = [0] # movement from E to W
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        	
        correspDetectorId = detectorInfo[0][2]['id']
        connectedPhases = [1] # movement from N to S
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	
    
    # Rede de interseções - Floresta
    elif netType==2:
        junctionsList = [741,736,749,963] 
        networkDetectors = [[999,901,882],[858,862,863],[900,901,903,904],[999,901,1001]]  
        detectorInfo = []
        for idx,thisIntersectionDetectors in enumerate(networkDetectors):
            detectorInfo.append([])
            for detector in thisIntersectionDetectors:
                detectorInfo[idx].append(dict(zip(detectorFields,[detector,0.0,0.0,0.0,0.0,0.0])))   
        movementInfo = []
        #
        ### Interseção 741 - Contorno com Itajubá
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[0][0]['id']
        connectedPhases = [0] # movement from W to E
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[0][1]['id']
        connectedPhases = [0] # movement from E to W
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        	
        correspDetectorId = detectorInfo[0][2]['id']
        connectedPhases = [1] # movement from N to S
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	
        #
        ### Interseção 736 - Pouso Alegre com Curvelo
        # 
        movementInfo.append([])
        correspDetectorId = detectorInfo[1][0]['id']
        connectedPhases = [0] # movement from W to S
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[1][1]['id']
        connectedPhases = [1] # movement from E to N
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[1][2]['id']
        connectedPhases = [0] # movement from S to N 
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        #
        ### Interseção 749 - Contorno com Curvelo
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[2][0]['id']
        connectedPhases = [0] # movement from S to W
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[2][1]['id']
        connectedPhases = [1] # movement from E to W
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
         
        correspDetectorId = detectorInfo[2][2]['id']
        connectedPhases = [2] # movement from W to N
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
    
        correspDetectorId = detectorInfo[2][3]['id']
        connectedPhases = [0,2] # movement from W to S
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        #
        ### Interseção 963- Contorno com Sapucaí
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[3][0]['id']
        connectedPhases = [1] # movement from S to W
        movementInfo[3].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[3][1]['id']
        connectedPhases = [0] # movement from E to W
        movementInfo[3].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
         
        correspDetectorId = detectorInfo[3][2]['id']
        connectedPhases = [0] # movement from W to E
        movementInfo[3].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))  
    
    # Rede de interseções - Savassi
    elif netType==3:
        junctionsList = [959, 1049, 937] 
        networkDetectors = [[1066, 1067, 1066, 1072, 1066],[1073, 1070, 1071],[1067, 1066, 1069]]  
        detectorInfo = []
        for idx,thisIntersectionDetectors in enumerate(networkDetectors):
            detectorInfo.append([])
            for detector in thisIntersectionDetectors:
                detectorInfo[idx].append(dict(zip(detectorFields,[detector,0.0,0.0,0.0,0.0,0.0])))   
        movementInfo = []
        #
        ### Interseção 959 - Contorno com Getúlio Vargas
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[0][0]['id']
        connectedPhases = [0] # movement from W to E
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[0][1]['id']
        connectedPhases = [0] # movement from E to W
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        	
        correspDetectorId = detectorInfo[0][2]['id']
        connectedPhases = [1] # movement from W to N
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	

        correspDetectorId = detectorInfo[0][2]['id']
        connectedPhases = [2] # movement from N to W
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	

        correspDetectorId = detectorInfo[0][3]['id']
        connectedPhases = [0,2] # movement from N to S
        movementInfo[0].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))	
        #
        ### Interseção 1049 - Getúlio Vargas com Alagoas
        # 
        movementInfo.append([])
        correspDetectorId = detectorInfo[1][0]['id']
        connectedPhases = [0] # movement from N to S
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[1][1]['id']
        connectedPhases = [0] # movement from S to N
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1580,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[1][2]['id']
        connectedPhases = [1] # movement from S to N
        movementInfo[1].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        #
        ### Interseção 937 - Contorno com Alagoas
        #
        movementInfo.append([])
        correspDetectorId = detectorInfo[2][0]['id']
        connectedPhases = [0] # movement from E to W
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
        
        correspDetectorId = detectorInfo[2][1]['id']
        connectedPhases = [0] # movement from W to E
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
         
        correspDetectorId = detectorInfo[2][2]['id']
        connectedPhases = [1] # movement from S to N
        movementInfo[2].append(dict(zip(movemFields,[correspDetectorId,connectedPhases,theCycleTime,1550,0.0,0.0,0.0])))
       
    #### Dicionários para salvar parâmetros das fases
    nIntersections = len(junctionsList)
    phaseFields = ['readTime','dur','max','min']
    phaseParam = []
    for inter in range(nIntersections):
        phaseParam4thisIntersect = []
        phaseParam.append({'phases':phaseParam4thisIntersect,'cycleTime':0})
   
   