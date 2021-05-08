#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: isegura
"""

import unittest
from fase3 import Map
from fase3 import HealthCenter


class Test(unittest.TestCase):
    
    def setUp(self):
        print('\nLos datos se inicializan para cada test..\n')
        
        #https://github.com/isegura/EDA/blob/master/grafoEjemplo.png
        #Creamos puntos de entrega
        self.centers=[]
        for x in ['A','B','C','D','E','F','G']:
            self.centers.append(HealthCenter(x))           
    
        self.m=Map()
        for p in self.centers:
            self.m.addHealthCenter(p)
        
        #print(self.m)
        
        self.m.addConnection(self.centers[0],self.centers[1],8)                    #A,B,8
        self.m.addConnection(self.centers[0],self.centers[2],9)                    #A,C,9
        self.m.addConnection(self.centers[0],self.centers[3],14)                   #A,D,14
        
        self.m.addConnection(self.centers[1],self.centers[4],15)                   #B,E,15
        self.m.addConnection(self.centers[1],self.centers[5],11)                   #B,F,11
        
        self.m.addConnection(self.centers[2],self.centers[5],2)                    #C,F,2
        
        self.m.addConnection(self.centers[5],self.centers[6],8)                    #F,G,8
        self.m.addConnection(self.centers[3],self.centers[6],2)                    #D,G,2
    
    
        #print(self.m)
        
        
        #  dfs path: A B E F C G D
        self.dfs=[self.centers[0],self.centers[1],self.centers[4],self.centers[5],self.centers[2],self.centers[6],self.centers[3]]
            
    
        #self.m.dijkstra()
        
        self.min_A_G=[self.centers[0],self.centers[3],self.centers[6]]
        self.dis_A_G=16
        
        self.min_B_D=[self.centers[1],self.centers[5],self.centers[6],self.centers[3]]
        self.dis_B_D=21
        
        self.min_E_D=[self.centers[4],self.centers[1],self.centers[5],self.centers[6],self.centers[3]]
        self.dis_E_D=36
        
        
    
        
    def test1_areConnected(self):
        #print(str(self.m))
        #comprobamos por ejemplo las conexiones de p0
        print('\n****** test1_areConnected ******************')
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[1]),8)
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[2]),9)
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[3]),14)
        #y una de sus recíprocas
        self.assertEqual(self.m.areConnected(self.centers[1],self.centers[0]),8)
        #comprobamos algunas que no están conectadas
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[4]),0)
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[5]),0)
        self.assertEqual(self.m.areConnected(self.centers[0],self.centers[6]),0)

        print('****** OK test1_areConnected ******************')
    
        
    # def test2_removeConnection(self):
    #     #print(str(self.m))
    #     #comprobamos por ejemplo las conexiones de p0
    #     print('\n****** test2_removeConnection ******************')
       
    #     self.assertEqual(self.m.areConnected(self.centers[0],self.centers[5]),0)
    #     self.m.addConnection(self.centers[0],self.centers[5],33)                    #A,B,8
    #     self.assertEqual(self.m.areConnected(self.centers[0],self.centers[5]),33)
    #     self.m.removeConnection(self.centers[0],self.centers[5])                    #A,B,8
    #     self.assertEqual(self.m.areConnected(self.centers[0],self.centers[5]),0)


    #     print('****** OK test2_removeConnection ******************')
    
           

    # def test3_createPath(self):
    #     print('\n****** test3_createPath ******************')
    #     result=self.m.createPath()
    #     self.assertEqual(len(result),len(self.dfs))
    #     for i in range(len(result)):
    #         #print(result[i],self.rutaDFS[i])
    #         self.assertEqual(result[i],self.dfs[i])
        
    #     print('****** OK test3_createPath ******************')
    
    # def test4_minimumPath(self):
    #     print('\n******  test4_minimumPath ******************')
    #     result,d=self.m.minimumPath(self.centers[0],self.centers[6])
    #     self.assertEqual(d,self.dis_A_G)
    #     self.assertEqual(len(result),len(self.min_A_G))
    #     for i in range(len(result)):
    #         self.assertEqual(result[i],self.min_A_G[i])
            
    #     print('****** OK test4_minimumPath ******************')

    # def test5_minimumPathBF(self):
    #     """test para probar la función minimumPathBF. Añade más métodos tests si lo 
    #     crees necesario para probar todos los posibles casos de esta función y que 
    #     permita probar que tu solución es robusta. """
    #     ...

    # def test6_minimumPathFW(self):
    #     """test para probar la función minimumPathFW. Añade más métodos tests si lo 
    #     crees necesario para probar todos los posibles casos de esta función y que 
    #     permita probar que tu solución es robusta. """
    #     ...

 
#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()




