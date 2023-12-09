import csv
import sqlite3
from datetime import date
from datetime import datetime
import os,sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QComboBox, QPushButton, QRadioButton, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from tablas_historico import Consultas_tablas_historicos
import webbrowser

class Importaciondatos(QDialog):

    def __init__(self):
        super().__init__()
######## 1 / 3 #############################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_ingresoDatos.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_ingresoDatos.ui", self)
       
        self.lista_lineEdit_1 = [self.lineEdit_modinsertent_2, self.lineEdit_modinsertbanc_2, self.lineEdit_modinsertcaja_2,
                            self.lineEdit_modinserteuribor_2, self.lineEdit_modinsertfijo_2, self.lineEdit_modinsertdiferen_2, 
                            self.lineEdit_modinsertotro_2]
        self.lista_lineEdit_2 = [self.lineEdit_intlegaldinero_4, self.lineEdit_intdemoradinero_4, self.lineEdit_fecinicialdinero_4,
                            self.lineEdit_fecfinaldinero_4, self.lineEdit_obsdinero_4]
        self.lista_lineEdit_3=[self.comboBox_4, self.comboBox_5, self.lineEdit_modinsertent,
                                self.lineEdit_modinsertbanc, self.lineEdit_modinsertcaja, self.lineEdit_modinserteuribor,
                                self.lineEdit_modinsertfijo, self.lineEdit_modinsertdiferen, self.lineEdit_modinsertotro]
        self.lista_lineEdit_4=[self.comboBox_6, self.lineEdit_intlegaldinero_3, self.lineEdit_intdemoradinero_3, 
                               self.lineEdit_fecinicialdinero_3, self.lineEdit_fecfinaldinero_3, self.lineEdit_obsdinero_3]

        self.lista_numero_agnos=[' ','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028']
        self.lista_meses_Anual= [' ',"Enero" ,"Febrero" ,"Marzo" ,"Abril" ,"Mayo" ,"Junio" ,"Julio" , "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]

        self.pushButton_delprograma.clicked.connect(self.close)
        self.pushButton_limpiardatosingres.clicked.connect(self.clear_campos)
        self.pushButton_ejecutardinero_2.clicked.connect(self.buscar_Registro_Indice)
        self.pushButton_ejecutardinero_4.clicked.connect(self.funcionActualizarRegistro)
        self.pushButton_ejecutardinero_6.clicked.connect(self.buscar_Registro_Dinero)
        self.pushButton_ejecutardinero_5.clicked.connect(self.funcionInsertarRegistro)
        self.pushButton_borrartablaeinsertar.clicked.connect(self.insertar_Tabla)
        self.pushButton_66.clicked.connect(self.open_tablas)
        self.pushButton_plantilla.clicked.connect(self.leer_plantilla)

        self.pushButton_ejecutardinero_2.setDisabled(True)
        self.pushButton_ejecutardinero_6.setDisabled(True)

        self.comboBox.addItems(self.lista_numero_agnos)
        self.comboBox_2.addItems(self.lista_meses_Anual)
        self.comboBox_3.addItems(self.lista_numero_agnos)
        self.comboBox_4.addItems(self.lista_numero_agnos)
        self.comboBox_5.addItems(self.lista_meses_Anual)
        self.comboBox_6.addItems(self.lista_numero_agnos)

        self.comboBox.setDisabled(True)
        self.comboBox_2.setDisabled(True)
        self.comboBox_3.setDisabled(True)

        for line in self.lista_lineEdit_1:
            line.setDisabled(True)

        for line in self.lista_lineEdit_2:
            line.setDisabled(True)

        self.rbtn1.toggled.connect(self.onClicked)
        self.rbtn2.toggled.connect(self.onClicked)
        self.rbtn3.toggled.connect(self.onClicked)
        self.rbtn4.toggled.connect(self.onClicked)
        self.rbtn5.toggled.connect(self.onClicked_2)
        self.rbtn6.toggled.connect(self.onClicked_2)

    def clearAll_lineEdit_combBox(self):
        for le in self.findChildren(QLineEdit):
            le.clear() 
        for le in self.findChildren(QComboBox):
            le.setCurrentIndex(0) 

    def leer_plantilla(self):
######## 2 / 3 ########################################################################################################################
        #nombre_pdf=self.resolver_ruta('GUIA DE IMPORTACION.pdf')
        #webbrowser.open_new(nombre_pdf)
        webbrowser.open_new('C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/GUIA DE IMPORTACION.pdf')

    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.textoRbtn=radioBtn.text()

            if self.textoRbtn == 'Indice mensual':
                self.comboBox.setDisabled(True)
                self.comboBox_2.setDisabled(True)
                self.comboBox_3.setDisabled(True)
                self.comboBox_4.setDisabled(False) 
                self.comboBox_5.setDisabled(False)
                self.comboBox_6.setDisabled(True)
                self.clearAll_lineEdit_combBox() 
                self.pushButton_ejecutardinero_2.setDisabled(True)
                self.pushButton_ejecutardinero_6.setDisabled(True)
            elif self.textoRbtn =='Int. legal anual':
                self.comboBox.setDisabled(True)
                self.comboBox_2.setDisabled(True)
                self.comboBox_3.setDisabled(True)
                self.comboBox_4.setDisabled(True) 
                self.comboBox_5.setDisabled(True)
                self.comboBox_6.setDisabled(False)
                self.clearAll_lineEdit_combBox()
                self.pushButton_ejecutardinero_2.setDisabled(True)
                self.pushButton_ejecutardinero_6.setDisabled(True)
            elif self.textoRbtn =='Histórico indices':
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)
                self.clearAll_lineEdit_combBox()
                self.comboBox_3.setDisabled(True)
                self.comboBox_4.setDisabled(True) 
                self.comboBox_5.setDisabled(True)
                self.pushButton_ejecutardinero_2.setDisabled(False)
                self.pushButton_ejecutardinero_6.setDisabled(True)
            elif self.textoRbtn =='Histórico Int. legal':
                self.comboBox.setDisabled(True)
                self.comboBox_2.setDisabled(True)
                self.comboBox_3.setDisabled(False)
                self.comboBox_4.setDisabled(True) 
                self.comboBox_5.setDisabled(True)
                self.clearAll_lineEdit_combBox()
                self.pushButton_ejecutardinero_2.setDisabled(True)
                self.pushButton_ejecutardinero_6.setDisabled(False)

    def onClicked_2(self):
        radioBtn_2 = self.sender()
        if radioBtn_2.isChecked():
            self.textoRbtn_2=radioBtn_2.text()

    def clear_campos(self):
        for l in self.findChildren(QLineEdit):
            l.clear() 

    def conecBase(self):
