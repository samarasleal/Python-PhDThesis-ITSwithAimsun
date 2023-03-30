#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 16:53:37 2018

@author: samara
"""

import numpy as np
import matplotlib.pyplot as plt

# Região 1 - Floresta Convergência
print("++++++++++++++ Floresta ++++++++++++++")
# Média
x1 = 354.19
x2 = 252.57
x3 = 171.11
x4 = 130.64
x5 = 183.69

# Desvio Padrão
s1 = 10.79
s2 = 14.58
s3 = 16.57
s4 = 7.81
sDE = 7.58

xx1 = x4 - x1
xx2 = x4 - x2
xx3 = x4 - x3
xxDE = x4 - x5

z1 = xx1 / np.sqrt( np.abs(((s4**2)/6) - ((s1**2)/8)) )
z2 = xx2 / np.sqrt( np.abs(((s4**2)/6) - ((s2**2)/4)) )
z3 = xx3 / np.sqrt( np.abs(((s4**2)/6) - ((s3**2)/9)) )
z4 = xxDE / np.sqrt( np.abs(((s4**2)/6) - ((sDE**2)/9)) )

print("Convergência - Floresta C1, C2, C3 e DE \n")
print(z1)
print(z2)
print(z3)
print(z4)

# Região 1 - Floresta BoxPlot

a1 = [
12222.0830803,
12771.5031092,
12558.3510862,
11678.2317149,
12691.8117666,
12354.0098377,
14673.0483777,
12678.8874322
]

a2 = [
32590.7669048,
37526.5611443,
35763.6350898,
40487.6088123,
32966.2222532,
35226.6998515,
38933.9483003,
32647.7649322
]

a3SA = [
51390.4609951,
50975.6286439,
53475.9564297,
51160.8811788,
53160.0717843,
50544.0180354,
51378.3982578,
52882.0374763
]

a1 = np.array(a1)
a2 = np.array(a2)
a3 = np.array(a3SA)

data = [a1, a2, a3]

print("\nBoxplot - Floresta AG, DE e BHTrans")
label = ['CAPSI - AG', 'CAPPSI - DE', 'BhTrans']
plt.boxplot(data, labels=label)

plt.show()

# Região 1 - Floresta Boxplot - Oscilação de demanda

aaF1 = [
11830.4148068,
12325.856906,
13983.930020,
11770.0846654,
9993.38488929,
12908.9494004,
9961.9040699
]

aaF3 = [
73396.9741982,
72456.2269083,
82967.3086569,
64783.7378289,
69877.948848,
82610.2932583,
92890.8665545
]

aaF1 = np.array(aaF1)
aaF3 = np.array(aaF3)

data = [aaF1, aaF3]

label = ['CAPSI - AG', 'BhTrans']
plt.boxplot(data, labels=label)

plt.show()

print("++++++++++++++ Savassi ++++++++++++++")
# Região 2 - Savassi Convergência 
# Médias
xS1 = 58.04
xS2 = 44.37
xS3 = 19.11
xS4 = 10.1
xS5 = 30.24

# Desvio Padrão
sS1 = 4.48
sS2 = 1.73
sS3 = 3.98
sS4 = 1.61
sDES = 2.85

xxS1 = xS4 - xS1
xxS2 = xS4 - xS2
xxS3 = xS4 - xS3
xxDES = xS4 - xS5

zS1 = xxS1 / np.sqrt( np.abs(((sS4**2)/6) - ((sS1**2)/8)) )
zS2 = xxS2 / np.sqrt( np.abs(((sS4**2)/6) - ((sS2**2)/4)) )
zS3 = xxS3 / np.sqrt( np.abs(((sS4**2)/6) - ((sS3**2)/9)) )
zS4 = xxDES / np.sqrt( np.abs(((sS4**2)/6) - ((sDES**2)/9)) )

print("\n Convergência - Savassi C1, C2, C3 e DE")
print(zS1)
print(zS2)
print(zS3)
print(zS4)


# Região 2 - Savassi Boxplot

aa1 = [
5921.29928838,
4289.97686767,
3686.09533033,
5892.00983883,
7912.39838882,
6798.23166058,
5199.34663661,
8098.03930022,
9892.93030399,
7393.90029991
]

aa2 = [
67012.8621596,
73508.4070698,
69773.8539753,
71900.8828822,
73094.4623721,
64931.6378288,
72339.9939393,
61327.938833,
54636.948884,
73094.462372
]

aa3SA = [
144856.231588,
142535.388388,
132773.937771,
178399.092883,
172388.983772,
145372.467388,
130163.862598,
156603.813613,
183344.827737,
160669.525593
]

aa1 = np.array(aa1)
aa2 = np.array(aa2)
aa3 = np.array(aa3SA)

data = [aa1, aa2, aa3]

label = ['CAPSI - AG', 'CAPPSI - DE', 'BhTrans']
plt.boxplot(data, labels=label)

plt.show()

# Região 2 - Savassi Boxplot - Oscilação de demanda

aaD1 = [
7898.96574039,
8158.8221165,
7149.2813159,
6484.8992992,
7898.96574039,
8158.822116,
7149.2813159,
9024.04258836,
8312.56636711,
7276.49650293
]

aaD3 = [
242967.366537,
184290.58032,
268148.681224,
182533.946153,
263835.372845,
184881.068766
]

aaD1 = np.array(aaD1)
aaD3 = np.array(aaD3)

data = [aaD1, aaD3]

label = ['CAPSI - AG', 'BhTrans']
plt.boxplot(data, labels=label)

plt.show()


