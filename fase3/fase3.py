#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:49:06 2020

@author: isegura
"""
import sys


class HealthCenter():
    def __init__(self,name=None):
        self.name=name
        
        
    def __eq__(self,other):
        return  other!=None and self.name==other.name
    
    def __str__(self):
        return self.name


class AdjacentVertex:
  def __init__(self,vertex,weight):
    """
    vertex: The index (0,1,2,...) of the vertex it has a connection to.
    weigth: Integer that represents the weight of that connection.
    """
    self.vertex=vertex
    self.weight=weight
  
  def __str__(self):
    return '('+str(self.vertex)+','+str(self.weight)+')'
 
class Map():
    def __init__(self):
        # self.centers: Dictionary of HealthCenter elements -> Attribute .name
        self.centers={}
        # self.vertices: Dictionary of AdjacentVertex elements -> Attributes: .vertex, .weight
        self.vertices={}
    
    def addHealthCenter(self,center):
        """Updates the centers dict by adding a new HealthCenter given as input"""
        # The index of the last element is len(self.centers) - 1
        # That means, `i` would be the index of the new element
        i=len(self.centers)
        self.centers[i]=center
        self.vertices[i]=[]
        
    def _getIndice(self,center):
        """Look for a `center` in self.centers and return its index (else return -1)"""
        # See the method addHealthCenter, the keys of self.centers
        # are simply 0, 1, 2, 3, ..., len(self.centers) - 1
        for index in self.centers.keys():
            if self.centers[index]==center:
                return index
        return -1
        
    def __str__(self):
        result=''
        for i in self.vertices.keys():
            result+=str(self.centers[i])+':\n'
            for adj in self.vertices[i]:
                result+='\t'+str(self.centers[adj.vertex])+', distance:'+str(adj.weight)+'\n'
        return result
    
       
    def addConnection(self,center1,center2,distance):
        """Create a new vertex between two centers using the AdjancentVertex class.

        Args:
            center1, center2: HealthCenters that will have a connection between them.
            distance: Integer that represents the distance between center1 and center2.
        
        """
        # Get the indices
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)

        # Make sure that the indices are correct
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        # Add the vertices for both HealthCenters (index1, index2)
        self.vertices[index1].append(AdjacentVertex(index2,distance))
        self.vertices[index2].append(AdjacentVertex(index1,distance))

        
    def areConnected(self,center1,center2):
        """If there's a vertex from center1 to center2, return the weight (else return 0)"""
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)

        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        # adj means adjacent. It's the index of the vertex our center has connection to.

        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                return adj.weight
        
        return 0
            
    def removeConnection(self,center1,center2):
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)

        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        # Keep in mind, there's a connection from center1 to center2 and
        # another one from center2 to center1. That's why we have 2 for loops.

        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                self.vertices[index1].remove(adj)
                break
                
        for adj in self.vertices[index2]:
            if adj.vertex==index1:
                self.vertices[index2].remove(adj)
                break


    def createPath(self): 
        """This function prints the vertices by dfs algorithm"""
        #print('dfs traversal:')
        # Mark all the vertices as not visited 
        visited = [False] * len(self.vertices)

        paths=[]
        for v in  self.vertices:
            if visited[v]==False:
                # Remember, as visited and paths are references to the list, if we change
                # them inside the the method _dfs, they will be changed inside createPath
                self._dfs(v, visited,paths)
        
        print()
        return paths
        
    def _dfs(self, v, visited,paths): 
        # Mark the current node as visited and print it 
        visited[v] = True
        #print(self.centers[v], end = ' ') 
        paths.append(self.centers[v])
        # Recur for all the vertices  adjacent to this vertex 
        for adj in self.vertices[v]: 
          i=adj.vertex
          if visited[i] == False: 
            self._dfs(i, visited,paths) 
            
            
    
    def printSolution(self,distances,previous,v): 
        """imprime los caminos mínimos desde v"""
        for i in range(len(self.vertices)):
          if distances[i]==sys.maxsize:
            print("There is not path from ",v,' to ',i)
          else: 
            minimum_path=[]
            prev=previous[i]
            while prev!=-1:
              minimum_path.insert(0,self.centers[prev])
              prev=previous[prev]
            
            minimum_path.append(self.centers[i])  
    
            print('Ruta mínima de:',self.centers[v],'->',self.centers[i],", distance", distances[i], ', ruta: ',  end= ' ')
            for x in minimum_path:
                print(x,end= ' ')
            print()
    
    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) with the mininum distance. To do this, 
        we see in the list distances. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 
    
        #returns the vertex with minimum distance from the non-visited vertices
        for i in range(len(self.vertices)): 
          if distances[i] <= min and visited[i] == False: 
            min = distances[i] 
            min_index = i 
      
        return min_index 
    
    def dijkstra(self, v=0): 
        """"This function takes the index of a delivery point pto and calculates its mininum path 
        to the rest of vertices by using the Dijkstra algoritm. Devuelve una lista con las distancias
        y una lista con los vértices anteriores a uno dado en el camino mínimo"""  
        
        
        #we use a Python list of boolean to save those nodes that have already been visited  
        visited = [False] * len(self.vertices) 
    
        #this list will save the previous vertex 
        previous=[-1]*len(self.vertices) 
    
        #This array will save the accumulate distance from v to each node
        distances = [sys.maxsize]*len(self.vertices) 
        #The distance from v to itself is 0
        distances[v] = 0
    
        for i in range(len(self.vertices)): 
          # Pick the vertex with the minimum distance vertex.
          # u is always equal to v in first iteration 
          u = self.minDistance(distances, visited) 
          # Put the minimum distance vertex in the shotest path tree
          visited[u] = True
          
          # Update distance value of the u's adjacent vertices only if the current  
          # distance is greater than new distance and the vertex in not in the shotest path tree 
          for adj in self.vertices[u]:
            i=adj.vertex
            w=adj.weight
            if visited[i]==False and distances[i]>distances[u]+w:
              distances[i]=distances[u]+w   
              previous[i]=u       
              
        #finally, we print the minimum path from v to the other vertices
        #self.printSolution(distances,previous,v)
        return previous,distances
 
    def minimumPath(self, start, end):
        """calcula la ruta mínima entre dos puntos de entrega"""
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None
        
        previous,distances=self.dijkstra(indexStart)
        
        #construimos el camino mínimo
        minimum_path=[]
        prev=previous[indexEnd]
        while prev!=-1:
            minimum_path.insert(0,str(self.centers[prev]))
            prev=previous[prev]
            
        minimum_path.append(str(self.centers[indexEnd]))
        return minimum_path, distances[indexEnd]
    
    def minimumPathBF(self,start,end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Bellman-Ford. Puedes implementar otras funciones auxiliares si lo consideras necesario """
        minimum_path=[]
        minimumDistance=0
        
        # GET THE INDICES (start and end)
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None

        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None
        
        # INITIALIZE THE DISTANCES (from indexStart to all the other vertices)
        #
        # keep in mind that there can be multiple ways to go to indexEnd,
        # that's why we have to go over all nodes
        distances = [sys.maxsize]*len(self.vertices) # sys.maxsize == infinite
        distances[indexStart] = 0 # distance from v to itself is 0
        
        # INTIALIZE THE PREVIOUS ARRAY
        previous=[-1]*len(self.vertices) 

        # RELAX ALL EDGES (|V| - 1 times)
        #
        # head_vertex: Vertex from which we start
        # tail_vertex: Vertex that we reach
        for _ in range(len(self.vertices) - 1):
            for i_head in self.vertices:
                for tail_vertex in self.vertices[i_head]:
                    i_tail = tail_vertex.vertex
                    weight = tail_vertex.weight

                    if distances[i_head] > distances[i_tail] + weight:
                        distances[i_head] = distances[i_tail] + weight
                        previous[i_head] = i_tail

        # Check that we found a way to go to out target node
        if distances[indexEnd] == sys.maxsize:
            raise RuntimeError("There's not a shortest path to that node")
        
        # Append all the previous nodes to the minimum path
        prev = previous[indexEnd]
        while prev != -1:
            minimum_path.insert(0, str(self.centers[prev]))
            prev = previous[prev]

        
        # Append the last node to the minimum path
        minimum_path.append(str(self.centers[indexEnd]))
        
        minimumDistance = distances[indexEnd]

        return minimum_path, minimumDistance
        
    def constructPath(self, path_matrix, min_path, i, j):
        if i == j:
            min_path.append(str(self.centers[i]))
        else:
            self.constructPath(path_matrix, min_path, i, path_matrix[i][j])
            min_path.append(str(self.centers[j]))

    def minimumPathFW(self,start,end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Floyd-Warshall. Puedes implementar otras funciones auxiliares si lo consideras necesario"""
        minimum_path=[]
        minimumDistance=0

        # GET THE INDICES (start and end)
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None

        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None

        # CREATE THE ADJACENCY MATRIX
        distances = [ [float("Inf") for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]

        # Give values to the distances matrix
        for v in self.vertices:
            distances[v][v] = 0

            for tail_vertex in self.vertices[v]:
                u = tail_vertex.vertex
                weight = tail_vertex.weight
                
                distances[u][v] = weight

        # CREATE THE PATH MATRIX
        min_path_matrix = [ [ 0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]

        # Give values to the path matrix
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                min_path_matrix[i][j] = i

                if (i != j and distances[i][j] == 0):
                    min_path_matrix[i][j] = -30000

        for k in range(len(self.vertices)):
            for i in range(len(self.vertices)):
                for j in range(len(self.vertices)):
                    
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        min_path_matrix[i][j] = min_path_matrix[k][j]

        self.constructPath(min_path_matrix, minimum_path, indexStart, indexEnd)
        minimumDistance = distances[indexStart][indexEnd]

        return minimum_path, minimumDistance

def test():
    #https://www.bogotobogo.com/python/images/Dijkstra/graph_diagram.png
   
    m=Map()
    for c in ['A','B','C','D','E','F']:
        m.addHealthCenter(HealthCenter(c))
    
    # print(m)
    m.addConnection(m.centers[0],m.centers[1],7)#A,B,7
    m.addConnection(m.centers[0],m.centers[2],9)#A,C,9
    m.addConnection(m.centers[0],m.centers[5],14)#A,F,14
    
    m.addConnection(m.centers[1],m.centers[2],10)#B,C,10
    m.addConnection(m.centers[1],m.centers[3],15)#B,D,15
    
    m.addConnection(m.centers[2],m.centers[3],11)#C,D,11
    m.addConnection(m.centers[2],m.centers[5],2)#C,F,2
    
    m.addConnection(m.centers[3],m.centers[4],6)#D,E,6
    
    m.addConnection(m.centers[4],m.centers[5],9)#E,F,9
    # print(m)
    
    
    c1=m.centers[0]
    c2=m.centers[3]
    # print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    # c2=m.centers[1]
    # print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    # m.removeConnection(c1,c2)
    # print(m)
    
    # print('createPath:',end=' ')
    # ruta=m.createPath()
    # #print('Ruta:',ruta)
    # for r in ruta:
    #     print(r, end=' ')
    # print()
    
    # minimum_path,d=m.minimumPath(c1,c2)
    # for p in minimum_path:
    #     print(p,end=' ')
    # print('total distance:',d)

    #añade más pruebas para probar los dos nuevos métodos minimumPathBF y minimumPathFW
    # minimum_path,d=m.minimumPathBF(c1,c2)
    # for p in minimum_path:
    #     print(p,end=' ')
    # print('total distance:',d)

    # minimum_path,d=m.minimumPathFW(c1,c2)
    # for p in minimum_path:
    #     print(p,end=' ')
    # print('total distance:',d)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    test()