######## 3 / 3 ####################################################################################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #self.conexion = sqlite3.connect(nombre_conexion)
        self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        self.mi_cursor=self.conexion.cursor()  

    def desconecBase(self):
        self.conexion.commit()
        self.conexion.close()

    def crea_table(self, nombre_tabla):
        try:
            self.conexion.execute(nombre_tabla)
        except sqlite3.OperationalError:
            QMessageBox.about(self, "Información", "La tabla ya existe")

    def eliminar_table(self):
        
        sql_1="DROP TABLE Datos_soloFijo"
        sql_2="DROP TABLE Historico_Indices"
        sql_3="DROP TABLE Interes_dinero"
        sql_4="DROP TABLE Datos_temporales_anual"
        sql_5="DROP TABLE Datos_temporales_bianual"
        self.conexion.execute(sql_5)


    def borrar_datostabla_historicoindices(self):
        sql_1= "DELETE FROM Historico_Indices;"
        self.mi_cursor.execute(sql_1)

    def borrar_datostabla_interesdinero(self):
        sql_2= "DELETE FROM Interes_dinero;"
        self.mi_cursor.execute(sql_2)

    def extrae_inserta_datos(self, archivo, insertar):
        lista_indice=[]
        with open (archivo, 'r') as w:
            reader=csv.reader(w, delimiter=";")
            for row in reader:
                lista_indice.append(row)
        conteo=len(lista_indice)

        for i in range (1,conteo):
            a=(lista_indice[i][0]).replace (",", ".")
            b=(lista_indice[i][1]).replace (",", ".")
            c=(lista_indice[i][2]).replace (",", ".")
            d=(lista_indice[i][3]).replace (",", ".")
            e=(lista_indice[i][4]).replace (",", ".")
            f=(lista_indice[i][5]).replace (",", ".")
            g=(lista_indice[i][6]).replace (",", ".")
            h=(lista_indice[i][7]).replace (",", ".")
            j=(lista_indice[i][8]).replace (",", ".")
        
            self.conexion.execute(insertar, (a, b, c, d, e, f, g, h, j))

    def extrae_inserta_datosdinero(self, archivo, insertar):
        lista_indice=[]
        with open (archivo, 'r') as w:
            reader=csv.reader(w, delimiter=";")
            for row in reader:
                lista_indice.append(row)
        conteo=len(lista_indice)

        for i in range (1,conteo):
            a=(lista_indice[i][0]).replace (",", ".")
            b=(lista_indice[i][1]).replace (",", ".")
            c=(lista_indice[i][2]).replace (",", ".")
            d=(lista_indice[i][3]).replace (",", ".")
            e=(lista_indice[i][4]).replace (",", ".")
            f=(lista_indice[i][5]).replace (",", ".")
        
            self.conexion.execute(insertar, (a, b, c, d, e, f))

    def buscarfila(self, agno, mes):
        if agno != '' and mes != '':
            sql=("SELECT AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL,OTRO FROM Historico_Indices WHERE AGNO= ? AND MES= ?")
            self.mi_cursor.execute(sql, (agno,mes,))
            registros=self.mi_cursor.fetchall()
            self.contador=0
            self.Dan0=[]
            for i in registros:
                self.Dan0.append(i)
                self.contador=self.contador+1


    def buscarfiladinero(self, agno_int):
        if agno_int != '':
            sql=("SELECT AGNO_INT, INT_LEGAL, INT_DEMORA, FECHA_INICIO, FECHA_FINAL, OBS FROM Interes_dinero WHERE AGNO_INT= ?")
            self.mi_cursor.execute(sql, (agno_int,))
            registros= self.mi_cursor.fetchall()
            self.contador2=0
            self.Dan01=[]
            for z in registros:
                self.Dan01.append(z)
                self.contador2=self.contador2+1 

    def insertarfila(self, agno, mes, entidades, bancos, cajas, euribor, fijo, diferencial, otro):
        sql=("INSERT INTO Historico_Indices (AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO) VALUES (?,?,?,?,?,?,?,?,?)")
        self.conexion.execute(sql, (agno, mes, entidades, bancos, cajas, euribor, fijo, diferencial, otro,))

    def insertarfiladinero(self, agno, intlegal, intdemora, fechainicio, fechafinal, observacion):
        sql=("INSERT INTO Interes_dinero (AGNO_INT, INT_LEGAL, INT_DEMORA, FECHA_INICIO, FECHA_FINAL, OBS) VALUES (?,?,?,?,?,?)")
        self.conexion.execute(sql, (agno, intlegal, intdemora, fechainicio, fechafinal, observacion,))

    def modificarfila(self, entidades, bancos, cajas, euribor, fijo, diferencial, otro, agno, mes):
        sql=("UPDATE Historico_Indices SET ENTIDADES = ?, BANCOS = ?, CAJAS = ?, EURIBOR = ?, FIJO=?, DIFERENCIAL=?, OTRO=? WHERE AGNO= ? AND MES= ?")
        self.mi_cursor.execute(sql, (entidades, bancos, cajas, euribor, fijo, diferencial, otro, agno, mes))

    def modificarfiladinero(self,intlegal, intdemora, fechainicio, fechafinal, observacion, agno):
        sql=("UPDATE Interes_dinero SET INT_LEGAL = ?, INT_DEMORA = ?, FECHA_INICIO = ?, FECHA_FINAL=?, OBS=? WHERE AGNO_INT= ?")
        self.mi_cursor.execute(sql, (intlegal, intdemora, fechainicio, fechafinal, observacion, agno))

    def buscar_Registro_Indice(self):
        try:
            self.conecBase()
            Ragno=self.comboBox.currentText()
            Rmes=self.comboBox_2.currentText()
            self.buscarfila(Ragno, Rmes)
            self.comboBox.setDisabled(True)
            self.comboBox_2.setDisabled(True)
            for line in self.lista_lineEdit_1:
                line.setDisabled(False)
            conteo=2
            for j in self.lista_lineEdit_1:
                j.setText(str(self.Dan0[0][conteo]))
                conteo+=1
            self.desconecBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Datos ingresados incorrectos")

    
    def buscar_Registro_Dinero(self):  
        try:
            self.conecBase()
            RagnoDin=self.comboBox_3.currentText()
            self.buscarfiladinero(RagnoDin)
            self.comboBox_3.setDisabled(True)

            for line in self.lista_lineEdit_2:
                line.setDisabled(False)

            self.lineEdit_intlegaldinero_4.setText(str(self.Dan01[0][1]))
            self.lineEdit_intdemoradinero_4.setText(str(self.Dan01[0][2]))
            self.lineEdit_fecinicialdinero_4.setText(str(self.Dan01[0][3]))
            self.lineEdit_fecfinaldinero_4.setText(str(self.Dan01[0][4]))
            self.lineEdit_obsdinero_4.setText(str(self.Dan01[0][5]))
            self.desconecBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Datos ingresados incorrectos")

    def funcionActualizarRegistro(self):
        try:
            if self.rbtn3.isChecked():
                C=self.lineEdit_modinsertent_2.text()
                D=self.lineEdit_modinsertbanc_2.text()
                E=self.lineEdit_modinsertcaja_2.text()
                F=self.lineEdit_modinserteuribor_2.text()
                G=self.lineEdit_modinsertfijo_2.text()
                H=self.lineEdit_modinsertdiferen_2.text()
                I=self.lineEdit_modinsertotro_2.text()
                A=self.comboBox.currentText()
                B=self.comboBox_2.currentText()
                self.conecBase()
                self.modificarfila(C,D,E,F,G,H,I,A,B)
                self.clearAll_lineEdit_combBox()
                self.comboBox.setDisabled(False)
                self.comboBox_2.setDisabled(False)
                for line in self.lista_lineEdit_1:
                    line.setDisabled(True)
                self.desconecBase()

            if self.rbtn4.isChecked():
                self.conecBase()
                L=self.lineEdit_intlegaldinero_4.text()
                M=self.lineEdit_intdemoradinero_4.text()
                N=self.lineEdit_fecinicialdinero_4.text()
                O=self.lineEdit_fecfinaldinero_4.text()
                P=self.lineEdit_obsdinero_4.text()
                K=self.comboBox_3.currentText()  
                self.modificarfiladinero(L,M,N,O,P,K)
                self.clearAll_lineEdit_combBox()
                self.comboBox_3.setDisabled(False)
                for line in self.lista_lineEdit_2:
                    line.setDisabled(True)
                self.desconecBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Datos ingresados incorrectos")


    def funcionInsertarRegistro(self):
        try:
            if self.rbtn1.isChecked():
                self.conecBase()
                self.comboBox_4.setDisabled(False) 
                self.comboBox_5.setDisabled(False)    
                for line in self.lista_lineEdit_1:
                    line.setDisabled(True)
                for line in self.lista_lineEdit_2:
                    line.setDisabled(True)
                AA=self.comboBox_4.currentText()
                BB=self.comboBox_5.currentText()
                self.buscarfila(AA, BB)
                print(self.contador)
                if self.contador==0:
                    self.insertarfila(self.lista_lineEdit_3[0].currentText(), self.lista_lineEdit_3[1].currentText(), self.lista_lineEdit_3[2].text(),
                                    self.lista_lineEdit_3[3].text(), self.lista_lineEdit_3[4].text(), self.lista_lineEdit_3[5].text(), 
                                    self.lista_lineEdit_3[6].text(), self.lista_lineEdit_3[7].text(),self.lista_lineEdit_3[8].text())
                else:
                    QMessageBox.about(self, "Información", "El registro con ese año y mes ya existe!!!")
                self.clearAll_lineEdit_combBox()
                self.desconecBase()

            if self.rbtn2.isChecked():
                self.conecBase()
                self.comboBox_6.setDisabled(False)
                for line in self.lista_lineEdit_1:
                    line.setDisabled(True)
                for line in self.lista_lineEdit_2:
                    line.setDisabled(True)
                AAA=self.comboBox_6.currentText()
                self.buscarfiladinero(AAA)
                if self.contador2==0:
                    self.insertarfiladinero(self.lista_lineEdit_4[0].currentText(), self.lista_lineEdit_4[1].Text(), self.lista_lineEdit_4[2].Text(),
                                            self.lista_lineEdit_4[3].Text(), self.lista_lineEdit_4[4].Text(), self.lista_lineEdit_4[5].Text() )
                else:
                    QMessageBox.about(self, "Información", "El registro con ese año ya existe!!!")
                self.clearAll_lineEdit_combBox()
                self.desconecBase()
        except:
            QMessageBox.about(self, "INFORMACION", "Datos ingresados incorrectos")

    def insertar_Tabla(self):
        try:
            if self.rbtn5.isChecked():
                self.borrar_datostabla_historicoindices()
                self.extrae_inserta_datos('historico_indices.csv', "INSERT INTO Historico_Indices(AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO) VALUES (?,?,?,?,?,?,?,?,?)")
                
            if self.rbtn6.isChecked():
                self.borrar_datostabla_interesdinero()
                self.extrae_inserta_datosdinero('interes_dinero.csv', "INSERT INTO Interes_dinero(AGNO_INT, INT_LEGAL, INT_DEMORA, FECHA_INICIO, FECHA_FINAL, OBS) VALUES (?,?,?,?,?,?)")
        except:
            QMessageBox.about(self, "INFORMACION","Formato incorrecto de la tabla")

    def open_tablas(self):
        try:
            self.ventana_calculadora=Consultas_tablas_historicos()
            self.ventana_calculadora.exec_()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la importación del df")
