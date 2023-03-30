#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 22:02:00 2018

@author: samara
"""

from datetime import datetime

def getDelayFromField():
    
    # Atraso total inicial da rede obtido em campo - Método das placas
    movs = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4]
    piM = ["PVV7333", "PWA8869", "AQZ0594", "HGS7645", "OQI6355", "QON6621", "HDB0572", "OWY4521", "HNB2622", "HNR7908"]
    hiM = ["08:25:28", "08:27:10", "09:13:20", "09:16:05", "09:30:40", "09:31:55", "09:33:45", "09:58:40", "09:59:00", "10:01:15"]
    sM = ["F", "A", "F", "A", "F", "F", "A", "F", "A", "A"]
    
    pfM = ["PVV7333", "PWA8869", "AQZ0594", "HGS7645", "OQI6355", "QON6621", "HDB0572", "OWY4521", "HNB2622", "HNR7908"]
    hfM = ["08:27:32", "08:27:41", "09:14:52", "09:15:52", "09:33:08", "09:34:36", "09:34:00", "10:00:29", "09:59:25", "10:02:24"]
    
    i=0
    AtrasoFM1 = 0
    AtrasoAM1 = 0
    AtrasoFM2 = 0
    AtrasoAM2 = 0
    AtrasoFM3 = 0
    AtrasoAM3 = 0
    AtrasoFM4 = 0
    AtrasoAM4 = 0
    countFM1 = 0
    countAM1 = 0
    countFM2 = 0
    countAM2 = 0
    countFM3 = 0
    countAM3 = 0
    countFM4 = 0
    countAM4 = 0
    atrasoM1 = 0
    atrasoM2 = 0
    atrasoM3 = 0
    atrasoM4 = 0
    while i<len(piM):
        j=0
        while j<len(pfM):
            if piM[i]==pfM[j]:
                horarioDateI = datetime.strptime(hiM[i],"%H:%M:%S")
                horarioDateF = datetime.strptime(hfM[j],"%H:%M:%S")
                dif = horarioDateF - horarioDateI
                if movs[i]==1:            
                    if sM[i]=="F":               
                        AtrasoFM1 = AtrasoFM1 + dif.total_seconds()
                        countFM1+=1
                    elif sM[i]=="A":
                        AtrasoAM1 = AtrasoAM1 + dif.total_seconds()
                        countAM1+=1
                elif movs[i]==2:            
                    if sM[i]=="F":               
                        AtrasoFM2 = AtrasoFM2 + dif.total_seconds()
                        countFM2+=1
                    elif sM[i]=="A":
                        AtrasoAM2 = AtrasoAM2 + dif.total_seconds()
                        countAM2+=1                    
                elif movs[i]==3:            
                    if sM[i]=="F":               
                        AtrasoFM3 = AtrasoFM3 + dif.total_seconds()
                        countFM3+=1
                    elif sM[i]=="A":
                        AtrasoAM3 = AtrasoAM3 + dif.total_seconds()
                        countAM3+=1
                else:            
                    if sM[i]=="F":               
                        AtrasoFM4 = AtrasoFM4 + dif.total_seconds()
                        countFM4+=1
                    elif sM[i]=="A":
                        AtrasoAM4 = AtrasoAM4 + dif.total_seconds()
                        countAM4+=1
            j+=1
        i+=1
    if AtrasoFM1!=0 and AtrasoAM1!=0:
        #print("Movimento 1")
        atrasoM1 =AtrasoFM1/countFM1 - AtrasoAM1/countAM1
        #print(atrasoM1)
    if AtrasoFM2!=0 and AtrasoAM2!=0:
        atrasoM2 = AtrasoFM2/countFM2 - AtrasoAM2/countAM2
        #print("Movimento 2")
        #print(atrasoM2)
    if AtrasoFM3!=0 and AtrasoAM3!=0:
        #print("Movimento 3")
        atrasoM3 = AtrasoFM3/countFM3 - AtrasoAM3/countAM3
        #print(atrasoM3)
    if AtrasoFM4!=0 and AtrasoAM3!=0:
        #print("Movimento 4")
        atrasoM4 = AtrasoFM4/countFM4 - AtrasoAM4/countAM4
        #print(atrasoM4)
    
    #print("----")
    # print("Interseção 1 - 741")
    atrasoI1 = atrasoM3 + atrasoM1 + atrasoM4
    # print("Interseção 2 - 736")
    atrasoI2 = atrasoM3 + atrasoM2 + atrasoM3
    # print("Interseção 3 - 749")
    atrasoI3 = atrasoM1 + atrasoM4 + atrasoM2
    # print("Interseção 4 - 963")
    atrasoI4 = atrasoM4 + atrasoM1
    
    #print("Atraso total real")
    total = (atrasoI1 + atrasoI2 + atrasoI3 + atrasoI4)/4
    #print(total)
    return total

    