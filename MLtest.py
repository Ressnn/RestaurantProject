# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:19:21 2019

@author: Pranav Devarinti
"""

import numpy as np
from operator import itemgetter
foods = np.random.uniform(low=-1,high=1,size=(10,100))
pan = np.random.uniform(low=0,high=1,size=(10,100))
us_ratings = np.random.uniform(low=-1,high=1,size=(10,10))
import matplotlib.pyplot as plt


def score(foods,pan):
    global us_ratings
    cl_list = []
    for i in range(len(pan)):
        user = pan[i]
        for a in range(len(us_ratings)):
            rating = us_ratings[a][i]
            food = foods[a]
            dist = np.absolute(np.subtract(user,food))
            rating = 1-rating
            cl_list.append(np.absolute(np.subtract(rating,dist)))
    return np.average(cl_list)

class Evolution():
    def __init__(self,size):
        self.size = size
        self.generate_population()
    def generate_population(self):
        self.population = []
        for i in range(self.size):
            self.population.append([np.random.uniform(low=-1,high=1,size=(10,100)),np.random.uniform(low=0,high=1,size=(10,100))])
    def score_all(self):
        global foods
        global pan
        sc_list = []
        for i in range(self.size):
            global foods
            global pan
            foods = self.population[i][0]
            pan = self.population[i][1]
            sc_list.append(score(foods,pan))
        self.scores = sc_list
        self.total = sum(self.scores)
        return sc_list
    def sort(self):
        sp_list = []
        for i in range(self.size):
            sp_list.append([self.population[i],self.scores[i]])
        sp_list.sort(key=itemgetter(1),reverse=False)
        self.sp_list = sp_list
    def half(self):
        self.sp_list = self.sp_list[:int(self.size/2)]
    def crossover(self):
        spo_list = []
        kids = []
        for i in self.sp_list:
            spo_list.append(i[0])
        for i in range(len(spo_list)):
            a = np.array(spo_list[np.random.randint(low=0,high=len(spo_list))][0])
            b = np.array(spo_list[np.random.randint(low=0,high=len(spo_list))][1])
            c = np.array(spo_list[np.random.randint(low=0,high=len(spo_list))][0])
            d = np.array(spo_list[np.random.randint(low=0,high=len(spo_list))][1])
            for r in range(10):
                for v in range(100):
                    if np.random.choice([True,False]):
                        a[r:v] = c[r:v]
                    if np.random.randint(0,10) == 0:
                        a[r:v] = np.random.uniform(-1,1)
                    if np.random.choice([True,False]):
                        b[r,v] = d[r,v]
                    if np.random.randint(0,10) == 0:
                        b[r,v] = np.random.uniform(-1,1)
                        
            kids.append([a,b])
        self.population = kids
        self.population += spo_list
    def epoch(self):
        rk = self.score_all()
        self.sort()
        self.half()
        self.crossover()
        print(np.mean(rk))
        return rk
Ev = Evolution(100)
skl = []
for i in range(0,1000):
    skl.append(Ev.epoch())
# In[]
rkl = np.mean(skl,1)
plt.plot(rkl)
rkl = np.min(skl,1)
plt.plot(rkl)
rkl = np.max(skl,1)
plt.plot(rkl)