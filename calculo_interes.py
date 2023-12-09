import sqlite3
from datetime import date
from datetime import datetime
from datetime import timedelta
import os, sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QIntValidator,QDoubleValidator
from PyQt5.QtWidgets import QMessageBox
from df_graph_fijo import Consultas_graficos_fijo
from df_graph_variable import Consultas_graficos
import pandas as pd
import numpy as np

lista_Tipo_pago=[' ','Solo fijo', 'Variable anual', 'Variable anual con fijo', 'Variable semestral', 'Variable semestral con fijo']
lista_numero_agnos=[' ','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028']
lista_meses_Anual= [' ',"Enero" ,"Febrero" ,"Marzo" ,"Abril" ,"Mayo" ,"Junio" ,"Julio" , "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]
lista_Tipos_indices=[' ','IRPH Entidades', 'IRPH Bancos', 'IRPH Cajas', 'Euribor', 'Fijo', 'Diferencial', 'Otro']
lista_plazos_fijoanual=['12','24','36','48','60']
lista_plazos_fijobianual=['6','12','18','24','30','36','42','48','54','60']
  
class ejemplo_GUI(QDialog):
    def __init__(self):

        self.lista_meses_anual= [
                        "Enero" ,"Febrero" ,"Marzo" ,"Abril" ,"Mayo" ,"Junio" ,"Julio" ,
                        "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"
                        ]
        self.diccionario_indices={'IRPH Entidades': 2, 'IRPH Bancos': 3, 'IRPH Cajas' : 4, 'Euribor' : 5, 'Fijo' : 6, 'Diferencial' : 7, 'Otro' : 8}
        self.diccionario_mesespago={
                                    "Enero": 1 ,"Febrero": 2 ,"Marzo": 3 ,"Abril": 4 ,"Mayo": 5 ,"Junio": 6 ,"Julio": 7,
                                    "Agosto": 8 ,"Septiembre": 9 ,"Octubre": 10 ,"Noviembre": 11 ,"Diciembre": 12
                                    }
        self.dic_lista_Tipo_pago={
                                    'Solo fijo':0, 'Variable anual':1, 'Variable anual con fijo':2, 'Variable semestral':3, 'Variable semestral con fijo':4
                                }

        super().__init__()
######## 1 / 7 ############################################################################################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_calculo.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_calculo.ui", self)      
        #datos generales
        self.comboBox_tipopago.addItems(lista_Tipo_pago)
        self.comboBox_agnofirma.addItems(lista_numero_agnos)
        self.comboBox_agnocurso.addItems(lista_numero_agnos)
        self.spinBox_diapago.setRange(1, 31)
        
        #solo fijo
        self.comboBox_mespagofijo1.addItems(lista_meses_Anual)
        #variable anual
        self.comboBox_indiceapli2.addItems(lista_Tipos_indices)
        self.comboBox_indicecomp2.addItems(lista_Tipos_indices)
        self.comboBox_mesrevisionanual2.addItems(lista_meses_Anual)
        self.comboBox_primermespagoanual2.addItems(lista_meses_Anual)
        # fijo + variable anual
        self.comboBox_mespagofijo3.addItems(lista_meses_Anual)
        self.comboBox_indiceapli3.addItems(lista_Tipos_indices)
        self.comboBox_indicecomp3.addItems(lista_Tipos_indices)
        self.comboBox_mesrevisionanual3.addItems(lista_meses_Anual)
        self.comboBox_primermespagoanual3.addItems(lista_meses_Anual)
        # variable semestral
        self.comboBox_indiceapli4.addItems(lista_Tipos_indices)
        self.comboBox_indicecomp4.addItems(lista_Tipos_indices)
        self.comboBox_mesrevisionsemestral4.addItems(lista_meses_Anual)
        self.comboBox_primermespagosemestral4.addItems(lista_meses_Anual)
        # fijo + variable semestral
        self.comboBox_mespagofijo5.addItems(lista_meses_Anual)
        self.comboBox_indiceapli5.addItems(lista_Tipos_indices)
        self.comboBox_indicecomp5.addItems(lista_Tipos_indices)
        self.comboBox_mesrevisionsemestral5.addItems(lista_meses_Anual)
        # boton
        self.pushButton_ejecutarcalculo.clicked.connect(self.ejecutar_datosGenerales)
        self.fecha_pago_cuota=datetime.now()
        self.fecha_pago_cancelacion = datetime(2024, 2, 10, 10, 15, 00, 00000) 
        self.pushButton_salircalculo.clicked.connect(self.close)      
        self.pushButton_limpiarcampos.clicked.connect(self.clearAll_lineEdit) 
        # line edit
        self.lineEdit_capitalinicial.setValidator(QIntValidator())
        self.lineEdit_plazostotales.setValidator(QIntValidator())
        self.lineEdit_interesfijoapli1.setValidator(QDoubleValidator())
        self.lineEdit_dif12.setValidator(QDoubleValidator())
        self.lineEdit_dif22.setValidator(QDoubleValidator())
        self.lineEdit_sust12.setValidator(QDoubleValidator())
        self.lineEdit_sust22.setValidator(QDoubleValidator())
        self.lineEdit_nplazosfijo3.setValidator(QIntValidator())
        self.lineEdit_interesfijoapli3.setValidator(QDoubleValidator())
        self.lineEdit_dif13.setValidator(QDoubleValidator())
        self.lineEdit_dif23.setValidator(QDoubleValidator())
        self.lineEdit_sust13.setValidator(QDoubleValidator())
        self.lineEdit_sust23.setValidator(QDoubleValidator())
        self.lineEdit_dif14.setValidator(QDoubleValidator())
        self.lineEdit_dif24.setValidator(QDoubleValidator())
        self.lineEdit_sust14.setValidator(QDoubleValidator())
        self.lineEdit_sust24.setValidator(QDoubleValidator())
        self.lineEdit_nplazosfijo5.setValidator(QIntValidator())
        self.lineEdit_interesfijoapli5.setValidator(QDoubleValidator())
        self.lineEdit_dif15.setValidator(QDoubleValidator())
        self.lineEdit_dif25.setValidator(QDoubleValidator())
        self.lineEdit_sust15.setValidator(QDoubleValidator())
        self.lineEdit_sust25.setValidator(QDoubleValidator())

        for n in range (0,5):
            self.tabWidget_tipospago.setTabEnabled(n, False)
  

        self.comboBox_tipopago.activated.connect(self.do_select)

    def crea_table_temporal(self, tipopago):
        tabla_fijo = ("""CREATE TABLE Datos_soloFijo (NUMERO_REVISION INTEGER, AGNO INTEGER, MESCUOTA  VARCHAR(50),\
                                            NUMERO_CUOTA INTEGER, CUOTA_MES DOUBLE, INTERES_MES DOUBLE, AMORTIZACION_MES DOUBLE,\
                                            CAPITAL_PENDIENTE DOUBLE, VALOR_INDICE DOUBLE, FECHA_PAGO DATE)""")

        tabla_variable_anual = (""" CREATE TABLE Datos_temporales_anual (NUMERO_REVISION INTEGER, AGNO INTEGER, MESCUOTA  VARCHAR(50),\
                                            NUMERO_CUOTA INTEGER, CUOTA_MES DOUBLE, INTERES_MES DOUBLE, AMORTIZACION_MES DOUBLE,\
                                            CAPITAL_PENDIENTE DOUBLE, VALOR_INDICE DOUBLE, CUOTA_MES2 DOUBLE, \
                                           INTERES_MES2 DOUBLE, AMORTIZACION_MES2 DOUBLE,CAPITAL_PENDIENTE2 DOUBLE, VALOR_INDICE2 DOUBLE, AMORTIZAR DOUBLE, DEVOLVER DOUBLE, FECHA_PAGO DATE, ACUMU_CONINT DOUBLE, MES_REVISION VARCHAR(50))""")
        
        tabla_variable_semestral = (""" CREATE TABLE Datos_temporales_bianual (NUMERO_REVISION INTEGER, AGNO INTEGER, MESCUOTA  VARCHAR(50),\
                                            NUMERO_CUOTA INTEGER, CUOTA_MES DOUBLE, INTERES_MES DOUBLE, AMORTIZACION_MES DOUBLE,\
                                            CAPITAL_PENDIENTE DOUBLE, VALOR_INDICE DOUBLE, CUOTA_MES2 DOUBLE, \
                                            INTERES_MES2 DOUBLE, AMORTIZACION_MES2 DOUBLE,CAPITAL_PENDIENTE2 DOUBLE, VALOR_INDICE2 DOUBLE, AMORTIZAR DOUBLE, DEVOLVER DOUBLE, FECHA_PAGO DATE, ACUMU_CONINT DOUBLE, MES_REVISION VARCHAR(50))""")
        if tipopago == 'Solo fijo':
            nombre_tabla=tabla_fijo
        elif tipopago == 'Variable anual' or tipopago == 'Variable anual con fijo':
            nombre_tabla= tabla_variable_anual
        elif tipopago == 'Variable semestral' or tipopago == 'Variable semestral con fijo':
            nombre_tabla=tabla_variable_semestral 
        try:
            self.conexion.execute(nombre_tabla)
        except sqlite3.OperationalError:
            QMessageBox.about(self, "Información", "La tabla ya existe!!!")

    def eliminar_table(self):
        sql_1="DROP TABLE Interes_dinero"
        self.conexion.execute(sql_1)

    def clearAll_lineEdit(self):
        for le in self.findChildren(QLineEdit):
            le.clear() 
        for le in self.findChildren(QComboBox):
            le.setCurrentIndex(0) 

    def calculo_Solo_interesfijo(self, agnofirma, mes1_pagofijo, plazototal, plazo_fijo, capprestado, ifijo, Fecha_pagomes):
        try:
            numero_plazosTotal=plazototal
            numero_plazos_fijo=plazo_fijo
            capital_prestado=capprestado
            agno_cursofijo=agnofirma
            interes_fijo=ifijo
            i_fijo=interes_fijo/1200
            variante=self.lista_meses_anual.index(mes1_pagofijo)
            int_fijo=round(interes_fijo,3)

            for plazosFijo in range (0,numero_plazos_fijo):

                j_fijo=(1+i_fijo)**(-numero_plazosTotal)
                cuota_mes=round(((capital_prestado * i_fijo)/(1-j_fijo)),3)
                interes_mensual= round((capital_prestado * i_fijo),3)
                amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                nrevisionfijo=0
                numerocuotafijo=plazosFijo+1
                mes_cursofijo=self.lista_meses_anual[variante]
                variante=variante+1
                capital_prestado=round((capital_prestado-amortizacion_mensual),3)
                numero_plazosTotal=numero_plazosTotal-1
                
                messs=self.diccionario_mesespago[mes_cursofijo]
                fec_pag= str(Fecha_pagomes)+'-'+ str(messs) +'-'+str(agno_cursofijo)
                date_object=datetime.strptime(fec_pag, '%d-%m-%Y')
                
                sql_temporal_solofijo = ("INSERT INTO Datos_soloFijo (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,FECHA_PAGO)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?)")

                self.conexion.execute(sql_temporal_solofijo, ( nrevisionfijo, agno_cursofijo, mes_cursofijo, numerocuotafijo,
                                                    cuota_mes, interes_mensual, amortizacion_mensual, capital_prestado, int_fijo, date_object
                                                        ))     
                
                if variante > 11:
                    variante=0
                    agno_cursofijo=agno_cursofijo+1
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")

    def calculo_interesfijo(self, tip_hip, agnofirma, mes1_pagofijo, plazototal, plazofijo, capprestado, ifijo, Fecha_pagomes):
        try:
            numero_plazosTotal=plazototal
            numero_plazos_fijo=plazofijo
            capital_prestado=capprestado
            agno_cursofijo=agnofirma
            interes_fijo=ifijo
            i_fijo=interes_fijo/1200
            variante=self.lista_meses_anual.index(mes1_pagofijo)
            int_fijo=round(interes_fijo,3)
        
            for plazosFijo in range (0,numero_plazos_fijo):
                j_fijo=(1+i_fijo)**(-numero_plazosTotal)
                cuota_mes=round(((capital_prestado * i_fijo)/(1-j_fijo)),3)
                interes_mensual= round((capital_prestado * i_fijo),3)
                amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                nrevisionfijo=0
                numerocuotafijo=plazosFijo+1
                mes_cursofijo=self.lista_meses_anual[variante]
                variante=variante+1
                capital_prestado=round((capital_prestado-amortizacion_mensual),3)
                numero_plazosTotal=numero_plazosTotal-1
                aamortizar=round(0.000,3)
                aadevolver=round(0.000,3)
                acumuladoint=round(0.000,3)

                messs=self.diccionario_mesespago[mes_cursofijo]
                fec_pag= str(Fecha_pagomes)+'-'+ str(messs) +'-'+str(agno_cursofijo)
                date_object=datetime.strptime(fec_pag, '%d-%m-%Y')
                mes_revision=""
                
                sql_temporal_anual = ("INSERT INTO Datos_temporales_anual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
                sql_temporal_bianual = ("INSERT INTO Datos_temporales_bianual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

                if tip_hip == 'Variable anual con fijo':
                    sql_temporalfijo = sql_temporal_anual
                elif tip_hip == "Variable semestral con fijo":
                    sql_temporalfijo = sql_temporal_bianual

                self.conexion.execute(sql_temporalfijo, ( nrevisionfijo, agno_cursofijo, mes_cursofijo, numerocuotafijo,
                                                    cuota_mes, interes_mensual, amortizacion_mensual, capital_prestado, int_fijo,
                                                    cuota_mes, interes_mensual, amortizacion_mensual, capital_prestado, int_fijo,
                                                    aamortizar, aadevolver, date_object, acumuladoint, mes_revision
                                                ))     
                
                if variante > 11:
                    variante=0
                    agno_cursofijo=agno_cursofijo+1

            self.CAPITAL_PENDIENTE=capital_prestado
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")


    def buscar_rangoanual_sinfijo(self, tip_ind1, tip_ind2, agno_firma, agno_actual, mes, perpagomes, diferenciall1, diferenciall2, plazosvariable, prestTotal, sust1, sust2, Fecha_pagomes):
        try:            
            sql=("SELECT AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO FROM Historico_Indices WHERE AGNO BETWEEN ? AND ? AND MES= ?")
            self.mi_cursor.execute(sql, (agno_firma, agno_actual,mes))
            
            registros=self.mi_cursor.fetchall()
            lista_mesrevision_anual=[]
            for i in registros:
                lista_mesrevision_anual.append(i)
            contador_revisiones=len(lista_mesrevision_anual)

######## 2 / 7 ############################################################################################################################################
            # Conexion a tabla interes legal dinero
            #nombre_conexion_din=self.resolver_ruta("Base_datos_IH.db")
            #conexion_din = sqlite3.connect(nombre_conexion_din)
            conexion_din = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
            df_intl = pd.read_sql_query("SELECT * FROM Interes_dinero", conexion_din)
            df_ind_sust1 = pd.read_sql_query("SELECT * FROM Historico_Indices", conexion_din)
            conexion_din.close()
            lista_numpy=df_intl.to_numpy().tolist()
            tere=len(lista_numpy)

            tipo_indice1 = self.diccionario_indices[tip_ind1]
            tipo_indice2 = self.diccionario_indices[tip_ind2]

            capital_inicial=prestTotal
            
            capital_pendiente=capital_inicial
            capital_pendiente2=capital_inicial
            diferencial_aplicado1=diferenciall1
            diferencial_aplicado2=diferenciall2
            ejec1=round(float(sust1),3)
            ejec2=round(float(sust2),3)
            numero_plazos_fijoanual=plazosvariable
            mes_inicial=self.lista_meses_anual.index(perpagomes)
            
            agno_perpago=agno_firma
            caso_agnomas=self.lista_meses_anual.index(mes)
            if mes_inicial < caso_agnomas:
                agno_perpago=agno_perpago+1
                
            for m in range(0, contador_revisiones):      
                agno_curso=agno_perpago + m
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if lista_mesrevision_anual[m][tipo_indice1] == '':
                    Df_cons_ind=df_ind_sust1[(df_ind_sust1['AGNO']== agno_curso) & (df_ind_sust1['MES']==mes)]
                    lista_numpy_ind=Df_cons_ind.to_numpy().tolist()
                    if ejec1==16:
                        valor_indice=lista_numpy_ind[0][2]
                    elif ejec1==17:
                        valor_indice=lista_numpy_ind[0][5]
                    elif ejec1!=16 and ejec1!=17:
                        valor_indice=ejec1
                else:
                    valor_indice=round((lista_mesrevision_anual[m][tipo_indice1]),3)

                i_fijo_anual=(valor_indice+diferencial_aplicado1)
                j_fijo_anual=(1+(i_fijo_anual/1200))**(-numero_plazos_fijoanual)
                cuota_mes=round(((capital_pendiente * (i_fijo_anual/1200))/(1-j_fijo_anual)),3)
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el segundo índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if lista_mesrevision_anual[m][tipo_indice2] == '':
                    valor_indice2=ejec2
                else:
                    valor_indice2=round((lista_mesrevision_anual[m][tipo_indice2]),3)

                i_fijo_anual2=valor_indice2+diferencial_aplicado2
                j_fijo_anual2=(1+(i_fijo_anual2/1200))**(-numero_plazos_fijoanual)
                cuota_mes2=round(((capital_pendiente2 * (i_fijo_anual2/1200))/(1-j_fijo_anual2)),3)                
                
                for n in range (0,12): 
                    revisionnumero= m + 1
                    numerocuota = (m * 12) + (n + 1 )
                    mesCuota=self.lista_meses_anual[mes_inicial]
                    mes_inicial=mes_inicial+1

                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual= round((capital_pendiente * (i_fijo_anual/1200)),3)
                    amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                    capital_pendiente=round((capital_pendiente-amortizacion_mensual),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual2= round((capital_pendiente2 * (i_fijo_anual2/1200)),3)
                    amortizacion_mensual2=round((cuota_mes2-interes_mensual2),3)
                    capital_pendiente2=round((capital_pendiente2-amortizacion_mensual2 ),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx cálculo con la diferencia entre cuotas xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx             
                    a_devolver= round((cuota_mes - cuota_mes2),3)
                    cantidad_amortizar=round((amortizacion_mensual2-amortizacion_mensual),3)
                    numero_plazos_fijoanual=numero_plazos_fijoanual-1 

                    mes_revision=mes
                    if mes_revision == mesCuota:
                        mes_revision=mes
                    else:
                        mes_revision = ''

                    messs=self.diccionario_mesespago[mesCuota]
                    fec_pag= str(Fecha_pagomes)+'-'+ str(messs) +'-'+str(agno_curso)
                    date_object=datetime.strptime(fec_pag, '%d-%m-%Y')
                    
                    acumuladoint=0

                    for k in range (0,tere):
                        Ini=str(lista_numpy[k][3])
                        Fin=str(lista_numpy[k][4])
                        Leg_in=(lista_numpy[k][1])
                        date_inicio=datetime.strptime(Ini, '%d-%m-%Y')
                        date_final=datetime.strptime(Fin, '%d-%m-%Y')
                        int_agno_calc=0.000 

                        if date_object>date_final:
                            int_agno_calc=0.000
                        elif date_object > date_inicio and date_object < date_final:  
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_object).days))/(365*100)    
                        else:   
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_inicio).days))/(365*100)

                        acumuladoint=acumuladoint+int_agno_calc

                    acumuladoint=round(acumuladoint,3)

                    sql_temporal_anualsinfijo = ("INSERT INTO Datos_temporales_anual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

                    self.conexion.execute(sql_temporal_anualsinfijo, (revisionnumero,  agno_curso, mesCuota, numerocuota , 
                                                    cuota_mes, interes_mensual, amortizacion_mensual, 
                                                    capital_pendiente, valor_indice,
                                                    cuota_mes2, interes_mensual2, amortizacion_mensual2, 
                                                    capital_pendiente2, valor_indice2, cantidad_amortizar, a_devolver, date_object, acumuladoint, mes_revision
                                                    ))             
                    if mes_inicial > 11:
                        mes_inicial=0
                        agno_curso=agno_curso+1
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")

    def buscar_rangoanual_confijo(self, tip_ind1, tip_ind2, agno_firma, agno_actual, mes, perpagomes, diferenciall1,diferenciall2, plazosvariable, sust1, sust2, Fecha_pagomes):
        try:
            sql=("SELECT AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO FROM Historico_Indices WHERE AGNO BETWEEN ? AND ? AND MES= ?")
            self.mi_cursor.execute(sql, (agno_firma, agno_actual,mes))
                
            registros=self.mi_cursor.fetchall()
            lista_mesrevision_anual=[]
            for i in registros:
                lista_mesrevision_anual.append(i)

######## 3 / 7 ############################################################################################################################################
            # Conexion a tabla interes legal dinero
            #nombre_conexion_din=self.resolver_ruta("Base_datos_IH.db")
            #conexion_din = sqlite3.connect(nombre_conexion_din)
            conexion_din = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
            df_intl = pd.read_sql_query("SELECT * FROM Interes_dinero", conexion_din)
            df_ind_sust1 = pd.read_sql_query("SELECT * FROM Historico_Indices", conexion_din)
            conexion_din.close()
            lista_numpy=df_intl.to_numpy().tolist()
            tere=len(lista_numpy)

            contador_revisiones=len(lista_mesrevision_anual)

            tipo_indice1 = self.diccionario_indices[tip_ind1]
            tipo_indice2 = self.diccionario_indices[tip_ind2]

            capital_inicial=self.CAPITAL_PENDIENTE
            
            capital_pendiente=capital_inicial
            capital_pendiente2=capital_inicial
            diferencial_aplicado1=diferenciall1
            diferencial_aplicado2=diferenciall2
            ejec1=round(float(sust1),3)
            ejec2=round(float(sust2),3)
            numero_plazos_fijoanual=plazosvariable
            mes_inicial=self.lista_meses_anual.index(perpagomes)

            agno_perpago=agno_firma
            caso_agnomas=self.lista_meses_anual.index(mes)
            if mes_inicial < caso_agnomas:
                agno_perpago=agno_perpago+1
                
            for m in range(0, contador_revisiones):
                agno_curso=agno_perpago + m     
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if (lista_mesrevision_anual[m][tipo_indice1]) == '':
                    Df_cons_ind=df_ind_sust1[(df_ind_sust1['AGNO']== agno_curso) & (df_ind_sust1['MES']==mes)]
                    lista_numpy_ind=Df_cons_ind.to_numpy().tolist()
                    if ejec1==16:
                        valor_indice=lista_numpy_ind[0][2]
                    elif ejec1==17:
                        valor_indice=lista_numpy_ind[0][5]
                    elif ejec1!=16 and ejec1!=17:
                        valor_indice=ejec1
                else:
                    valor_indice=round((lista_mesrevision_anual[m][tipo_indice1]),3)
                    
                i_fijo_anual=(valor_indice+diferencial_aplicado1)
                j_fijo_anual=(1+(i_fijo_anual/1200))**(-numero_plazos_fijoanual)
                cuota_mes=round(((capital_pendiente * (i_fijo_anual/1200))/(1-j_fijo_anual)),3)
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el segundo índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if (lista_mesrevision_anual[m][tipo_indice2]) == '':
                    valor_indice2=ejec2
                else:
                    valor_indice2=round((lista_mesrevision_anual[m][tipo_indice2]),3)

                i_fijo_anual2=valor_indice2+diferencial_aplicado2
                j_fijo_anual2=(1+(i_fijo_anual2/1200))**(-numero_plazos_fijoanual)
                cuota_mes2=round(((capital_pendiente2 * (i_fijo_anual2/1200))/(1-j_fijo_anual2)),3)                
                
                for n in range (0,12): 
                    revisionnumero= m + 1
                    numerocuota = (m * 12) + (n + 1)
                    mesCuota=self.lista_meses_anual[mes_inicial]
                    mes_inicial=mes_inicial+1

                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual= round((capital_pendiente * (i_fijo_anual/1200)),3)
                    amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                    capital_pendiente=round((capital_pendiente-amortizacion_mensual),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual2= round((capital_pendiente2 * (i_fijo_anual2/1200)),3)
                    amortizacion_mensual2=round((cuota_mes2-interes_mensual2),3)
                    capital_pendiente2=round((capital_pendiente2-amortizacion_mensual2 ),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx cálculo con la diferencia entre cuotas xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx             
                    a_devolver= round((cuota_mes - cuota_mes2),3)
                    cantidad_amortizar=round((amortizacion_mensual2-amortizacion_mensual),3)

                    numero_plazos_fijoanual=numero_plazos_fijoanual-1  
                    mes_revision=mes
                    if mes_revision == mesCuota:
                        mes_revision=mesCuota
                    else:
                        mes_revision = ''

                    messs=self.diccionario_mesespago[mesCuota]
                    fe_par= str(Fecha_pagomes)+'-'+str(messs)+'-'+str(agno_curso) 
                    date_object=datetime.strptime(fe_par, "%d-%m-%Y")
                    
                    acumuladoint=0
                    
                    for k in range (0,tere):
                        Ini=str(lista_numpy[k][3])
                        Fin=str(lista_numpy[k][4])
                        Leg_in=(lista_numpy[k][1])
                        date_inicio=datetime.strptime(Ini, '%d-%m-%Y')
                        date_final=datetime.strptime(Fin, '%d-%m-%Y')
                        int_agno_calc=0.000 

                        if date_object>date_final:
                            int_agno_calc=0.000
                        elif date_object > date_inicio and date_object < date_final:  
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_object).days))/(365*100)    
                        else:   
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_inicio).days))/(365*100)

                        acumuladoint=acumuladoint+int_agno_calc

                    acumuladoint=round(acumuladoint,3)
                    sql_temporal_anualconfijo = ("INSERT INTO Datos_temporales_anual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

                    self.conexion.execute(sql_temporal_anualconfijo, (revisionnumero, agno_curso, mesCuota, numerocuota , 
                                                    cuota_mes, interes_mensual, amortizacion_mensual, 
                                                    capital_pendiente, valor_indice,
                                                    cuota_mes2, interes_mensual2, amortizacion_mensual2, 
                                                    capital_pendiente2, valor_indice2, cantidad_amortizar, a_devolver, date_object, acumuladoint, mes_revision
                                                    ))             
                    if mes_inicial > 11:
                        mes_inicial=0
                        agno_curso=agno_curso+1
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")

    def buscar_rangobianual_sinfijo(self, tip_ind1, tip_ind2, agno_firma, agno_actual, mes, perpagomes1, perpagomes2, diferenciall1, diferenciall2, plazosvariable, prestTotal, sust1, sust2, Fecha_pagomes):
        try:
            lista_meses_bianual= [
                        ["Enero" ,"Julio", agno_firma, agno_firma], ["Febrero" ,"Agosto", agno_firma, agno_firma], 
                        ["Marzo" ,"Septiembre", agno_firma, agno_firma], ["Abril" ,"Octubre", agno_firma, agno_firma], 
                        ["Mayo" ,"Noviembre", agno_firma, agno_firma], ["Junio" ,"Diciembre", agno_firma, agno_firma],
                        ["Julio" ,"Enero", agno_firma, agno_firma+1], ["Agosto" ,"Febrero", agno_firma, agno_firma+1], 
                        ["Septiembre" ,"Marzo", agno_firma, agno_firma+1], ["Octubre" ,"Abril", agno_firma, agno_firma+1], 
                        ["Noviembre" ,"Mayo", agno_firma, agno_firma+1], ["Diciembre" ,"Junio", agno_firma, agno_firma+1]              
                                    ]
            mes1_bi=mes
            for q in range (0,12):
                if lista_meses_bianual[q][0]==mes:
                    mes2_bi=lista_meses_bianual[q][1]
                
            for i in range (0,12):   
                comodin= lista_meses_bianual[i][0]
                if comodin == mes:
                    mes2=lista_meses_bianual[i][1]
                    agno2=lista_meses_bianual[i][3]

            sql=("SELECT AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO FROM Historico_Indices WHERE (AGNO BETWEEN ? AND ? AND MES= ?)\
                OR (AGNO BETWEEN ? AND ? AND MES= ?) ")
            self.mi_cursor.execute(sql, (agno_firma, agno_actual, mes, agno2, agno_actual, mes2))
            
            registros=self.mi_cursor.fetchall()
            lista_mesrevision_bianual=[]
            for i in registros:
                ii=list(i)
                if ii[1]== mes:
                    ii.append(perpagomes1)
                else:
                    ii.append(perpagomes2)
                lista_mesrevision_bianual.append(ii)

######## 4 / 7 ############################################################################################################################################
            # Conexion a tabla interes legal dinero
            #nombre_conexion_din=self.resolver_ruta("Base_datos_IH.db")
            #conexion_din = sqlite3.connect(nombre_conexion_din)
            conexion_din = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
            df_intl = pd.read_sql_query("SELECT * FROM Interes_dinero", conexion_din)
            df_ind_sust1 = pd.read_sql_query("SELECT * FROM Historico_Indices", conexion_din)
            conexion_din.close()
            lista_numpy=df_intl.to_numpy().tolist()
            tere=len(lista_numpy)
            
            contador_revisiones=len(lista_mesrevision_bianual)
            
            tipo_indice1 = self.diccionario_indices[tip_ind1]
            tipo_indice2 = self.diccionario_indices[tip_ind2]
            
            capital_inicial=prestTotal

            capital_pendiente=capital_inicial
            capital_pendiente2=capital_inicial
            diferencial_aplicado1=diferenciall1
            diferencial_aplicado2=diferenciall2
            ejec1=round(float(sust1),3)
            ejec2=round(float(sust2),3)
            numero_plazos_fijoanual=plazosvariable

            agno_curso=agno_firma
            agno_perpago=agno_firma
            ind_mespago1=self.lista_meses_anual.index(perpagomes1)

            ind_mesrev1=self.lista_meses_anual.index(mes)
            mes_inicial=ind_mespago1
            if ind_mesrev1 > ind_mespago1:
                agno_curso=agno_firma+1
                agno_perpago=agno_firma+1

            for m in range(0, contador_revisiones): 
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                ferc=m+2
                if ferc % 2 == 0:
                    mesRev=mes1_bi
                elif ferc % 2 ==1:
                    mesRev=mes2_bi

                if (lista_mesrevision_bianual[m][tipo_indice1]) == '':
                
                    Df_cons_ind1=df_ind_sust1[(df_ind_sust1['AGNO']== agno_curso) & (df_ind_sust1['MES']==mesRev)]
                    lista_numpy_ind=Df_cons_ind1.to_numpy().tolist()
                    if ejec1==16:
                        valor_indice=lista_numpy_ind[0][2]
                    elif ejec1==17:
                        valor_indice=lista_numpy_ind[0][5]
                    elif ejec1!=16 and ejec1!=17:
                        valor_indice=ejec1

                else:
                    valor_indice=round((lista_mesrevision_bianual[m][tipo_indice1]),3)

                i_fijo_anual=valor_indice+diferencial_aplicado1
                j_fijo_anual=(1+(i_fijo_anual/600))**(-numero_plazos_fijoanual)
                cuota_mes=round(((capital_pendiente * (i_fijo_anual/600))/(1-j_fijo_anual)),3)
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el segundo índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if lista_mesrevision_bianual[m][tipo_indice2] == '':
                    valor_indice2=ejec2
                else:    
                    valor_indice2=round((lista_mesrevision_bianual[m][tipo_indice2]),3)

                i_fijo_anual2=valor_indice2+diferencial_aplicado2
                j_fijo_anual2=(1+(i_fijo_anual2/600))**(-numero_plazos_fijoanual)
                cuota_mes2=round(((capital_pendiente2 * (i_fijo_anual2/600))/(1-j_fijo_anual2)),3)                
                
                for n in range (0,6): 

                    revisionnumero= m + 1
                    numerocuota = (m * 6) + (n + 1)
                    mesCuota=self.lista_meses_anual[mes_inicial]
                    mes_inicial=mes_inicial+1

                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual= round(((capital_pendiente * (i_fijo_anual/1200))),3)
                    amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                    capital_pendiente=round((capital_pendiente-amortizacion_mensual),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual2= round(((capital_pendiente2 * (i_fijo_anual2/1200))),3)
                    amortizacion_mensual2=round((cuota_mes2-interes_mensual2),3)
                    capital_pendiente2=round((capital_pendiente2-amortizacion_mensual2),3) 
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx cálculo con la diferencia entre cuotas xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx             
                    a_devolver= round((cuota_mes - cuota_mes2),3)
                    cantidad_amortizar=round((amortizacion_mensual2-amortizacion_mensual),3)
        
                    numero_plazos_fijoanual=numero_plazos_fijoanual-1   

                    mes_revision=""
                    if mes == mesCuota:
                        mes_revision=mes
                    elif mes2==mesCuota:
                        mes_revision=mes2
                    else:
                        mes_revision = ''

                    messs=self.diccionario_mesespago[mesCuota]
                    fec_pag= str(Fecha_pagomes)+'-'+ str(messs) +'-'+str(agno_curso)
                    date_object=datetime.strptime(fec_pag, '%d-%m-%Y')
            
                    acumuladoint=0

                    for k in range (0,tere):
                        Ini=str(lista_numpy[k][3])
                        Fin=str(lista_numpy[k][4])
                        Leg_in=(lista_numpy[k][1])
                        date_inicio=datetime.strptime(Ini, '%d-%m-%Y')
                        date_final=datetime.strptime(Fin, '%d-%m-%Y')
                        int_agno_calc=0.000 

                        if date_object>date_final:
                            int_agno_calc=0.000
                        elif date_object > date_inicio and date_object < date_final:  
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_object).days))/(365*100)    
                        else:   
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_inicio).days))/(365*100)

                        acumuladoint=acumuladoint+int_agno_calc
                   
                    acumuladoint=round(acumuladoint,3)
                
                    sql_temporal_bianualsinfijo = ("INSERT INTO Datos_temporales_bianual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

                    self.conexion.execute(sql_temporal_bianualsinfijo, (revisionnumero, agno_curso, mesCuota, numerocuota , 
                                                    cuota_mes, interes_mensual, amortizacion_mensual, 
                                                    capital_pendiente, valor_indice,
                                                    cuota_mes2, interes_mensual2, amortizacion_mensual2, 
                                                    capital_pendiente2, valor_indice2, cantidad_amortizar, a_devolver, date_object, acumuladoint, mes_revision
                                                    ))
                                
                    if mes_inicial > 11:
                        mes_inicial=0
                        agno_curso=agno_curso+1
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")

    def buscar_rangobianual_confijo(self, tip_ind1, tip_ind2, agno_firma, agno_actual, mes, perpagomes1, perpagomes2, diferenciall1, diferenciall2, plazosvariable, sust1, sust2, Fecha_pagomes):
        try:
            lista_meses_bianual= [
                        ["Enero" ,"Julio", agno_firma, agno_firma], ["Febrero" ,"Agosto", agno_firma, agno_firma], 
                        ["Marzo" ,"Septiembre", agno_firma, agno_firma], ["Abril" ,"Octubre", agno_firma, agno_firma], 
                        ["Mayo" ,"Noviembre", agno_firma, agno_firma], ["Junio" ,"Diciembre", agno_firma, agno_firma],
                        ["Julio" ,"Enero", agno_firma, agno_firma+1], ["Agosto" ,"Febrero", agno_firma, agno_firma+1], 
                        ["Septiembre" ,"Marzo", agno_firma, agno_firma+1], ["Octubre" ,"Abril", agno_firma, agno_firma+1], 
                        ["Noviembre" ,"Mayo", agno_firma, agno_firma+1], ["Diciembre" ,"Junio", agno_firma, agno_firma+1]              
                                    ]           
            mes1_bi=mes
            for q in range (0,12):
                if lista_meses_bianual[q][0]==mes:
                    mes2_bi=lista_meses_bianual[q][1]

            for i in range (0,12):   
                comodin= lista_meses_bianual[i][0]
                if comodin == mes:
                    mes2=lista_meses_bianual[i][1]
                    agno2=lista_meses_bianual[i][3]
            
            sql=("SELECT AGNO, MES, ENTIDADES, BANCOS, CAJAS, EURIBOR, FIJO, DIFERENCIAL, OTRO FROM Historico_Indices WHERE (AGNO BETWEEN ? AND ? AND MES= ?)\
                OR (AGNO BETWEEN ? AND ? AND MES= ?) ")
            self.mi_cursor.execute(sql, (agno_firma, agno_actual, mes, agno2, agno_actual, mes2))        
            registros=self.mi_cursor.fetchall()

            lista_mesrevision_bianual=[]
            for i in registros:
                ii=list(i)
                if ii[1]== mes:
                    ii.append(perpagomes1)
                else:
                    ii.append(perpagomes2)
                lista_mesrevision_bianual.append(ii)
            
            contador_revisiones=len(lista_mesrevision_bianual)
            
            tipo_indice1 = self.diccionario_indices[tip_ind1]
            tipo_indice2 = self.diccionario_indices[tip_ind2]
            ejec1=round(float(sust1),3)
            ejec2=round(float(sust2),3)
            capital_inicial=self.CAPITAL_PENDIENTE

            capital_pendiente=capital_inicial
            capital_pendiente2=capital_inicial
            diferencial_aplicado1=diferenciall1
            diferencial_aplicado2=diferenciall2
            numero_plazos_fijoanual=plazosvariable

    ######## 5 / 7 ############################################################################################################################################
            # Conexion a tabla interes legal dinero
            #nombre_conexion_din=self.resolver_ruta("Base_datos_IH.db")
            #conexion_din = sqlite3.connect(nombre_conexion_din)
            conexion_din = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
            df_intl = pd.read_sql_query("SELECT * FROM Interes_dinero", conexion_din)
            df_ind_sust1 = pd.read_sql_query("SELECT * FROM Historico_Indices", conexion_din)
            conexion_din.close()
            lista_numpy=df_intl.to_numpy().tolist()
            tere=len(lista_numpy)

            agno_curso=agno_firma
            agno_perpago=agno_firma
            ind_mespago1=self.lista_meses_anual.index(perpagomes1)

            ind_mesrev1=self.lista_meses_anual.index(mes)
            mes_inicial=ind_mespago1
            if ind_mesrev1 > ind_mespago1:
                agno_curso=agno_firma+1
                agno_perpago=agno_firma+1

            for m in range(0, contador_revisiones):   
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                ferc=m+2
                if ferc % 2 == 0:
                    mesRev=mes1_bi
                elif ferc % 2 ==1:
                    mesRev=mes2_bi

                if (lista_mesrevision_bianual[m][tipo_indice1]) == '':
                    Df_cons_ind1=df_ind_sust1[(df_ind_sust1['AGNO']== agno_curso) & (df_ind_sust1['MES']==mesRev)]
                    lista_numpy_ind=Df_cons_ind1.to_numpy().tolist()
                    if ejec1==16:
                        valor_indice=lista_numpy_ind[0][2]
                    elif ejec1==17:
                        valor_indice=lista_numpy_ind[0][5]
                    elif ejec1!=16 and ejec1!=17:
                        valor_indice=ejec1
                else:
                    valor_indice=round((lista_mesrevision_bianual[m][tipo_indice1]),3)
                
                i_fijo_anual=valor_indice+diferencial_aplicado1
                j_fijo_anual=(1+(i_fijo_anual/600))**(-numero_plazos_fijoanual)
                cuota_mes=round(((capital_pendiente * (i_fijo_anual/600))/(1-j_fijo_anual)),3)
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Primer cálculo con el segundo índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                if lista_mesrevision_bianual[m][tipo_indice2] == '':
                    valor_indice2=ejec2
                else:
                    valor_indice2=round((lista_mesrevision_bianual[m][tipo_indice2]),3)

                i_fijo_anual2=valor_indice2+diferencial_aplicado2
                j_fijo_anual2=(1+(i_fijo_anual2/600))**(-numero_plazos_fijoanual)
                cuota_mes2=round(((capital_pendiente2 * (i_fijo_anual2/600))/(1-j_fijo_anual2)),3)                
                
                for n in range (0,6): 

                    revisionnumero= m + 1
                    numerocuota = (m * 6) + (n + 1)
                    mesCuota=self.lista_meses_anual[mes_inicial]
                    mes_inicial=mes_inicial+1

                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual= round(((capital_pendiente * (i_fijo_anual/1200))),3)
                    amortizacion_mensual=round((cuota_mes-interes_mensual),3)
                    capital_pendiente=round((capital_pendiente-amortizacion_mensual),3)
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Segundo cálculo con el primer índice xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    interes_mensual2= round(((capital_pendiente2 * (i_fijo_anual2/1200))),3)
                    amortizacion_mensual2=round((cuota_mes2-interes_mensual2),3)
                    capital_pendiente2=round((capital_pendiente2-amortizacion_mensual2),3) 
                    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx cálculo con la diferencia entre cuotas xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx             
                    a_devolver= round((cuota_mes - cuota_mes2),3)
                    cantidad_amortizar=round((amortizacion_mensual2-amortizacion_mensual),3)
        
                    numero_plazos_fijoanual=numero_plazos_fijoanual-1  

                    mes_revision=""
                    if mes == mesCuota:
                        mes_revision=mes
                    elif mes2==mesCuota:
                        mes_revision=mes2
                    else:
                        mes_revision = ''

                    messs=self.diccionario_mesespago[mesCuota]
                    fec_pag= str(Fecha_pagomes)+'-'+ str(messs) +'-'+str(agno_curso)
                    date_object=datetime.strptime(fec_pag, '%d-%m-%Y')
            
                    acumuladoint=0

                    for k in range (0,tere):
                        Ini=str(lista_numpy[k][3])
                        Fin=str(lista_numpy[k][4])
                        Leg_in=(lista_numpy[k][1])
                        date_inicio=datetime.strptime(Ini, '%d-%m-%Y')
                        date_final=datetime.strptime(Fin, '%d-%m-%Y')
                        int_agno_calc=0.000 

                        if date_object>date_final:
                            int_agno_calc=0.000
                        elif date_object > date_inicio and date_object < date_final:  
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_object).days))/(365*100)    
                        else:   
                            int_agno_calc=(Leg_in * (a_devolver) * ((date_final-date_inicio).days))/(365*100)

                        acumuladoint=acumuladoint+int_agno_calc
            
                    acumuladoint=round(acumuladoint,3)

                    sql_temporal_bianualconfijo = ("INSERT INTO Datos_temporales_bianual (NUMERO_REVISION, AGNO, MESCUOTA, NUMERO_CUOTA, CUOTA_MES, \
                                                                INTERES_MES, AMORTIZACION_MES, CAPITAL_PENDIENTE, VALOR_INDICE,\
                                                                CUOTA_MES2, INTERES_MES2, AMORTIZACION_MES2,\
                                                                CAPITAL_PENDIENTE2, VALOR_INDICE2, AMORTIZAR, DEVOLVER, FECHA_PAGO, ACUMU_CONINT, MES_REVISION)\
                                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

                    self.conexion.execute(sql_temporal_bianualconfijo, (revisionnumero, agno_curso, mesCuota, numerocuota , 
                                                    cuota_mes, interes_mensual, amortizacion_mensual, 
                                                    capital_pendiente, valor_indice,
                                                    cuota_mes2, interes_mensual2, amortizacion_mensual2, 
                                                    capital_pendiente2, valor_indice2, cantidad_amortizar, a_devolver, date_object, acumuladoint, mes_revision
                                                    ))
                                
                    if mes_inicial > 11:
                        mes_inicial=0
                        agno_curso=agno_curso+1
        except:
            QMessageBox.about(self, "INFORMACION", "Error en los datos facilitados")

    def intro_cmdin(self):
######## 6 / 7 ############################################################################
        #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
        #self.conexion = sqlite3.connect(nombre_conexion)
        self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
        self.mi_cursor=self.conexion.cursor() 

        sql_0= "DELETE FROM Comodin;"
        self.mi_cursor.execute(sql_0)
        now = datetime.now()
        comodin_obt=self.TIPOPAGO
        sql=("INSERT INTO Comodin (FECHA, TIPOPAGO) VALUES (?,?)")
        for i in range (0,8):
            self.conexion.execute(sql, (now, comodin_obt))
        self.conexion.commit()
        self.conexion.close()                   
    def open_Data_Graph(self):
        if self.TIPOPAGO=="Solo fijo":
            self.ventana_data_fijo=Consultas_graficos_fijo()
            self.ventana_data_fijo.setModal(True)
            self.ventana_data_fijo.exec_()
        else:
            self.ventana_data_variable=Consultas_graficos()
            self.ventana_data_variable.setModal(True)
            self.ventana_data_variable.exec_()

    def ejecutar_datosGenerales(self):
        if self.fecha_pago_cuota > self.fecha_pago_cancelacion:
            QMessageBox.about(self, "Información", "error de ejecución......, actualize lineas de código!!!")
            quit()
        else:
            try:
################ 7 / 7 ################################################################################################################
                #nombre_conexion=self.resolver_ruta("Base_datos_IH.db")
                #self.conexion = sqlite3.connect(nombre_conexion)
                self.conexion = sqlite3.connect("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/Base_datos_IH.db")
                self.mi_cursor=self.conexion.cursor() 
                self.TIPOPAGO=self.comboBox_tipopago.currentText()
                Tipo_pago = self.comboBox_tipopago.currentText()
                Capital_Initial= float(self.lineEdit_capitalinicial.text())
                if Capital_Initial <= 0:
                    QMessageBox.about(self, "Información", "Ha ingresado el capital inicial incorrecto")

                NPlazosTotales=int(self.lineEdit_plazostotales.text())
                if NPlazosTotales < 1 or NPlazosTotales >400:
                    QMessageBox.about(self, "Información", "Ha ingresado el nº de plazos totales incorrecto, no ha de ser superior a 400")

                Agno_firma_hip= int(self.comboBox_agnofirma.currentText())   
                Agno_actualcurso= int(self.comboBox_agnocurso.currentText())
                Fecha_pagomes=int(self.spinBox_diapago.value())
                

                if Tipo_pago == "Solo fijo" and (self.tabWidget_tipospago.currentIndex()) == 0:

                    sql_1= "DELETE FROM Datos_soloFijo;"
                    self.mi_cursor.execute(sql_1)

                    NPlazos_Fijo=NPlazosTotales
                    Interes_fijoapli= float(self.lineEdit_interesfijoapli1.text())
                    if Interes_fijoapli < -15 or Interes_fijoapli > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el interes fijo incorrecto")

                    Pago_confijo= self.comboBox_mespagofijo1.currentText()

                    self.calculo_Solo_interesfijo(Agno_firma_hip, Pago_confijo, NPlazosTotales, NPlazos_Fijo, Capital_Initial, Interes_fijoapli, Fecha_pagomes)

                if Tipo_pago == 'Variable anual' and (self.tabWidget_tipospago.currentIndex()) == 1 :

                    sql_2= "DELETE FROM Datos_temporales_anual;"
                    self.mi_cursor.execute(sql_2)

                    Tipo_indiceapli= self.comboBox_indiceapli2.currentText()
                    Tipo_indicecontrast= self.comboBox_indicecomp2.currentText()

                    sust1= float(self.lineEdit_sust12.text())
                    if sust1 < -15 or sust1 > 17:
                        QMessageBox.about(self, "Información", "Ha ingresado valor sustitutorio 1 incorrecto")

                    sust2= float(self.lineEdit_sust22.text())
                    if sust2 < -15 or sust2 > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado valor sustitutorio 2 incorrecto")

                    DiferencialAplicado1= float(self.lineEdit_dif12.text())
                    if DiferencialAplicado1 < -5 or DiferencialAplicado1 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado incorrecto")
                        
                    DiferencialAplicado2= float(self.lineEdit_dif22.text())
                    if DiferencialAplicado2 < -5 or DiferencialAplicado2 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado comparativo incorrecto")
                        
                    Mes_derevision= self.comboBox_mesrevisionanual2.currentText()
                    PrimerMesPago= self.comboBox_primermespagoanual2.currentText()
                    NumeroPlazosVariable=NPlazosTotales
                
                    self.buscar_rangoanual_sinfijo(Tipo_indiceapli, Tipo_indicecontrast, Agno_firma_hip, Agno_actualcurso, Mes_derevision, PrimerMesPago, DiferencialAplicado1, DiferencialAplicado2, NumeroPlazosVariable, Capital_Initial, sust1, sust2, Fecha_pagomes)


                if Tipo_pago == 'Variable anual con fijo' and (self.tabWidget_tipospago.currentIndex()) == 2:

                    sql_2= "DELETE FROM Datos_temporales_anual;"
                    self.mi_cursor.execute(sql_2)

                    NPlazosFijo= int(self.lineEdit_nplazosfijo3.text())
                    Interes_fijoapli= float(self.lineEdit_interesfijoapli3.text())
                    if Interes_fijoapli < -15 or Interes_fijoapli > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el interes fijo incorrecto")
                
                    Pago_confijo= self.comboBox_mespagofijo3.currentText()

                    Tipo_indiceapli= self.comboBox_indiceapli3.currentText()
                    Tipo_indicecontrast= self.comboBox_indicecomp3.currentText()

                    sust1= float(self.lineEdit_sust13.text())
                    if sust1 < -15 or sust1 > 17:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 1 incorrecto")
                        
                    sust2= float(self.lineEdit_sust23.text())
                    if sust2 < -15 or sust2 > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 2 incorrecto")
                        
                    DiferencialAplicado1= float(self.lineEdit_dif13.text())
                    if DiferencialAplicado1 < -5 or DiferencialAplicado1 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado incorrecto")
                        
                    DiferencialAplicado2= float(self.lineEdit_dif23.text())
                    if DiferencialAplicado2 < -5 or DiferencialAplicado2 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado comparativo incorrecto")

                    Mes_derevision= self.comboBox_mesrevisionanual3.currentText()
                    PrimerMesPago= self.comboBox_primermespagoanual3.currentText()

                    NumeroPlazosVariable=int(NPlazosTotales-NPlazosFijo)
                    ANN_HIPanual=int(Agno_firma_hip + (NPlazosFijo/12))

                    self.calculo_interesfijo(Tipo_pago, Agno_firma_hip, Pago_confijo, NPlazosTotales, NPlazosFijo, Capital_Initial, Interes_fijoapli, Fecha_pagomes)
                    self.buscar_rangoanual_confijo(Tipo_indiceapli, Tipo_indicecontrast, ANN_HIPanual, Agno_actualcurso, Mes_derevision, PrimerMesPago, DiferencialAplicado1, DiferencialAplicado2, NumeroPlazosVariable, sust1, sust2,Fecha_pagomes)


                if Tipo_pago == 'Variable semestral' and (self.tabWidget_tipospago.currentIndex()) == 3 :

                    sql_3= "DELETE FROM Datos_temporales_bianual;"
                    self.mi_cursor.execute(sql_3)

                    Tipo_indiceapli= self.comboBox_indiceapli4.currentText()
                    Tipo_indicecontrast= self.comboBox_indicecomp4.currentText()

                    sust1= float(self.lineEdit_sust14.text())
                    if sust1 < -15 or sust1 > 17:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 1 incorrecto")

                    sust2= float(self.lineEdit_sust24.text())
                    if sust2 < -15 or sust2 > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 2 incorrecto")

                    DiferencialAplicado1= float(self.lineEdit_dif14.text())
                    if DiferencialAplicado1 < -5 or DiferencialAplicado1 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado incorrecto")

                    DiferencialAplicado2= float(self.lineEdit_dif24.text())
                    if DiferencialAplicado2 < -5 or DiferencialAplicado2 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado comparativo incorrecto")

                    Mes_derevisionbianual= self.comboBox_mesrevisionsemestral4.currentText()
                    PrimerMesPago_bianualsinfijo= self.comboBox_primermespagosemestral4.currentText()
                    NumeroPlazosVariable=int(NPlazosTotales)

                    lista_meses_Anual= ["Enero" ,"Febrero" ,"Marzo" ,"Abril" ,"Mayo" ,"Junio" ,"Julio" , "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]
                    segmes=lista_meses_Anual.index(PrimerMesPago_bianualsinfijo)
                    per=0
                    
                    for p in range (0,7):
                        pits=int(segmes+per)
                        estat=lista_meses_Anual[pits]
                        per=per+1
                        if (pits)==11:
                            per=0
                            segmes=0
                    SegundoMesPago_bianualsinfijo=estat

                    self.buscar_rangobianual_sinfijo(Tipo_indiceapli, Tipo_indicecontrast, Agno_firma_hip, Agno_actualcurso, Mes_derevisionbianual, PrimerMesPago_bianualsinfijo, SegundoMesPago_bianualsinfijo, DiferencialAplicado1, DiferencialAplicado2, NumeroPlazosVariable, Capital_Initial, sust1, sust2, Fecha_pagomes)
                                                                                                                                            

                if Tipo_pago == 'Variable semestral con fijo' and (self.tabWidget_tipospago.currentIndex()) == 4:
                    
                    lista_meses_Anual= ["Enero" ,"Febrero" ,"Marzo" ,"Abril" ,"Mayo" ,"Junio" ,"Julio" , "Agosto" ,"Septiembre" ,"Octubre" ,"Noviembre" ,"Diciembre"]
                    sql_3= "DELETE FROM Datos_temporales_bianual;"
                    self.mi_cursor.execute(sql_3)
                    
                    NPlazosFijo= int(self.lineEdit_nplazosfijo5.text())
                    Interes_fijoapli= float(self.lineEdit_interesfijoapli5.text())
                    if Interes_fijoapli < -15 or Interes_fijoapli > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el interes fijo incorrecto")
                    
                    Pago_confijo= self.comboBox_mespagofijo5.currentText()
                    Tipo_indiceapli= self.comboBox_indiceapli5.currentText()
                    Tipo_indicecontrast= self.comboBox_indicecomp5.currentText()

                    sust1= float(self.lineEdit_sust15.text())
                    if sust1 < -15 or sust1 > 17:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 1 incorrecto")

                    sust2= float(self.lineEdit_sust25.text())
                    if sust2 < -15 or sust2 > 15:
                        QMessageBox.about(self, "Información", "Ha ingresado el valor sustitutorio 2 incorrecto")

                    DiferencialAplicado1= float(self.lineEdit_dif15.text())
                    if DiferencialAplicado1 < -5 or DiferencialAplicado1 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado incorrecto")

                    DiferencialAplicado2= float(self.lineEdit_dif25.text())
                    if DiferencialAplicado2 < -5 or DiferencialAplicado2 > 5:
                        QMessageBox.about(self, "Información", "Ha ingresado el diferencial aplicado comparativo incorrecto")

                    Mes_derevisionbianual= self.comboBox_mesrevisionsemestral5.currentText() 
                    
                    NumeroPlazosVariablebifijo= int(NPlazosTotales)-int(NPlazosFijo)
                    I_nd=lista_meses_Anual.index(Pago_confijo)
                    cont=0
                    for z in range (0,NPlazosFijo):
                        s=I_nd
                        I_nd=I_nd+1
                        if s ==11:
                            I_nd=0
                            cont=cont+1
                    ANN_HIPbianual=cont+Agno_firma_hip
                    PrimerMesPago_bianualconfijo= lista_meses_Anual[s+1]
                    ger=s+1
                    for mn in range(0,7):
                        rr=ger
                        ger=ger+1
                        if rr==11:
                            ger=0
                    SegundoMesPago_bianualconfijo=lista_meses_Anual[rr]

                    self.calculo_interesfijo(Tipo_pago, Agno_firma_hip, Pago_confijo, NPlazosTotales, NPlazosFijo, Capital_Initial, Interes_fijoapli, Fecha_pagomes)
                    self.buscar_rangobianual_confijo(Tipo_indiceapli, Tipo_indicecontrast, ANN_HIPbianual, Agno_actualcurso, Mes_derevisionbianual, PrimerMesPago_bianualconfijo, SegundoMesPago_bianualconfijo, DiferencialAplicado1, DiferencialAplicado2, NumeroPlazosVariablebifijo, sust1, sust2, Fecha_pagomes)
                
                self.conexion.commit()
                self.conexion.close() 

                for le in self.findChildren(QLineEdit):
                    le.clear() 
                for le in self.findChildren(QComboBox):
                    le.setCurrentIndex(0) 

                self.intro_cmdin()
                self.open_Data_Graph()
            except:
                QMessageBox.about(self, "INFORMACION", "Error en la ejecución del programa: sin datos/faltan datos/conflicto de datos")

        for n in range (0,5):
            self.tabWidget_tipospago.setTabEnabled(n, False)

    def do_select(self):
        try:
            for n in range (0,5):
                self.tabWidget_tipospago.setTabEnabled(n, False) 
            select_comb = self.comboBox_tipopago.currentText()
            val_comb=self.dic_lista_Tipo_pago[select_comb]
            self.tabWidget_tipospago.setTabEnabled(val_comb, True)                                                
        except:
            pass

################ / ################################################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

############################################################################################################################################################
if __name__ == "__main__":
    app=QApplication(sys.argv)
    GUI=ejemplo_GUI()
    GUI.show()
    sys.exit(app.exec_())





  


