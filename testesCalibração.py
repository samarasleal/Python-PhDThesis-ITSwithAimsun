def MANEParam(theCycleTime, movementInfo, detectorInfo, intersectionsList, idmeteringList, delayParamDefault, timeSim, reactionT, reactionTS, reactionTL, vehMaxSpeed, vehMaxDecel, vehSpeedAccep, vehMinDist, idVehList, idInter):
    delayParamDefault = np.asarray(delayParamDefault).astype(float)
    # setar os novos valores dos parâmetros na rede
    funcAimsun.setParametersToAimsunNetwork(intersectionsList, reactionT, reactionTS, reactionTL, vehMaxSpeed, vehMaxDecel, vehSpeedAccep, vehMinDist, idVehList, idInter) 
    
    # Calcular atraso 
    meanLostTimeInt = [0,0,0,0] 
    yellowTimeInt = [0,0,0,0] 
    eGInt = [0,0,0,0]
    # Somando valores dos parâmetros por interseção
    j= 0
    while j < len(intersectionsList):
        rT = [] 
        rTS = []
        rTS = []
        rTL = []
        vMS = []
        vMD = []
        vSA = []
        vD = []
        i=0
        while i < len(idInter):
            if intersectionsList[j] == idInter[i]:
                rT.append(reactionT[i])
                rTS.append(reactionTS[i])
                rTL.append(reactionTL[i])
                vMS.append(vehMaxSpeed[i])
                vMD.append(vehMaxDecel[i])
                vSA.append(vehSpeedAccep[i])
                vD.append(vehMinDist[i])
            i+=1
        meanLostTimeInt[j] = (np.mean(rT) + np.mean(rTS) + np.mean(rTL)) / 3
        yellowTimeInt[j] = meanLostTimeInt[j] + ( np.mean(vMS) / ( 2* np.mean(vMD) ) )
        eGInt[j] = 40 +  yellowTimeInt[j] - meanLostTimeInt[j]
        j+=1

    splits = [[[eGInt[0]], [eGInt[0]], [eGInt[0]]], [[eGInt[1]], [eGInt[1]], [eGInt[1]]], [[eGInt[2]], [eGInt[2]], [eGInt[2]], [eGInt[2], eGInt[2]]], [[eGInt[3]], [eGInt[3]], [eGInt[3]]]]
    if nomeFuncao == "canadian":
        delayParamAG = estimatedCycleDelayCanadianByMov(splits, theCycleTime, [], movementInfo, detectorInfo)
    elif nomeFuncao == "HCM":
        delayParamAG = estimatedCycleDelayHCMByMov(splits, theCycleTime, regime, movementInfo, detectorInfo)
    elif nomeFuncao == "akcelik":
        delayParamAG = estimatedCycleDelayAkcelikByMov(splits, theCycleTime, regime, movementInfo, detectorInfo)
    else:
        delayParamAG = funcAimsun.getDelayFromAimsunNetwork(timeSim)    
    delayParamAG = np.asarray(delayParamAG).astype(float)
    mane = ((delayParamDefault - delayParamAG )/ delayParamDefault) / 2
    mane = mane if mane > 0.0 else -(mane)
    return mane