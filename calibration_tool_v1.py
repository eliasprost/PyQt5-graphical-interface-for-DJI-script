#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Elias Prost
"""
import subprocess 
import sys
import time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox
import webbrowser
from PyQt5CustomMessageBoxWithAutoclose import CustomMessageBox

##### 1 - Welcome dialog
class IntroMenu(QDialog): 
    def __init__(self):
        super(IntroMenu, self).__init__()
        loadUi("intro_dialog.ui", self)
        self.to_menu_button.clicked.connect(self.go_to_calibrate_menu)
        self.to_exit_button.clicked.connect(self.close_program)
        self.info_button.clicked.connect(self.info_author)
        
    def info_author(self):
        webbrowser.open("https://www.facebook.com/dronecollisioncenter/", new=2, autoraise=True)
            
    def go_to_calibrate_menu(self):
        calibration_menu_inst = CalibrationMenu()
        widget.addWidget(calibration_menu_inst)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def close_program(self):
        widget.close()

         
##### Menu 2 - calibration box
class CalibrationMenu(QMainWindow):
    def __init__(self):
        super(CalibrationMenu, self).__init__()
        loadUi("calibration_menu.ui", self) 

        # Set calibrates, info and back buttons
        self.calibrate_button_jc.clicked.connect(self.go_script_JointCoarse)
        self.calibrate_button_lh.clicked.connect(self.go_script_LinearHall)
        self.info_button.clicked.connect(self.info_author)
        self.back_button.clicked.connect(self.go_back)
        
        # Qradio buttons - select drone model
        self.spark_select.toggled.connect(self.select_model_port)
        self.mavic_air_select.toggled.connect(self.select_model_port)
        self.mavic_2_z_select.toggled.connect(self.select_model_port)
        self.mavic_2_p_select.toggled.connect(self.select_model_port)
        self.mavic_mini_select.toggled.connect(self.select_model_port)
        self.mavic_air_2_select.toggled.connect(self.select_model_port)
        self.mavic_air_2_S_select.toggled.connect(self.select_model_port)
        self.mavic_air_mini_2_select.toggled.connect(self.select_model_port)
        
        # QSpinBox - select port
        self.port_selector.valueChanged.connect(self.select_model_port)
        
    def go_back(self): # Go to the previous menu
        Intro_menu_inst = IntroMenu()
        widget.addWidget(Intro_menu_inst)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def info_author(self):
        webbrowser.open("https://www.facebook.com/dronecollisioncenter/", new=2, autoraise=True)
    
    def select_model_port(self): # take data from Qradio buttons and select model.
                                 # take data from spinbox and select port.
                                 # set text of label by information of port and model selected.
        model= "---"
        port= "---"
        
        if self.spark_select.isChecked() == True:
            model = "WM100"
                
        if self.mavic_air_select.isChecked() == True:
            model = "WM230"
                
        if self.mavic_2_z_select.isChecked() == True:
            model = "WM240"
            
        if self.mavic_2_p_select.isChecked() == True:
            model = "WM240"
            
        if self.mavic_mini_select.isChecked() == True:
            model = "WM160"
            
        if self.mavic_air_2_select.isChecked() == True:
            model = "WM231"
                
        if self.mavic_air_2_S_select.isChecked() == True:
            model = "WM231"
            
        if self.mavic_air_mini_2_select.isChecked() == True:
            model = "WM160"
        
        port = str(self.port_selector.value())
        
        # Label show
        self.select_label.setText(f"El modelo seleccioando es: {model}, en el puerto: com{port}")

        return port, model
        
    
    def go_script_JointCoarse(self): # launch JointCoarse command from script "comm_og_service_tool.py" 
        # Set variables to call in DJI script
        port_ = CalibrationMenu.select_model_port(self)[0]
        model_ = CalibrationMenu.select_model_port(self)[1]
        
        #Launch DJI calibration script with arguments
        cmd = f"python comm_og_service_tool.py com{port_} {model_} GimbalCalib JointCoarse"        
        subprocess.Popen(cmd, shell=True)
        
        #Launch message box
        CustomMessageBox.showWithTimeout(15, "\nINFO: Calibration process started; monitoring progress. The Gimbal will move through its boundary positions, then it will fine-tune its central position.\n\nIt will take around 15 seconds, please wait.\n\n(if an error appeared previously, discard this window and retry with differents parameters)\n\n*The window will close automatically after the scheduled time*", "Joint Coarse", icon=QMessageBox.Information, buttons=QMessageBox.Discard)
  
    def go_script_LinearHall(self): # launch LinearHall command from script "comm_og_service_tool.py" 
        # Set variables to call in DJI script
        port_ = CalibrationMenu.select_model_port(self)[0]
        model_ = CalibrationMenu.select_model_port(self)[1]
        
        #Launch DJI calibration script with arguments
        cmd = f"python comm_og_service_tool.py com{port_} {model_} GimbalCalib LinearHall"
        subprocess.Popen(cmd, shell=True)
        
        #Launch message box
        CustomMessageBox.showWithTimeout(30, "\nINFO: Calibration process started; monitoring progress.The Gimbal will slowly move through all positions in all axes, several times.\n\nIt will take around 30 seconds, please wait.\n\n(if an error appeared previously, discard this window and retry with differents parameters)\n\n*The window will close automatically after the scheduled time*", "Linear Hall", icon=QMessageBox.Information, buttons=QMessageBox.Discard)

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)   
    widget = QtWidgets.QStackedWidget()
    
    # launch screen 1 - Intro Menu
    intro_menu_inst = IntroMenu()
    widget.addWidget(intro_menu_inst)
    
    # set widget height and width / title
    widget.setFixedHeight(440)
    widget.setFixedWidth(337)
    widget.setWindowTitle("DDC Drone Tools V1.0")
    
    # Show
    widget.show()
    
    sys.exit(app.exec_())
    