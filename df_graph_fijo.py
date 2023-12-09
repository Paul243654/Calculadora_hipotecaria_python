from fileinput import close
import sqlite3
from turtle import title
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import os, sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QComboBox, QPushButton,QListWidget, QTableView, QTableWidgetItem, QVBoxLayout, QGridLayout, QGraphicsView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Consultas_graficos_fijo(QDialog):
    def __init__(self):
        super().__init__()
######## 1 / 4 ############################################################################################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_datosgraficofijo.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_datosgraficofijo.ui", self)
######## 2 / 4 ###############################################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor()       
        dfr_comodin= pd.read_sql("SELECT TIPOPAGO from Comodin", conexion)
        dfw=dfr_comodin.to_numpy().tolist()
        self.TIPOPAGO=(dfw[0][0])
        conexion.commit()
        conexion.close()

        self.ej_tar()
        self.ej_tar_2()
        try:
            self.grafica = Canvas_grafica()
            self.verticalLayout_grafFijo.addWidget(self.grafica)
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la obtención del gráfico")

        self.pushButton_salirformdatosfijo.clicked.connect(self.close)
        self.pushButton_expexceldatfijo.clicked.connect(self.export_excel)
        
    def conectarBase(self):
######## 3 / 4 ############################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #self.conexion = sqlite3.connect(nombre_conexion)
        self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=self.conexion.cursor() 

    def desconectarBase(self):
        self.conexion.commit()
        self.conexion.close()

    def datosGral(self):
        
        self.dfr_solofijo= pd.read_sql("SELECT * from Datos_soloFijo", self.conexion)

        if self.TIPOPAGO == 'Solo fijo':
            self.dfr = self.dfr_solofijo
            lista_dfr=self.dfr.to_numpy().tolist()               
            fila=0
            for registro in lista_dfr:
                columna=0
                self.tableWidget_datosfijo.insertRow(fila)
                for elemento in registro:
                    celda=QTableWidgetItem(str(elemento))
                    self.tableWidget_datosfijo.setItem(fila, columna, celda)
                    columna +=1
                fila +=1

    def agrup_fijo(self):
        self.dfr_fijo=self.dfr[['NUMERO_REVISION', 'NUMERO_CUOTA', 'INTERES_MES', 'AMORTIZACION_MES']]
        self.grouped_dfr_fijo = self.dfr_fijo.groupby('NUMERO_REVISION').agg({'NUMERO_REVISION': 'count', 'INTERES_MES':'sum', 'AMORTIZACION_MES':'sum'})
        
        def operaciones3(fila3):
            resultado3=fila3['INTERES_MES']+fila3['AMORTIZACION_MES']
            return resultado3

        self.grouped_dfr_fijo['TOTAL_PAGADO']=self.grouped_dfr_fijo.apply(operaciones3, axis=1)
        self.AA=(self.grouped_dfr_fijo.iloc[0]['INTERES_MES'])
        self.BB=(self.grouped_dfr_fijo.iloc[0]['AMORTIZACION_MES'])
        self.CC=(self.grouped_dfr_fijo.iloc[0]['TOTAL_PAGADO'])
        self.CC=round(self.CC,2)
        self.AA=str(self.AA)
        self.BB=str(self.BB)
        self.CC=str(self.CC)

        lista_totfij=[self.AA, self.BB, self.CC]
        fila=0
        columna=0
        for elemento in lista_totfij: 
            celda=QTableWidgetItem(str(elemento))
            self.tableWidget_fijototales.setItem(fila, columna, celda)
            columna +=1 

    def save(self):
        self.filenames = QFileDialog.getSaveFileName(self,'Exportando archivo .xlsx', '','*.xlsx')
        self.filename=self.filenames[0]
    
    def export_excel(self):
        try:
            self.save()
            self.dfr.to_excel(self.filename, index=False)
            QMessageBox.about(self, "INFORMACION", "Archivo Historial_hipoteca_tipoFijo.xlsx exportado correctamente.")
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la exportación de datos")
    
    def ej_tar(self):
        try:
            self.conectarBase()
            self.datosGral()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la ejecución")

    def ej_tar_2(self):
        try:
            self.conectarBase()
            self.agrup_fijo()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la ejecución")

    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

class Canvas_grafica(FigureCanvas):
    def __init__(self):
######## 4 / 4 #######################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #conexion = sqlite3.connect(nombre_conexion)
        conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=conexion.cursor() 

        dfr_solofijo= pd.read_sql("SELECT * from Datos_soloFijo", conexion)
        dfr_fijo=dfr_solofijo[['INTERES_MES', 'AMORTIZACION_MES']]

        Total_interes = dfr_fijo['INTERES_MES'].sum()
        Total_amortizacion = dfr_fijo['AMORTIZACION_MES'].sum()
        
        self.fig, self.ax = plt.subplots(figsize =(10, 7))
        super().__init__(self.fig)  
        car_s = ['INTERESES', 'AMORTIZACION'] 
        data = [Total_interes, Total_amortizacion] 
        self.ax.pie(data, labels = car_s)
        
        conexion.commit()
        conexion.close()

######## / #######################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)
      

if __name__ == "__main__":
    app=QApplication(sys.argv)
    GUIa=Consultas_graficos_fijo()
    GUIa.show()
    sys.exit(app.exec_())


   

