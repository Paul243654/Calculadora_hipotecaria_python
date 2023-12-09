import sqlite3
import pandas as pd
import numpy as np
import os, sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QComboBox, QPushButton,QListWidget, QFileDialog, QTableWidgetItem, QVBoxLayout, QGridLayout, QGraphicsView


class Consultas_tablas_historicos(QDialog):
    def __init__(self):
        super().__init__()
######## 1 / 2 #############################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_tablas.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_tablas.ui", self)
        self.most_ind()
        self.most_din()
        self.pushButton_1.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.export_excel_indice)
        self.pushButton_2.clicked.connect(self.export_excel_dinero)

    def conectarBase(self):
######## 2 / 2 ###################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #self.conexion = sqlite3.connect(nombre_conexion)
        self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        mi_cursor=self.conexion.cursor() 

    def desconectarBase(self):
        self.conexion.commit()
        self.conexion.close()

    def tabla_indices(self):   
        self.dfr_indices= pd.read_sql("SELECT * from Historico_Indices", self.conexion)
        lista_dfr=self.dfr_indices.to_numpy().tolist()               
        fila=0
        for registro in lista_dfr:
            columna=0
            self.tableWidget_indices.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(str(elemento))
                self.tableWidget_indices.setItem(fila, columna, celda)
                columna +=1
            fila +=1

    def tabla_interesLegal(self):   
        self.dfr_dinero= pd.read_sql("SELECT * from Interes_dinero", self.conexion)
        lista_dfr=self.dfr_dinero.to_numpy().tolist()               
        fila=0
        for registro in lista_dfr:
            columna=0
            self.tableWidget_2.insertRow(fila)
            for elemento in registro:
                celda=QTableWidgetItem(str(elemento))
                self.tableWidget_2.setItem(fila, columna, celda)
                columna +=1
            fila +=1

    def save(self):
        self.filenames = QFileDialog.getSaveFileName(self,'Exportando archivo .xlsx', '','*.xlsx')
        self.filename=self.filenames[0]

    def export_excel_indice(self):
        try:
            self.save()
            self.dfr_indices.to_excel(self.filename, index=False)
            QMessageBox.about(self, "INFORMACION", "Archivo Historial_indices.xlsx exportado correctamente")
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la exportación de datos")

    def export_excel_dinero(self):
        try:
            self.save()
            self.dfr_dinero.to_excel(self.filename, index=False)
            QMessageBox.about(self, "INFORMACION", "Archivo Historial_interesLegal.xlsx exportado correctamente")
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la exppotación de datos")

    def most_ind(self):
        try:
            self.conectarBase()
            self.tabla_indices()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la obtención del df índices")

    def most_din(self):
        try:
            self.conectarBase()
            self.tabla_interesLegal()
            self.desconectarBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la obtención del df interés legal")

########  /  ###################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    GUIa=Consultas_tablas_historicos()
    GUIa.show()
    sys.exit(app.exec_())