import numpy as np
import itertools as it
import math
import gc


#from App.DataBase.db import *

class ModelosIniciales():
    """
        Plantear los modelos matemáticos iniciales y escoger
        el de mayor efecto.
    """

    def __init__(self, datos, NormDist, Efecto, nombre):
        self.Mejores = {}
        self.contador = 1
        #Creación base de datos
        """
        nombre = 'App/DataBase/' + nombre
        BD = DataBase(nombre)
        BD.Create()
        """

        #Llenado de la base de datos
        self.Combinaciones(datos, Efecto, NormDist, nombre)

        self.Selection()

    def Selection(self):
        Rmax = 0
        eliminar = []
        for key in self.Mejores:
            if self.Mejores[key] is not None and \
                 self.Mejores[key]['R2aju'] > Rmax:
                Rmax = self.Mejores[key]['R2aju']
                self.Mejor = self.Mejores[key]
            elif self.Mejores[key] is None:
                eliminar.append(key)
        
        for key in eliminar:
            self.Mejores.pop(key, None)
            
    def Calculos(self, Ecu, Y, NormDist, nombre, exponentes, Ecc = False, \
            matrix = False, matrixx = False):
        try:
            dic = {
                'Ecuación':Ecu,
                'Variables': {}
            }
            M = []
            M.append(np.ones(NormDist['N_Datos']))
            contador = 0
            if matrixx:
                dic['Matriz exp'] = np.array(matrix)
                Y = np.transpose(Y)
                Y = Y[0]
            else:
                for i in range(len(Ecu)):
                    dic['Variables'][Ecu[i]] = {}
                    subdic= {
                        'Exponentes': {},
                        'Vector': np.ones(NormDist['N_Datos'])
                    }
                    if Ecc:
                        Ecuu = Ecc[i]
                    else:
                        Ecuu = Ecu[i]
                    for Ec in Ecuu:
                        subdic['Exponentes'][Ec] = exponentes[contador]
                        for k in range(int(exponentes[contador])):
                            subdic['Vector'] *= NormDist[Ec]['Vector']
                        contador += 1
                    dic['Variables'][Ecu[i]] = subdic
                    M.append(dic['Variables'][Ecu[i]]['Vector'])
                dic['Matriz exp'] = np.transpose(np.array(M))
            dic['Bs'] = np.matmul(
                np.matmul(
                    np.linalg.inv(np.matmul(
                        np.transpose(dic['Matriz exp']),
                        dic['Matriz exp']
                        )),
                    np.transpose(
                        dic['Matriz exp'])),
                np.transpose(Y)
                )
            dic['Ycal'] = np.matmul(
                dic['Matriz exp'],
                dic['Bs']
                )
            #Yi - Ycal, Yi - Yexpprom
            dic['Yi-Ycal'] = np.zeros(NormDist['N_Datos'])
            dic['Yi-Yexpprom'] = np.zeros(NormDist['N_Datos'])
            for i in range(NormDist['N_Datos']):
                dic['Yi-Ycal'][i] = \
                    Y[i] - dic['Ycal'][i]
                dic['Yi-Yexpprom'][i] = \
                    Y[i] - np.mean(Y)
            SSreg = np.sum(dic['Yi-Ycal']**2)
            SStot = np.sum(dic['Yi-Yexpprom']**2)
            dic['R2'] = (SStot-\
                    SSreg)/SStot
            dic['R2aju'] = 0
            if NormDist['N_Datos']- len(dic['Ecuación'])-1 != 0:
                dic['R2aju'] = \
                    (SStot/(NormDist['N_Datos']-1)-\
                        SSreg/(NormDist['N_Datos']-\
                            len(dic['Ecuación'])-\
                            1))/(SStot/(NormDist['N_Datos']-1))
            if dic['R2aju'] > 1:
                dic['R2aju'] = 0
            #self.Guardar(dic, nombre)
            return dic
        except:
            pass

    def Guardar(self, dic, nombre):
        model = Modelo(nombre, dic)
        model.Create()

    def Combinaciones(self, datos, Efecto, NormDist, nombre):
        cont = 1
        for i in range(len(Efecto)):
            Ecu = list(it.combinations(Efecto, i+1))
            for Ec in Ecu:
                contador = 0
                for i in range(len(Ec)):
                    for E in Ec[i]:
                        contador += 1
                exponentes = np.ones(contador)
                dic = self.Calculos(Ec, datos['Y'], NormDist, nombre, exponentes)
                self.Mejores[cont] = dic
                cont += 1

    def combinations(self, iterable, r, datos, NormDist, nombre):
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        while True:
            Ec = list(pool[i] for i in indices)
            self.Calculos(Ec, datos, NormDist, nombre)
            #print(Ec)
            del Ec
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                gc.collect()
                return
            indices[i]  += 1
            
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1


    def __call__(self):
        return self.Mejores

class ModeloFinal(ModelosIniciales):
    """
        A partir del mejor modelo inicial, se desarrolla un proceso iterativo
        que permita seleccionar los exponentes finales.
    """
    def __init__(self, Ecuacion, NormDist, ref = 0.82, Y = None,\
                     maximo = 3, db = 'db', Porcentaje = 0.85):
        self.Respuestas = {}
        self.Ans = {}
        comb = self.CombExp(Ecuacion, maximo)
        self.Solucion(comb, NormDist, Y, db, ref, Porcentaje)
        #self.Selection()

    def CombExp(self, Ecuacion, maximo):
        #Exponentes
        contador = 0
        for i in range(len(Ecuacion)):
            for E in Ecuacion[i]:
                contador += 1
        exponentes = np.ones(contador)

        comb = []
        for Ec in Ecuacion:
            cont = np.ones(len(Ec))
            ultimo = len(Ec)-1
            while ultimo != -1:
                var = ''
                for i in range(len(Ec)):
                    if i == len(Ec)-1:
                        for j in range(maximo):
                            comb.append(var + Ec[i] + str(int(cont[i])))
                            cont[i] += 1
                        cont[i] = 1
                        var = ''
                        if cont[ultimo] == maximo or ultimo == len(Ec)-1:
                            ultimo -= 1
                        cont[ultimo] += 1
                        var = ''
                    else:
                        var += Ec[i] + str(int(cont[i]))
        return comb

    def Solucion(self, Exp, NormDist, Y, nombre, ref, porcentaje):
        self.Ans = None
        Cont = True
        for i in range(len(Exp)):
            if Cont:
                Ecu = list(it.combinations(Exp, i+1))
                for i in range(len(Ecu)):
                    if Cont:
                        exponentes = []
                        Ec = []
                        for j in range(len(Ecu[i])):
                            val = ''
                            for k in range(len(Ecu[i][j])):
                                try:
                                    exponentes.append(int(Ecu[i][j][k]))
                                except:
                                    if k <= len(Ecu[i][j])-2:
                                        val += Ecu[i][j][k]
                            Ec.append(val)
                        if NormDist['N_Datos']- len(Ecu[i])-1 >= 1:
                            Ans = self.Calculos(Ecu[i], Y, NormDist, nombre, exponentes, Ec)
                        else:
                            Ans = None
                        try:
                            if Ans['R2aju'] > ref:
                                self.Ans = Ans
                                Cont = False
                                break
                            elif Ans['R2aju'] > porcentaje*ref:
                                print(Ans['R2aju'])
                        except: 
                            pass

    def Selection(self):
        Rmax = 0
        for key in self.Respuestas:
            if self.Respuestas[key]['R2aju'] > Rmax:
                self.Ans = self.Respuestas[key]
                Rmax = self.Respuestas[key]['R2aju']