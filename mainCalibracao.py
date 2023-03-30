# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 15:32:25 2019

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
import copy
import time
import GACalibrarModelo
import funcCampo

##############################          Algoritmos Evolutivos          ##############################
POPSIZE = 50                # Tamanho da população AG
INIT = True
CR = 0.8                    # Probabilidade de Cruzamento
MT = 0.04                   # Probabilidade de Mutação
refresh = 10                # Atualização das iterações
decision_variableParam = [[],[],[],[],[],[],[]]
bestmenP = [[],[],[],[],[],[],[]]
numberOfParamsToEvolve = 0
reactionT=[]
reactionTS=[]
reactionTL=[]
vehMaxDSpeed=[]
vehMaxDeceleration=[]
vehSpeedAcceptance=[]
vehMinDist=[]
idVeh=[]
listIdInter=[]
qtdeFilhos = 0
solucaoElite = 0
indElite = 0

##############################          Aimsun          ##############################
controlType = 2             # 0:uncontrolled; 1:fixed; 2:external; 3:actuated 
netType = 3                 # 1:isolada, 2:em Rede  
theCycleTime = 90.0
i = 0
t = 0 

##############################          Dicionário          ##############################
# Criar dicionários de dados: detectores, movimentos, fases, etc...
dictionaries.createDictionaries(netType, theCycleTime)
junctionsList = dictionaries.junctionsList

##############################          Arquivo para informações sobre os detectores          ##############################
dataFileName3 = '/Users/samara/Dropbox/DOUTORADO/Aimsun/projeto_aimsun/ActiveControl v4- Offset/Experimentos/AGParam.dat'
myFPAGParam =  open(dataFileName3, 'w')
	
##############################          Funções do Aimsun          ##############################
def AAPILoad():
	return 0

# Inicar a simulação e os modulos	
def AAPIInit():
    global delayParamDefault    
    # Atraso total inicial da rede obtido em campo - Método das placas
    delayParamDefault = funcCampo.getDelayFromField()                 
    AKIPrintString( "My AAPIInit finalizada!" )
    return 0

# Chamada no inicío de cada passo de simulação
def AAPIManage(timeSim, timeSta, timeTrans, acycle):
    global junctionsList, delayParamDefault,POPSIZE, numberOfParamsToEvolve, decision_variableParam
    global myFPAGParam, i, t, CR, MT, refresh, bestmenP, pop, fpop, filhos, ffilhos, qtdeFilhos, solucaoElite, indElite
    
    ##########           AG - Calibrar Paramêtros da rede       ############
    if (timeSim == 120):
        AKIPrintString("My AAPIManage - Início calibração do modelo")                                
        # Obter valores iniciais dos parâmtros da rede para o AG (listas )
        reactionT, reactionTS, reactionTL, vehMaxDSpeed, vehMaxDeceleration, vehSpeedAcceptance, vehMinDist, idV, idI = funcAimsun.getParametersFromAimsunNetwork(junctionsList)
        for b in reactionT:
            decision_variableParam[0].append(b)
        for c in reactionTS:
            decision_variableParam[1].append(c)
        for d in reactionTL:
            decision_variableParam[2].append(d)
        for e in vehMaxDSpeed:
            decision_variableParam[3].append(e)
        for f in vehMaxDeceleration:
            decision_variableParam[4].append(f)
        for g in vehSpeedAcceptance:
            decision_variableParam[5].append(g)
        for h in vehMinDist:
            decision_variableParam[6].append(h)            
        for x in idI:
            listIdInter.append(x)
        for y in idV:
            idVeh.append(y)                
        AKIPrintString("Valores Iniciais dos parâmetros")
        print(decision_variableParam)
        numberOfParamsToEvolve = len(decision_variableParam) 
    
        # Rotinas de Otimização - Inicialização
        AKIPrintString( "AG - Inicializar população")                            
        pop, fpop, filhos, ffilhos = GACalibrarModelo.initGAEngine(decision_variableParam, POPSIZE, numberOfParamsToEvolve)
        
    elif timeSim>120 and timeSim<3600:   
        # Rotinas de Otimização - Evolução
        AKIPrintString( "My AAPIManage: tempo = %s - AG - Rotinas de Otimização" %(timeSim))                            
        bestmen, i, t, pop, fpop, filhos, ffilhos, qtdeFilhos, solucaoElite, indElite = GACalibrarModelo.evolveGA(indElite, solucaoElite, qtdeFilhos, pop, fpop, filhos, ffilhos, i, t, timeSim, AKIGetTimeSta()-10, refresh, myFPAGParam, POPSIZE, CR, MT, numberOfParamsToEvolve, junctionsList, delayParamDefault, decision_variableParam, idVeh, listIdInter)

    return timeSim
	
# Chamado no final de cada passo de simulação para obter informações
def AAPIPostManage(timeSim, timeSta, timeTrans, acycle):
    return 0

# Finalizar a simulação	
def AAPIFinish():
    global myFPAGParam, bestmenP, junctionsList, delayParamDefault, timeSim
    myFPAGParam.close()    
    AKIPrintString( "My AAPIFinish finalizada!" )
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