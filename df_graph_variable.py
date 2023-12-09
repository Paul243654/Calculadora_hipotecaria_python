from cProfile import label
import sqlite3
from datetime import date
from datetime import datetime
from datetime import timedelta
from IPython.display import display
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
import os, sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QComboBox, QPushButton,QListWidget, QTableView, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Consultas_graficos(QDialog):

    def __init__(self):
        super().__init__()
######## 1 / 6 #############################################################################################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_datosgraficovariable.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_datosgraficovariable.ui", self)
######## 2 / 6 ################################################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor()

        dfr_comodin= pd.read_sql("SELECT TIPOPAGO from Comodin", conexion)
        dfw=dfr_comodin.to_numpy().tolist()
        self.TIPOPAGO=(dfw[0][0])

        conexion.commit()
        conexion.close()

        self.ej_tarV()
        self.ej_tarV_2()
        self.ej_tarV_3()

        try:
            self.grafica1 = Canvas_grafica1()
            self.grafica2 = Canvas_grafica2()
            self.grafica3 = Canvas_grafica3()
            self.verticalLayout_totales.addWidget(self.grafica1)
            self.verticalLayout_grafevolind.addWidget(self.grafica2)
            self.verticalLayout_grafagruprev.addWidget(self.grafica3)
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la obtención del gráfico")

        self.pushButton_salirdatosgraf.clicked.connect(self.close)
        self.pushButton_exportarexcel.clicked.connect(self.export_excel)

    def conectarBase(self):
