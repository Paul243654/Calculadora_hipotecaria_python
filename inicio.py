from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QComboBox, QPushButton,QListWidget, QTableView, QTableWidgetItem, QVBoxLayout, QGridLayout, QGraphicsView
import os, sys
from calculo_interes import ejemplo_GUI
from Ficher_datos import Importaciondatos
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
import webbrowser

class Consultas_graficos(QDialog):
    def __init__(self):
        super().__init__()
######## 1 / 2 ####################################################################################################################################
        #nombre_archivo=self.resolver_ruta("formulario_hipoteca_acceso.ui")
        #uic.loadUi(nombre_archivo, self)
        uic.loadUi("C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/formulario_hipoteca_acceso.ui", self)
        self.pushButton_ircalculadora.setDisabled(True)
        self.pushButton_iringresodatos.setDisabled(True)

        self.pushButton_ircalculadora.clicked.connect(self.op_calc)
        self.pushButton_iringresodatos.clicked.connect(self.op_hist)
        self.pushButton_delprogramainicio.clicked.connect(self.close)
        self.pushButton_inicio.clicked.connect(self.Gui_login)
        self.pushButton_manual.clicked.connect(self.leer_guia)

    def leer_guia(self):
######## 2 / 2 #######################################################################################################################################
        #nombre_pdf=self.resolver_ruta('GUIA DE USO.pdf')
        #webbrowser.open_new(nombre_pdf)
        webbrowser.open_new('C:/Users/Paul/Desktop/PROYECTOS INFORMATICOS/CALCULADORA HIPOTECARIA PYTHON/GUIA DE USO.pdf')

    def Gui_login(self):
        user_name=self.lineEdit_user.text()
        user_pwd=self.lineEdit_pwd.text()

        if len(user_name) == 0 or len(user_pwd) == 0 :
            QMessageBox.about(self, "INFORMACION","No ha ingresado un usuario/paswword")
            self.pushButton_ircalculadora.setDisabled(True)
            self.pushButton_iringresodatos.setDisabled(True)
        elif user_name == "admin" and user_pwd == "admin":
            self.pushButton_ircalculadora.setDisabled(False)
            self.pushButton_iringresodatos.setDisabled(False)
            self.lineEdit_user.clear()
            self.lineEdit_pwd.clear()
        else:    
            QMessageBox.about(self, "INFORMACION","usuario/paswword incorrectos")
            self.lineEdit_user.clear()
            self.lineEdit_pwd.clear()
            self.pushButton_ircalculadora.setDisabled(True)
            self.pushButton_iringresodatos.setDisabled(True)

    def open_historicoDatos(self):
        self.ventana_ingresoDatos=Importaciondatos()
        self.ventana_ingresoDatos.setModal(True)
        self.ventana_ingresoDatos.exec_()

    def open_calculadoraH(self):
        self.ventana_calculadora=ejemplo_GUI()
        self.ventana_calculadora.setModal(True)
        self.ventana_calculadora.exec_()

    def op_hist(self):
        try:
            self.open_historicoDatos()
        except:
            QMessageBox.about(self, "INFORMACION", "Error en la importación de módulo")

    def op_calc(self):
        try:
            self.open_calculadoraH()
        except:
            QMessageBox.about(self, "INFORMACION","Error en la importación de módulo")

########  / #######################################################################################################################################
    def resolver_ruta(self,ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath('.'), ruta_relativa)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    GUIa=Consultas_graficos()
    GUIa.show()
    sys.exit(app.exec_())