######## / ####################################################################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    Fre=Importaciondatos()
    Fre.show()
    sys.exit(app.exec_())


#llamada.crea_table(""" CREATE TABLE Historico_Indices (AGNO INTEGER, MES VARCHAR(50), ENTIDADES DOUBLE, BANCOS DOUBLE, CAJAS DOUBLE, EURIBOR DOUBLE, FIJO DOUBLE, DIFERENCIAL DOUBLE, OTRO DOUBLE)""")
#llamada.crea_table(""" CREATE TABLE Interes_dinero (AGNO_INT INTEGER, INT_LEGAL DOUBLE, INT_DEMORA DOUBLE, FECHA_INICIO DATE, FECHA_FINAL DATE, OBS VARCHAR(60))""")
#llamada.eliminar_table()
#llamada.buscarfila(2021,'Abril')
#llamada.buscarfiladinero(2009)
#llamada.insertarfila(2022, 'Agosto', 9.999, ' ', '', 6.666, ' ', ' ',' ')
#llamada.insertarfiladinero(2025, 3.23, 3.24, date(2025,1,1), date(2025,12,31), 'Sin observaciones')


#llamada.borrar_datostabla_historicoindices()
#llamada.borrar_datostabla_interesdinero()
#llamada.extrae_inserta_datos('historico_indices.csv', "INSERT INTO Historico_Indices(AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO) VALUES (?,?,?,?,?,?,?,?,?)")
#llamada.extrae_inserta_datosdinero('interes_dinero.csv', "INSERT INTO Interes_dinero(AGNO_INT, INT_LEGAL, INT_DEMORA, FECHA_INICIO, FECHA_FINAL, OBS) VALUES (?,?,?,?,?,?)")

#llamada.modificarfila(5.02, ' ', ' ', 5.02, ' ', ' ', ' ', 2022, 'Enero')
#llamada.buscar_insertar_registro(2022, 'Abril', 3.333, ' ', ' ', 3.333, ' ', ' ', ' ')

#llamada.modificarfiladinero(3.33, 3.33, date(2025,1,1), date(2025,12,31), 'con observaciones', 2025)
#llamada.buscar_insertar_registrodinero(2022, 3.333, 2.222, date(2025,1,1), date(2025,12,31), 'Sin alguna observación')