######## 3 / 6 ###############################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #self.conexion = sqlite3.connect(nombre_conexion)
        self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=self.conexion.cursor() 

    def desconectarBase(self):
        self.conexion.commit()
        self.conexion.close()

    def datosGral(self):
        
        self.dfr_anual= pd.read_sql("SELECT * from Datos_temporales_anual", self.conexion)
        self.dfr_bianual= pd.read_sql("SELECT * from Datos_temporales_bianual", self.conexion)

        if self.TIPOPAGO == 'Variable anual' or self.TIPOPAGO == 'Variable anual con fijo':
            self.dfr = self.dfr_anual
            lista_dfr=self.dfr.to_numpy().tolist()               
            fila=0
            for registro in lista_dfr:
                columna=0
                self.tableWidget_detVariable.insertRow(fila)
                for elemento in registro:
                    celda=QTableWidgetItem(str(elemento))
                    self.tableWidget_detVariable.setItem(fila, columna, celda)
                    columna +=1
                fila +=1

        elif self.TIPOPAGO == 'Variable semestral' or self.TIPOPAGO == 'Variable semestral con fijo':
            self.dfr = self.dfr_bianual 
            lista_dfr=self.dfr.to_numpy().tolist()               
            fila=0
            for registro in lista_dfr:
                columna=0
                self.tableWidget_detVariable.insertRow(fila)
                for elemento in registro:
                    celda=QTableWidgetItem(str(elemento))
                    self.tableWidget_detVariable.setItem(fila, columna, celda)
                    columna +=1
                fila +=1

    def evol_ind(self):       
        self.dfr1=self.dfr[['AGNO','MES_REVISION', 'VALOR_INDICE', 'VALOR_INDICE2']]
        self.dfr2=self.dfr1[self.dfr1['MES_REVISION'] != ""]

    def agrup_revision(self):
        self.dfr_a=self.dfr[['NUMERO_REVISION', 'INTERES_MES', 'INTERES_MES2', 'AMORTIZACION_MES', 'AMORTIZACION_MES2', 'VALOR_INDICE', 'VALOR_INDICE2'
                                    ]]
        self.grouped_dfr_b = self.dfr_a.groupby('NUMERO_REVISION').agg({'INTERES_MES':'sum', 'INTERES_MES2':'sum', 'AMORTIZACION_MES':'sum',
                                        'AMORTIZACION_MES2':'sum', 'VALOR_INDICE': 'mean', 'VALOR_INDICE2':'mean'})
        
        lista_dfr_group=self.grouped_dfr_b.to_numpy().tolist()               
        fila=0
        for registro in lista_dfr_group:
            columna=0
            self.tableWidget_3.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(str(elemento))
                self.tableWidget_3.setItem(fila, columna, celda)
                columna +=1
            fila +=1

    def totales_hip(self):

        self.dfr_t=self.dfr[['NUMERO_REVISION', 'INTERES_MES', 'INTERES_MES2', 'AMORTIZACION_MES', 'AMORTIZACION_MES2']]
        def operaciones1(fila1):
            resultado1=fila1['INTERES_MES']-fila1['INTERES_MES2']
            return resultado1
        self.dfr_t['DIFERENCIA_INTERESES']=self.dfr_t.apply(operaciones1, axis=1) 

        self.dfr_tt=self.dfr_t[['NUMERO_REVISION', 'INTERES_MES', 'INTERES_MES2', 'AMORTIZACION_MES', 'AMORTIZACION_MES2', 'DIFERENCIA_INTERESES']]
        def operaciones2(fila2):
            resultado2=fila2['AMORTIZACION_MES2']-fila2['AMORTIZACION_MES']
            return resultado2    
        self.dfr_tt['DIFERENCIA_AMORTIZACION']=self.dfr_tt.apply(operaciones2, axis=1)
        
        self.lista_totales=[]
        cols_asumar=['INTERES_MES', 'INTERES_MES2', 'AMORTIZACION_MES', 'AMORTIZACION_MES2', 'DIFERENCIA_INTERESES', 'DIFERENCIA_AMORTIZACION']
        cuenta_rev=self.dfr_tt["NUMERO_REVISION"].count()
        self.lista_totales.append(cuenta_rev)
        totales=self.dfr_tt[cols_asumar].sum()
        for j in totales:
            self.lista_totales.append(j)
        
        lista_totvariable_st=totales.to_numpy().tolist()
        lista_totvariable=[]
        for n in lista_totvariable_st:
            fg=round(n,2)
            lista_totvariable.append(fg)

        fila=0
        columna=0
        self.tableWidget_2.insertRow(fila)
        for elemento in lista_totvariable: 
            celda=QTableWidgetItem(str(elemento))
            self.tableWidget_2.setItem(fila, columna, celda)
            columna +=1

    def save(self):
        self.filenames = QFileDialog.getSaveFileName(self,'Exportando archivo .xlsx', '','*.xlsx')
        self.filename=self.filenames[0]

    def export_excel(self):
        try:
            self.save()
            self.dfr.to_excel(self.filename, index=False)
            QMessageBox.about(self, "INFORMACION", "Archivo Historial_hipoteca_tipoVariable.xlsx exportado correctamente")
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la exportación de datos")

    def ej_tarV(self):
        try:
            self.conectarBase()
            self.datosGral()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la ejecución")

    def ej_tarV_2(self):
        try:
            self.conectarBase()
            self.agrup_revision()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la ejecución")

    def ej_tarV_3(self):
        try:
            self.conectarBase()
            self.totales_hip()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la ejecución")
######## / ############################################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

class Canvas_grafica1(FigureCanvas):
    def __init__(self):
######## 4 / 6 ###########################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor()

        dfr_comodin= pd.read_sql("SELECT TIPOPAGO from Comodin", conexion)
        dfw=dfr_comodin.to_numpy().tolist()
        TIPOPAGO=(dfw[0][0])

        cor_anual= pd.read_sql("SELECT * from Datos_temporales_anual", conexion)
        cor_bianual=pd.read_sql("SELECT * from Datos_temporales_bianual", conexion)

        if TIPOPAGO == 'Variable anual' or TIPOPAGO == 'Variable anual con fijo':
            dfr = cor_anual
        elif TIPOPAGO == 'Variable semestral' or TIPOPAGO == 'Variable semestral con fijo':
            dfr = cor_bianual 
           
        dfr_filt=dfr[['INTERES_MES', 'AMORTIZACION_MES']]

        Total_interes = dfr_filt['INTERES_MES'].sum()
        Total_amortizacion = dfr_filt['AMORTIZACION_MES'].sum()
        
        self.fig, self.ax = plt.subplots(figsize =(10, 7))
        super().__init__(self.fig)  
        car_s = ['INTERESES', 'AMORTIZACION'] 
        data = [Total_interes, Total_amortizacion] 
        self.ax.pie(data, labels = car_s)

        conexion.commit()
        conexion.close()
######## / ###################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

class Canvas_grafica2(FigureCanvas):
    def __init__(self): 
######## 5 / 6 ###################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor()

        dfr_comodin= pd.read_sql("SELECT TIPOPAGO from Comodin", conexion)
        dfw=dfr_comodin.to_numpy().tolist()
        TIPOPAGO=(dfw[0][0])

        cor_anual= pd.read_sql("SELECT * from Datos_temporales_anual", conexion)
        cor_bianual=pd.read_sql("SELECT * from Datos_temporales_bianual", conexion)

        if TIPOPAGO == 'Variable anual' or TIPOPAGO == 'Variable anual con fijo':
            dfr = cor_anual
        elif TIPOPAGO == 'Variable semestral' or TIPOPAGO == 'Variable semestral con fijo':
            dfr = cor_bianual 

        dfr1=dfr[['AGNO','MES_REVISION', 'VALOR_INDICE', 'VALOR_INDICE2']]
        dfr2=dfr1[dfr1['MES_REVISION'] != ""]

        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        x = np.array(dfr2['AGNO'])
        y1 = np.array(dfr2['VALOR_INDICE'])
        y2= np.array(dfr2['VALOR_INDICE2'])  
        plt.plot(y1)
        plt.plot(y2)
    
        conexion.commit()
        conexion.close()
######## /###################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

class Canvas_grafica3(FigureCanvas):
    def __init__(self): 
######## 6 / 6 ######################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor()

        dfr_comodin= pd.read_sql("SELECT TIPOPAGO from Comodin", conexion)
        dfw=dfr_comodin.to_numpy().tolist()
        TIPOPAGO=(dfw[0][0])

        cor_anual= pd.read_sql("SELECT * from Datos_temporales_anual", conexion)
        cor_bianual=pd.read_sql("SELECT * from Datos_temporales_bianual", conexion)

        if TIPOPAGO == 'Variable anual' or TIPOPAGO == 'Variable anual con fijo':
            dfr = cor_anual
        elif TIPOPAGO == 'Variable semestral' or TIPOPAGO == 'Variable semestral con fijo':
            dfr = cor_bianual 

        dfr_a=dfr[['NUMERO_REVISION', 'INTERES_MES', 'INTERES_MES2', 'AMORTIZACION_MES', 'AMORTIZACION_MES2', 'VALOR_INDICE', 'VALOR_INDICE2'
                                    ]]
        grouped_dfr_b = dfr_a.groupby('NUMERO_REVISION').agg({'NUMERO_REVISION': 'mean','INTERES_MES':'sum', 'INTERES_MES2':'sum', 'AMORTIZACION_MES':'sum',
                                        'AMORTIZACION_MES2':'sum', 'VALOR_INDICE': 'mean', 'VALOR_INDICE2':'mean'})
        
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        comodin=grouped_dfr_b.shape[0]

        x = np.arange(comodin) 
        y1 = grouped_dfr_b['INTERES_MES']
        y2 = grouped_dfr_b['INTERES_MES2']
        width = 0.40
        
        self.ax.bar(x-0.2, y1, width) 
        self.ax.bar(x+0.2, y2, width) 

        conexion.commit()
        conexion.close()

######## /######################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    GUIa=Consultas_graficos()
    GUIa.show()
    sys.exit(app.exec_())

