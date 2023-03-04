# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.15.8

#  ---------------------------- FIX -------------------------------
# V 0.0.2    Fix after save item shows my machines

import locale  # Για να δείχνει τους αριθμούς με τελεία πχ 1.000

locale.setlocale(locale.LC_ALL, "")  # Για να δείχνει τους αριθμούς με τελεία πχ 1.000

import db
import edit_window
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from datetime import datetime

today_obj = datetime.today()

BASE_PATH = f"\\\\network\\full\\path\\{today_obj.year}"
YEARS_PATH = BASE_PATH[:-4]
YEARS = os.listdir(YEARS_PATH)
mlshop = 1

if mlshop:
    # ML Shop dbases
    DBASE = os.path.join(BASE_PATH, "Μηχανήματα.db")
    BASE_DIR = os.path.join(BASE_PATH, "ΑΡΧΕΙΑ")
else:  # VPN
    DBASE = "Μηχανήματα_2023.db"  # Local Dbase
    BASE_DIR = "ΑΡΧΕΙΑ"
    # dbase = "\\\\10.8.0.1\\Public\\GOOGLE-DRIVE\\ΕΓΓΡΑΦΑ\\6.  ΒΙΒΛΙΟ SERVICE\\Service_book.db"  #  VPN Windows

ENGINE = create_engine(f"sqlite:///{DBASE}")
SESSION = sessionmaker(bind=ENGINE)()
BASE = declarative_base()
# conn = session.bind
CONN = ENGINE.connect()

db.engine = ENGINE
db.session = SESSION
db.conn = CONN
edit_window.session = SESSION

import settings
from PyQt5 import QtCore, QtGui, QtWidgets
import re
import pathlib  # Για backup
import shutil
import traceback
import pandas as pd  # To excel
from sqlalchemy import select
import sys
from settings import VERSION, today, root_logger
from edit_window import Edit_Ui_Form_Window
from db import fetch_clicked_table_data, fetch_all_table_data, Οροφος_1, Οροφος_2, Οροφος_4, Οροφος_5, Οροφος_6, \
    Πασιάς, Κτηνιατρείο, Πρωτοβάθμια, Δευτεροβάθμια, Κτέο, Αμύνταιο, Κεδασυ, Εκτός, \
    get_total_counter, tables, get_my_machines, search_in_table, search_code_in_table, \
    search_in_my_machines, search_code_in_my_machines, search_in_all_tables, search_code_in_all_machines, conn

sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


# Κάνουμε sub class το QTreeWidgetItem για να κάνει sort τους αριθμούς που είναι σε string μορφή
class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        return self.natural_sort_key(key1) < self.natural_sort_key(key2)

    @staticmethod
    def natural_sort_key(key):
        regex = '(\d*\.\d+|\d+)'
        parts = re.split(regex, key)
        return tuple((e if i % 2 == 0 else float(e)) for i, e in enumerate(parts))


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.edit_window = None
        self.add_window = None
        self.second_edit_window = None
        self.selected_table = None
        self.data_to_show = None
        self.total_ypiresias = 0
        self.selected_year = settings.today_obj.year
        self.total_prints = get_total_counter()
        self.edit_item = None
        self.add_item = None
        self.second_edit_window = None
        self.second_edit_item = None
        self.my_table = False
        self.all_machines = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 800))
        MainWindow.setWindowTitle(f"Μηχανήματα Περιφέρειας Φλώρινας {VERSION}  {self.selected_year}")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/periferia.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        # ----------------------------------------FONTS-------------------------------------------------
        self.font_12 = QtGui.QFont()
        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)
        self.font_12.setBold(False)
        self.font_12.setItalic(False)
        self.font_12.setWeight(10)

        self.font_14_bold = QtGui.QFont()
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(85)

        self.font_14 = QtGui.QFont()
        self.font_14.setFamily("Calibri")
        self.font_14.setPointSize(14)
        self.font_14.setBold(False)
        self.font_14.setWeight(55)

        self.font_12_bold = QtGui.QFont()
        self.font_12_bold.setFamily("Calibri")
        self.font_12_bold.setPointSize(12)
        self.font_12_bold.setBold(True)
        self.font_12_bold.setWeight(75)
        self.font_20_bold = QtGui.QFont()
        self.font_20_bold.setFamily("Calibri")
        self.font_20_bold.setPointSize(20)
        self.font_20_bold.setBold(True)
        self.font_20_bold.setWeight(85)
        self.font_16_bold = QtGui.QFont()
        self.font_16_bold.setFamily("Calibri")
        self.font_16_bold.setPointSize(16)
        self.font_16_bold.setBold(True)
        self.font_16_bold.setWeight(85)

        # -----------Shortcuts --------------------------
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), self.centralwidget)
        self.shortcut_esc.activated.connect(self.quit)
        # Εισαγωγή μηχανήματος
        self.shortcut_f1 = QtWidgets.QShortcut(QtGui.QKeySequence('F1'), self.centralwidget)
        self.shortcut_f1.activated.connect(self.show_add_window)

        # ----------------------------- Icons-------------------
        self.search_icon = QtGui.QIcon()
        self.search_icon.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floor_1_icon = QtGui.QIcon()
        self.floor_1_icon.addPixmap(QtGui.QPixmap("icons/1_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floor_2_icon = QtGui.QIcon()
        self.floor_2_icon.addPixmap(QtGui.QPixmap("icons/2_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floor_4_icon = QtGui.QIcon()
        self.floor_4_icon.addPixmap(QtGui.QPixmap("icons/4_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floor_5_icon = QtGui.QIcon()
        self.floor_5_icon.addPixmap(QtGui.QPixmap("icons/5_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floor_6_icon = QtGui.QIcon()
        self.floor_6_icon.addPixmap(QtGui.QPixmap("icons/6_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.refresh_icon = QtGui.QIcon()
        self.refresh_icon.addPixmap(QtGui.QPixmap("icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # 1ος Όροφος
        self.flor_1_btn = QtWidgets.QToolButton(self.centralwidget)
        self.flor_1_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.flor_1_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.flor_1_btn.setSizePolicy(sizePolicy)
        self.flor_1_btn.setToolTip("1ος Όροφος")
        self.flor_1_btn.setStatusTip("Μηχανήματα πρώτου ορόφου")
        self.flor_1_btn.setIcon(self.floor_1_icon)
        self.flor_1_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 90px")
        self.flor_1_btn.setShortcut("")
        self.flor_1_btn.setObjectName("flor_1_btn")
        self.flor_1_btn.clicked.connect(lambda: self.show_data(Οροφος_1))
        self.gridLayout.addWidget(self.flor_1_btn, 0, 0, 1, 1)

        # 2ος Όροφος
        self.flor_2_btn = QtWidgets.QToolButton(self.centralwidget)
        self.flor_2_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.flor_2_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.flor_2_btn.setSizePolicy(sizePolicy)
        self.flor_2_btn.setToolTip("2ος Όροφος")
        self.flor_2_btn.setStatusTip("Μηχανήματα δεύτερου ορόφου")
        self.flor_2_btn.setIcon(self.floor_2_icon)
        self.flor_2_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 90px")
        self.flor_2_btn.setObjectName("flor_2_btn")
        self.flor_2_btn.clicked.connect(lambda: self.show_data(Οροφος_2))
        self.gridLayout.addWidget(self.flor_2_btn, 0, 1, 1, 1)

        # 4ος Όροφος
        self.flor_4_btn = QtWidgets.QToolButton(self.centralwidget)
        self.flor_4_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.flor_4_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.flor_4_btn.setSizePolicy(sizePolicy)
        self.flor_4_btn.setToolTip("4ος Όροφος")
        self.flor_4_btn.setStatusTip("Μηχανήματα τέταρτου ορόφου")
        self.flor_4_btn.setIcon(self.floor_4_icon)
        self.flor_4_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 90px")
        self.flor_4_btn.setObjectName("flor_4_btn")
        self.flor_4_btn.clicked.connect(lambda: self.show_data(Οροφος_4))
        self.gridLayout.addWidget(self.flor_4_btn, 0, 2, 1, 1)

        # 5ος Όροφος
        self.flor_5_btn = QtWidgets.QToolButton(self.centralwidget)
        self.flor_5_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.flor_5_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.flor_5_btn.setSizePolicy(sizePolicy)
        self.flor_5_btn.setIcon(self.floor_5_icon)
        self.flor_5_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 90px")
        self.flor_5_btn.setToolTip("5ος Όροφος")
        self.flor_5_btn.setStatusTip("Μηχανήματα πέμπτου ορόφου")
        self.flor_5_btn.setObjectName("flor_5_btn")
        self.flor_5_btn.clicked.connect(lambda: self.show_data(Οροφος_5))
        self.gridLayout.addWidget(self.flor_5_btn, 0, 3, 1, 1)

        # 6ος Όροφος
        self.flor_6_btn = QtWidgets.QToolButton(self.centralwidget)
        self.flor_6_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.flor_6_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.flor_6_btn.setSizePolicy(sizePolicy)
        self.flor_6_btn.setToolTip("6ος Όροφος")
        self.flor_6_btn.setStatusTip("Μηχανήματα έκτου ορόφου")
        self.flor_6_btn.setIcon(self.floor_6_icon)
        self.flor_6_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 90px")
        self.flor_6_btn.setObjectName("flor_6_btn")
        self.flor_6_btn.clicked.connect(lambda: self.show_data(Οροφος_6))
        self.gridLayout.addWidget(self.flor_6_btn, 0, 4, 1, 1)

        # Πασιάς
        self.pasias_btn = QtWidgets.QToolButton(self.centralwidget)
        self.pasias_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.pasias_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.pasias_btn.setSizePolicy(sizePolicy)
        self.pasias_btn.setToolTip("Μηχανήματα Πασιά")
        self.pasias_btn.setFont(self.font_16_bold)
        self.pasias_btn.setText("ΠΑΣΙΑΣ")
        self.pasias_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.pasias_btn.setStatusTip("Μηχανήματα που είναι στο γραφείο του Πασιά Παντελή")
        self.pasias_btn.setObjectName("pasias_btn")
        self.pasias_btn.clicked.connect(lambda: self.show_data(Πασιάς))
        self.gridLayout.addWidget(self.pasias_btn, 0, 5, 1, 1)

        # Κτηνιατρείο
        self.ktiniatrio_btn = QtWidgets.QToolButton(self.centralwidget)
        self.ktiniatrio_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ktiniatrio_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.ktiniatrio_btn.setSizePolicy(sizePolicy)
        self.ktiniatrio_btn.setFont(self.font_16_bold)
        self.ktiniatrio_btn.setText("ΚΤΗΝΙΑΤΡΕΙΟ")
        self.ktiniatrio_btn.setStyleSheet("border-style: outset;"
                                          "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.ktiniatrio_btn.setToolTip("Κτηνιατρείο")
        self.ktiniatrio_btn.setStatusTip("Μηχανήματα που είναι στο κτηνιατρείο Φλώρινας")
        self.ktiniatrio_btn.setObjectName("ktiniatrio_btn")
        self.ktiniatrio_btn.clicked.connect(lambda: self.show_data(Κτηνιατρείο))
        self.gridLayout.addWidget(self.ktiniatrio_btn, 0, 6, 1, 1)

        # ---------------------- Κάτω εικονίδια ------------#
        # Πρωτοβάθμια
        self.protobathmia_btn = QtWidgets.QToolButton(self.centralwidget)
        self.protobathmia_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.protobathmia_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.protobathmia_btn.setSizePolicy(sizePolicy)
        self.protobathmia_btn.setFont(self.font_16_bold)
        self.protobathmia_btn.setText("ΠΡΩΤΟΒΑΘΜΙΑ")
        self.protobathmia_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                            "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.protobathmia_btn.setToolTip("Πρωτοβάθμια")
        self.protobathmia_btn.setStatusTip("Μηχανήματα που είναι στη Πρωτοβάθμια Φλώρινας")
        self.protobathmia_btn.setObjectName("protobathmia_btn")
        self.protobathmia_btn.clicked.connect(lambda: self.show_data(Πρωτοβάθμια))
        self.gridLayout.addWidget(self.protobathmia_btn, 1, 0, 1, 1)

        # Δευτεροβάθμια
        self.deyterobathmia_btn = QtWidgets.QToolButton(self.centralwidget)
        self.deyterobathmia_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.deyterobathmia_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.deyterobathmia_btn.setSizePolicy(sizePolicy)
        self.deyterobathmia_btn.setToolTip("μηχανήματα στην Δευτεροβάθμια")
        self.deyterobathmia_btn.setFont(self.font_16_bold)
        self.deyterobathmia_btn.setText("ΔΕΥΤΕΡΟΒΑΘΜΙΑ")
        self.deyterobathmia_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                              "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.deyterobathmia_btn.setStatusTip("Μηχανήματα που είναι στη Δευτεροβάθμια Φλώρινας")
        self.deyterobathmia_btn.setObjectName("deyterobathmia_btn")
        self.deyterobathmia_btn.clicked.connect(lambda: self.show_data(Δευτεροβάθμια))
        self.gridLayout.addWidget(self.deyterobathmia_btn, 1, 1, 1, 1)

        # ΚΤΕΟ
        self.kteo_btn = QtWidgets.QToolButton(self.centralwidget)
        self.kteo_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.kteo_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.kteo_btn.setSizePolicy(sizePolicy)
        self.kteo_btn.setToolTip("Μηχανήματα ΚΤΕΟ")
        self.kteo_btn.setFont(self.font_16_bold)
        self.kteo_btn.setText("ΚΤΕΟ")
        self.kteo_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                    "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.kteo_btn.setStatusTip("Μηχανήματα που είναι στο δημόσιο ΚΤΕΟ Φλώρινας")
        self.kteo_btn.setObjectName("kteo_btn")
        self.kteo_btn.clicked.connect(lambda: self.show_data(Κτέο))
        self.gridLayout.addWidget(self.kteo_btn, 1, 2, 1, 1)

        # Αμύνταιο
        self.amyntaio_btn = QtWidgets.QToolButton(self.centralwidget)
        self.amyntaio_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.amyntaio_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.amyntaio_btn.setSizePolicy(sizePolicy)
        self.amyntaio_btn.setText("ΑΜΥΝΤΑΙΟ")
        self.amyntaio_btn.setFont(self.font_16_bold)
        self.amyntaio_btn.setToolTip("Αμύνταιο")
        self.amyntaio_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                        "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                        "qproperty-iconSize: 100px")
        self.amyntaio_btn.setStatusTip("Μηχανήματα που είναι στο Αμύνταιο")
        self.amyntaio_btn.setObjectName("amyntaio_btn")
        self.amyntaio_btn.clicked.connect(lambda: self.show_data(Αμύνταιο))
        self.gridLayout.addWidget(self.amyntaio_btn, 1, 3, 1, 1)

        # ΚΕ.Δ.Α.Σ.Υ
        self.kedasy_btn = QtWidgets.QToolButton(self.centralwidget)
        self.kedasy_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.kedasy_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.kedasy_btn.setSizePolicy(sizePolicy)
        self.kedasy_btn.setToolTip("Μηχανήματα ΚΕ.Δ.Α.Σ.Υ")
        self.kedasy_btn.setStatusTip("Μηχανήματα που είναι στο ΚΕ.Δ.Α.Σ.Υ")
        self.kedasy_btn.setText("ΚΕ.Δ.Α.Σ.Υ")
        self.kedasy_btn.setFont(self.font_16_bold)
        self.kedasy_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.kedasy_btn.setObjectName("kedasy_btn")
        self.kedasy_btn.clicked.connect(lambda: self.show_data(Κεδασυ))
        self.gridLayout.addWidget(self.kedasy_btn, 1, 4, 1, 1)

        # Εκτός χρήσης μηχανήματα
        self.ektos_btn = QtWidgets.QToolButton(self.centralwidget)
        self.ektos_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ektos_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.ektos_btn.setSizePolicy(sizePolicy)
        self.ektos_btn.setToolTip("Μηχανήματα Εκτός χρήσης")
        self.ektos_btn.setFont(self.font_16_bold)
        self.ektos_btn.setText("ΕΚΤΟΣ\nΛΕΙΤΡΟΥΡΓΙΑΣ")
        self.ektos_btn.setStyleSheet("border-style: outset; " "background-color: #ffb907;"
                                     "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.ektos_btn.setStatusTip("Μηχανήματα που είναι εκτός χρήσης")
        self.ektos_btn.setObjectName("ektos_btn")
        self.ektos_btn.clicked.connect(lambda: self.show_data(Εκτός))
        self.gridLayout.addWidget(self.ektos_btn, 1, 5, 1, 1)

        # Ολα τα μηχανήματα
        self.all_machines_btn = QtWidgets.QToolButton(self.centralwidget)
        self.all_machines_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.all_machines_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.all_machines_btn.setSizePolicy(sizePolicy)
        self.all_machines_btn.setToolTip("Ολα τα μηχανήματα")
        self.all_machines_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                            "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.all_machines_btn.setText("ΟΛΑ ΤΑ \nΜΗΧΑΝΗΜΑΤΑ")
        self.all_machines_btn.setFont(self.font_16_bold)
        self.all_machines_btn.setStatusTip("Προβολή όλων των μηχανημάτων που τροφοδοτεί η περιφέρεια Φλώρινας")
        self.all_machines_btn.setObjectName("ektos_btn")
        self.all_machines_btn.clicked.connect(self.show_all_machines_data)
        self.gridLayout.addWidget(self.all_machines_btn, 1, 6, 1, 1)

        # Ετος
        self.year_label = QtWidgets.QLabel(self.centralwidget)
        self.year_label.setFont(self.font_14_bold)
        self.year_label.setText(f"Έτος")
        self.year_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.year_label, 3, 0, 1, 1)

        self.year_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.year_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.year_lineEdit.setObjectName("year_lineEdit")
        self.year_lineEdit.setFont(self.font_14)
        self.year_lineEdit.setReadOnly(True)

        self.year_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.year_combobox.setMinimumSize(QtCore.QSize(0, 30))
        self.year_combobox.setFont(self.font_14)
        self.year_combobox.setObjectName("year_combobox")
        self.year_combobox.setLineEdit(self.year_lineEdit)
        self.year_combobox.addItems(YEARS)
        self.year_combobox.currentIndexChanged.connect(self.change_year)
        self.gridLayout.addWidget(self.year_combobox, 4, 0, 1, 1)

        # Δικά μας μηχανήματα
        self.my_machines_btn = QtWidgets.QToolButton(self.centralwidget)
        self.my_machines_btn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.my_machines_btn.setMinimumSize(QtCore.QSize(180, 60))
        self.my_machines_btn.setSizePolicy(sizePolicy)
        self.my_machines_btn.setToolTip("Δικά μου μηχανήματα")
        self.my_machines_btn.setStyleSheet("border-style: outset;" "background-color: #ffb907;"
                                           "border-width: 2px;" "border-radius: 15px;" "border-color: black;")
        self.my_machines_btn.setText("ΔΙΚΑ ΜΟΥ \nΜΗΧΑΝΗΜΑΤΑ")
        self.my_machines_btn.setFont(self.font_16_bold)
        self.my_machines_btn.setStatusTip("Προβολή δικών μου μηχανημάτων")
        self.my_machines_btn.setObjectName("my_machines_btn")
        self.my_machines_btn.clicked.connect(self.show_my_machines)
        self.gridLayout.addWidget(self.my_machines_btn, 2, 1, 1, 1)

        # Συνολικός μετρητής
        self.total_prints_label = QtWidgets.QLabel(self.centralwidget)
        self.total_prints_label.setSizePolicy(sizePolicy)
        self.total_prints_label.setMaximumSize(QtCore.QSize(16777215, 40))
        if self.total_prints == "Σφάλμα":
            self.total_prints_label.setStyleSheet("color: red")
        try:
            self.total_prints_label.setText(
                f"Σύνολο εκτυπώσεων <b style='color: red;'>{self.selected_year}</b>: {self.total_prints:n} Σελ.")
        except Exception as error:
            self.total_prints_label.setText(f"Σύνολο εκτυπώσεων {self.selected_year}: {self.total_prints} Σελ.")
            QtWidgets.QMessageBox.warning(None, "Προειδοποίηση", f'Κάποιο μηχάνημα δεν έχει σωστό σύνολο\n {error}')

        self.total_prints_label.setToolTip(f"Συνολικός μετρητής")
        self.total_prints_label.setStatusTip("Συνολικές εκτυπώσεις απ'όλα τα μηχανήματα")
        self.total_prints_label.setWhatsThis("Σύνολο εκτυπώσεων που έχουν κάνει όλα τα μηχανήματα")
        self.total_prints_label.setFont(self.font_20_bold)
        self.total_prints_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.total_prints_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.total_prints_label.setObjectName("total_prints_label")
        self.gridLayout.addWidget(self.total_prints_label, 2, 2, 1, 3)

        self.refresh_btn = QtWidgets.QToolButton(self.centralwidget)
        self.refresh_btn.setToolTip("Ανανέωση συνολικών εκτυπώσεων")
        self.refresh_btn.setStatusTip("Κουμπί ανανέωσης συνολικών εκτυπώσεων")
        self.refresh_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.refresh_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.refresh_btn.setSizePolicy(sizePolicy)
        self.refresh_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.refresh_btn.setStyleSheet("border-style: outset;"
                                       "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                       "qproperty-iconSize: 40px")
        self.refresh_btn.setIcon(self.refresh_icon)
        self.refresh_btn.setIconSize(QtCore.QSize(40, 40))
        self.refresh_btn.setObjectName("refresh_btn")
        self.refresh_btn.clicked.connect(lambda: self.refresh_counter())
        self.gridLayout.addWidget(self.refresh_btn, 2, 5, 1, 1, QtCore.Qt.AlignLeft)

        # Αναζήτηση αριθμού
        self.search_number_label = QtWidgets.QLabel(self.centralwidget)
        self.search_number_label.setSizePolicy(sizePolicy)
        self.search_number_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.search_number_label.setMinimumSize(QtCore.QSize(180, 40))
        self.search_number_label.setFont(self.font_14_bold)
        self.search_number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.search_number_label.setObjectName("search_number_label")
        self.gridLayout.addWidget(self.search_number_label, 3, 2, 1, 1)
        self.search_number_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_number_lineEdit.setSizePolicy(sizePolicy)
        self.search_number_lineEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.search_number_lineEdit.setMinimumSize(QtCore.QSize(180, 40))
        self.search_number_lineEdit.setFont(self.font_12)
        self.search_number_lineEdit.setToolTip("Αναζήτηση με κωδικό συσκευής")
        self.search_number_lineEdit.setStatusTip(
            "Εύρεση μηχανήματος με αναζήτηση κωδικού συσκευής στον επιλεγμένο πίνακα")
        self.search_number_lineEdit.setObjectName("search_number_lineEdit")
        self.search_number_lineEdit.returnPressed.connect(self.search_code_by_table)
        self.gridLayout.addWidget(self.search_number_lineEdit, 4, 2, 1, 1)

        self.search_number_btn = QtWidgets.QToolButton(self.centralwidget)
        self.search_number_btn.setToolTip("Κουμπί αναζήτησης κωδικού")
        self.search_number_btn.setStatusTip("Κουμπί αναζήτησης κωδικού μηχανήματος στον επιλεγμένο πίνακα")
        self.search_number_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.search_number_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.search_number_btn.setSizePolicy(sizePolicy)
        self.search_number_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_number_btn.setStyleSheet("border-style: outset;"
                                             "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                             "qproperty-iconSize: 40px")
        self.search_number_btn.setIcon(self.search_icon)
        self.search_number_btn.setIconSize(QtCore.QSize(40, 40))
        self.search_number_btn.setObjectName("search_number_btn")
        self.search_number_btn.clicked.connect(self.search_code_by_table)
        self.gridLayout.addWidget(self.search_number_btn, 4, 3, 1, 1)

        # Αναζήτηση
        self.search_label = QtWidgets.QLabel(self.centralwidget)
        self.search_label.setFont(self.font_14_bold)
        self.search_label.setSizePolicy(sizePolicy)
        self.search_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.search_label.setMinimumSize(QtCore.QSize(180, 40))
        self.search_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.search_label.setObjectName("search_label")
        self.gridLayout.addWidget(self.search_label, 3, 4, 1, 1)
        self.search_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_lineEdit.setFont(self.font_12)
        self.search_lineEdit.setSizePolicy(sizePolicy)
        self.search_lineEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.search_lineEdit.setMinimumSize(QtCore.QSize(180, 40))
        self.search_lineEdit.setToolTip("Απλή αναζήτηση μηχανήματος")
        self.search_lineEdit.setStatusTip(
            "Εύρεση μηχανήματος με αναζήτηση οποιουδήποτε στοιχείου στον επιλεγμένο πίνακα")
        self.search_lineEdit.setObjectName("search_lineEdit")
        self.search_lineEdit.returnPressed.connect(self.search_by_table)
        self.gridLayout.addWidget(self.search_lineEdit, 4, 4, 1, 1)
        self.search_btn = QtWidgets.QToolButton(self.centralwidget)
        self.search_btn.setToolTip("Κουμπί απλής αναζήτησης")
        self.search_btn.setStatusTip("Κουμπί αναζήτησης μηχανήματος με οποιουδήποτε στοιχείου στον επιλεγμένο πίνακα")
        self.search_btn.setSizePolicy(sizePolicy)
        self.search_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.search_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.search_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_btn.setStyleSheet("border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "qproperty-iconSize: 40px")
        self.search_btn.setIcon(self.search_icon)
        self.search_btn.setIconSize(QtCore.QSize(40, 40))
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(self.search_by_table)
        self.gridLayout.addWidget(self.search_btn, 4, 5, 1, 1)

        # Σύνολο υπηρεσίας
        self.total_ypiresias_label = QtWidgets.QLabel(self.centralwidget)
        self.total_ypiresias_label.setFont(self.font_14_bold)
        self.total_ypiresias_label.setSizePolicy(sizePolicy)
        self.total_ypiresias_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.total_ypiresias_label.setMinimumSize(QtCore.QSize(180, 40))
        self.total_ypiresias_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.total_ypiresias_label.setObjectName("total_ypiresias_label")
        self.total_ypiresias_label.setText("Σύνολο υπηρεσίας")
        self.gridLayout.addWidget(self.total_ypiresias_label, 3, 6, 1, 1)
        self.total_ypiresias_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.total_ypiresias_lineEdit.setFont(self.font_14_bold)
        self.total_ypiresias_lineEdit.setSizePolicy(sizePolicy)
        self.total_ypiresias_lineEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.total_ypiresias_lineEdit.setMinimumSize(QtCore.QSize(180, 40))
        self.total_ypiresias_lineEdit.setToolTip("Σύνολο εκτυπώσεων υπηρεσίας")
        self.total_ypiresias_lineEdit.setStatusTip(
            "Συνολικός μετρητής εκτυπώσεων υπηρεσίας")
        self.search_lineEdit.setObjectName("total_ypiresias_lineEdit")
        self.total_ypiresias_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.total_ypiresias_lineEdit, 4, 6, 1, 1)

        # treeWidget
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setToolTip("")
        self.treeWidget.setStatusTip("")
        self.treeWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setLineWidth(14)
        self.treeWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.treeWidget.setTabKeyNavigation(True)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderLabels(
            ["ID", "Κωδικός", "Όροφος", "Γραφείο", "Τύπος", "Μηχάνημα", "Serial", "Αρχικός", "Τελικός", "Σύνολο",
             "Χρέωση"])
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: black;"
                                               "font-style: normal;font-size: 12pt;font-weight: bold;")
        self.treeWidget.header().setDefaultSectionSize(150)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setMinimumSectionSize(50)
        self.treeWidget.header().setStretchLastSection(True)
        self.treeWidget.setFont(self.font_12)
        self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
        self.treeWidget.setColumnWidth(0, 20)
        self.treeWidget.setColumnWidth(1, 120)
        self.treeWidget.setColumnWidth(2, 135)
        self.treeWidget.setColumnWidth(3, 350)
        self.treeWidget.setColumnWidth(5, 200)
        self.treeWidget.itemDoubleClicked.connect(self.show_edit_window)
        self.gridLayout.addWidget(self.treeWidget, 5, 0, 1, 8)
        # ------------------------Menu---------------------------#
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 28))
        self.menubar.setFont(self.font_14)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuBackup = QtWidgets.QMenu(self.menubar)
        self.menuBackup.setFont(self.font_14)
        self.menuBackup.setObjectName("menuBackup")
        self.menuInfo = QtWidgets.QMenu(self.menubar)
        self.menuInfo.setFont(self.font_14)
        self.menuInfo.setObjectName("menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setFont(self.font_14)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setFont(self.font_14)
        self.action.setObjectName("action")
        self.action_F1 = QtWidgets.QAction(MainWindow)
        self.action_F1.setFont(self.font_14)
        self.action_F1.setObjectName("action_F1")
        self.action_F1.triggered.connect(self.show_add_window)
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setFont(self.font_14)
        self.action_3.setObjectName("action_3")
        self.action_3.triggered.connect(self.delete_selected_item)
        self.action_Esc = QtWidgets.QAction(MainWindow)
        self.action_Esc.setFont(self.font_14)
        self.action_Esc.setObjectName("action_Esc")
        self.action_Esc.triggered.connect(self.quit)
        self.actionBackup_Database = QtWidgets.QAction(MainWindow)
        self.actionBackup_Database.setFont(self.font_14)
        self.actionBackup_Database.setObjectName("actionBackup_Database")
        self.actionBackup_Database.triggered.connect(backup)
        self.action_Excel = QtWidgets.QAction(MainWindow)
        self.action_Excel.setFont(self.font_14)
        self.action_Excel.setObjectName("action_Excel")
        self.action_Excel.triggered.connect(to_excel)
        self.action_create_year = QtWidgets.QAction(MainWindow)
        self.action_create_year.setFont(self.font_14)
        self.action_create_year.setObjectName("action_create_year")
        self.action_create_year.triggered.connect(create_year)
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setFont(self.font_14)
        self.action_4.setObjectName("action_4")
        self.action_4.triggered.connect(self.info)
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_F1)
        self.menu.addSeparator()
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_Esc)
        self.menuBackup.addAction(self.actionBackup_Database)
        self.menuBackup.addAction(self.action_Excel)
        self.menuBackup.addAction(self.action_create_year)
        self.menuInfo.addAction(self.action_4)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuBackup.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        MainWindow.setCentralWidget(self.centralwidget)
        self.grouping_btn()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.search_label.setText(_translate("MainWindow", "Αναζήτηση"))
        self.search_number_label.setText(_translate("MainWindow", "Αναζήτηση κωδικού"))
        self.menu.setTitle(_translate("MainWindow", "Αρχείο"))
        self.menuBackup.setTitle(_translate("MainWindow", "Backup"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        self.action.setText(_translate("MainWindow", "Ανοιγμα αρχείου"))
        self.action_F1.setText(_translate("MainWindow", "Προσθήκη  F1"))
        self.action_3.setText(_translate("MainWindow", "Διαγραφή"))
        self.action_Esc.setText(_translate("MainWindow", "Εξοδος  Esc"))
        self.actionBackup_Database.setText(_translate("MainWindow", "Backup Database"))
        self.action_Excel.setText(_translate("MainWindow", "Εξαγωγή Excel"))
        self.action_create_year.setText(_translate("MainWindow", f"Δημιουργία νέας χρονιάς {int(today_obj.year) + 1}"))
        self.action_4.setText(_translate("MainWindow", "Πληροφορίες"))

    # Έξοδος
    def quit(self, *args):
        answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Σίγουρα θέλετε να κλείσετε τo πρόγραμμα;",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            # self.close()
            sys.exit(app.exec_())
        else:
            return

    # Ομαδοποίηση κουμπιών για την αλλαγή χρωμάτων
    def grouping_btn(self):

        up_btn = [self.flor_1_btn, self.flor_2_btn, self.flor_4_btn, self.flor_5_btn, self.flor_6_btn, self.pasias_btn,
                  self.ktiniatrio_btn]
        down_btn = [self.protobathmia_btn, self.deyterobathmia_btn, self.kteo_btn, self.amyntaio_btn, self.ektos_btn,
                    self.all_machines_btn, self.kedasy_btn, self.my_machines_btn]
        self.all_btn = up_btn + down_btn
        # Grouping buttons
        self.btn_grp = QtWidgets.QButtonGroup()
        self.btn_grp.setExclusive(True)
        for btn in self.all_btn:
            self.btn_grp.addButton(btn)

    # αλλαγή χρωμάτων
    def change_colors_of_pressed_btn(self, pressed_btn):
        up_btn = [self.flor_1_btn, self.flor_2_btn, self.flor_4_btn, self.flor_5_btn, self.flor_6_btn, self.pasias_btn,
                  self.ktiniatrio_btn]
        down_btn = [self.protobathmia_btn, self.deyterobathmia_btn, self.kteo_btn, self.amyntaio_btn, self.ektos_btn,
                    self.all_machines_btn, self.kedasy_btn, self.my_machines_btn]
        self.all_btn = up_btn + down_btn

        pressed_btn.setStyleSheet(
            f"background-color: #50f333;" "color: black;"
            "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;" "padding: 4px;")
        for btn in self.all_btn:
            if btn in up_btn and btn != pressed_btn:
                btn.setStyleSheet(
                    f"background-color: #fff;" "color: black;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")
            elif btn in down_btn and btn != pressed_btn:
                btn.setStyleSheet(
                    f"background-color: #ffb907;" "color: black;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")

    # Εμφάνιση δεδομένων επιλεγμένου πίνακα
    def show_data(self, table):
        self.selected_table = table
        self.my_table = False
        self.all_machines = False
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.treeWidget.clear()
        self.data_to_show = fetch_clicked_table_data(table)
        self.total_ypiresias = 0
        self.total_ypiresias_label.show()
        self.total_ypiresias_lineEdit.show()
        for index, item in enumerate(self.data_to_show):
            try:
                self.qitem = TreeWidgetItem(self.treeWidget,
                                            [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                             item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                             str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                self.total_ypiresias += item.σύνολο
            except Exception as error:
                self.qitem = TreeWidgetItem(self.treeWidget,
                                            [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                             item.μοντέλο, item.serial, str(item.αρχικός),
                                             str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                self.total_ypiresias = "Σφάλμα"
                self.total_prints_label.setText(f"Σύνολο εκτυπώσεων: Σφάλμα")
                self.total_prints_label.setStyleSheet("color: red ")
                self.total_ypiresias_lineEdit.setText(str(f"{self.total_ypiresias}"))
                QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                              f'show_data Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')

                return
            # self.treeWidget.resizeColumnToContents(index)
        self.total_ypiresias_lineEdit.setText(str(f"{self.total_ypiresias:n}"))

    # εμφάνιση δεδομένων όλων το μηχανημάτων ΠΡΟΣΟΧΗ δεν είναι πίνακας
    def show_all_machines_data(self):
        self.selected_table = None
        self.my_table = False
        self.all_machines = True
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.treeWidget.clear()
        self.all_data = fetch_all_table_data()  # επιστρέφει [[,],] λίστες μέσα σε λίστα
        self.total_ypiresias = 0
        self.total_ypiresias_label.hide()
        self.total_ypiresias_lineEdit.hide()
        for data in self.all_data:
            for index, item in enumerate(data):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                                 item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"),
                                                 str(f"{item.τελικός - item.αρχικός:n}"), str(item.χρέωση)])
                except ValueError as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                                 item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')
                # self.treeWidget.resizeColumnToContents(index)

        # self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    # ανανέωση τελικού μετρητή
    def refresh_counter(self):
        self.total_prints = 0
        self.total_prints = get_total_counter()
        try:
            self.total_prints_label.setText(
                f"Σύνολο εκτυπώσεων <b style='color: red;'>{self.selected_year}</b>: {self.total_prints:n} Σελ.")
            self.total_prints_label.setStyleSheet("color: black")
        except Exception as error:
            self.total_prints_label.setText(f"Σύνολο εκτυπώσεων: Σφάλμα")
            self.total_prints_label.setStyleSheet("color: red ")
            QtWidgets.QMessageBox.warning(None, "Προειδοποίηση", f'Κάποιο μηχάνημα δεν έχει σωστό σύνολο\n {error}')

    # εμφάνιση παράθυρου επεξεργασίας αντικειμένου
    def show_edit_window(self, item=None, column=None):
        global SESSION, BASE_DIR
        selected_item_id = item.text(0)  # Όταν πατάμε διπλό click στα μηχανήματα
        selected_item_serial = item.text(6)

        # Αν δεν υπάρχει edit_task_window ή αν ο χρήστης έχει κλείσει το παράθυρο απο το Χ πάνω δεξιά
        # ελέγχουμε αν είναι ορατό
        if self.edit_window is None or not self.edit_window.isVisible():
            self.edit_window = QtWidgets.QWidget()
            self.edit_item = Edit_Ui_Form_Window()
            self.edit_item.selected_item_id = selected_item_id
            self.edit_item.setupUi(self.edit_window)
            self.edit_item.window = self.edit_window

            if self.selected_table is None:  # Όταν είναι απο όλα τα μηχανήματα ο πίνακας είναι None
                self.edit_item.get_data_from_serial(selected_item_id, selected_item_serial, self.edit_window)
                self.edit_item.session = SESSION
                self.edit_item.BASE_DIR = BASE_DIR
                self.edit_item.show_file()
                self.edit_window.show()
                self.edit_item.window_closed.connect(lambda: (self.closed_first_edit_window(), self.refresh_counter()))
                return
            else:
                self.edit_item.get_data(self.selected_table, selected_item_id)
                self.edit_item.selected_table = self.selected_table
                self.edit_window.setWindowTitle(
                    f"Παράθυρο επεξεργασίας πίνακα {self.selected_table.__tablename__}")
                self.edit_item.window_closed.connect(lambda: (self.closed_first_edit_window(), self.refresh_counter()))
                self.edit_item.session = SESSION
                self.edit_item.BASE_DIR = BASE_DIR
                self.edit_item.show_file()
                self.edit_window.show()
                return

        else:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ κλείστε το ανοιχτά παράθυρα "
                                                            f"επεξεργασίας μηχανήματος.")
            return

    def closed_first_edit_window(self, all_data=None):
        if self.my_table:
            self.show_my_machines()
        elif self.all_machines:
            self.show_all_machines_data()
        else:
            self.show_data(self.selected_table)

        self.edit_window.close()

    def close_add_window(self):
        self.show_data(self.selected_table)
        self.add_window.close()

    # εμφάνιση μόνο τον δικό μου μηχανημάτων ΔΕΝ ΕΙΝΑΙ ΠΙΝΑΚΑΣ
    def show_my_machines(self):
        self.selected_table = None
        self.my_table = True
        self.all_machines = False
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        # treeWidget
        self.treeWidget.clear()
        self.all_data = get_my_machines()
        self.total_ypiresias = 0
        self.total_ypiresias_label.hide()
        self.total_ypiresias_lineEdit.hide()
        for item in self.all_data:
            try:
                self.qitem = TreeWidgetItem(self.treeWidget,
                                            [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                             item.τύπος,
                                             item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                             str(f"{item.τελικός:n}"),
                                             str(f"{item.τελικός - item.αρχικός:n}"), str(item.χρέωση)])
            except ValueError as error:
                self.qitem = TreeWidgetItem(self.treeWidget,
                                            [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                             item.τύπος,
                                             item.μοντέλο, item.serial, str(item.αρχικός),
                                             str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                              f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')

    def delete_selected_item(self):
        if self.selected_table is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                          f"Πρέπει πρώτα να επιλέξετε πίνακα!\nΔεν μπορείτε να σβήσετε"
                                          f" απο το κουμπί ΔΙΚΑ ΜΟΥ και ΟΛΛΑ ΤΑ ΜΗΧΑΝΗΜΑΤΑ")
            return
        elif self.treeWidget.currentItem() is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ επιλέξτε πρώτα αντικείμενο!")
            return
        else:
            item = self.treeWidget.selectedItems()
            item_id = item[0].text(0)  # item[0].text(0) ==> ID  item[0].text(5) ==> serial απο το treewidget
            answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                   f"Σίγουρα θέλετε να διαγράψετε το μηχάνημα:\n"
                                                   f"{item[0].text(4)} {item[0].text(5)}\n"
                                                   f"S/N: {item[0].text(6)}\n"
                                                   f"απο τον πίνακα {self.selected_table.__tablename__};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                       f"Μη την διαγραφή του μηχανήματος θα αφαιρεθούν απο τον\n"
                                                       f"συνολικό μετρητή {item[0].text(9)} σελίδες",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:
                    item_to_delete = SESSION.query(self.selected_table).get(item_id)
                    SESSION.delete(item_to_delete)
                    SESSION.commit()
                    QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"Το μηχάνημα {item[0].text(5)}\n"
                                                                          f" διαγράφηκε!"
                                                                          f"\nΑπο τον πίνακα {self.selected_table.__tablename__}")
            self.show_data(self.selected_table)

    # Αναζήτηση σε πίνακα
    def search_by_table(self):
        text_to_search = self.search_lineEdit.text()
        if text_to_search == "" or text_to_search == " ":
            if self.selected_table is not None:
                self.show_data(self.selected_table)
            elif self.my_table:
                self.show_my_machines()
            else:
                self.show_all_machines_data()
            return
        if self.selected_table is not None:  # αν έχουμε επιλέξει πίνακα
            self.my_table = False
            self.all_machines = False
            self.search_lineEdit.clear()
            self.treeWidget.clear()
            self.data_to_show = search_in_table(self.selected_table, text_to_search)
            for index, item in enumerate(self.data_to_show):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                except Exception as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')
        # Αναζήτηση στα μηχανήματα μου
        elif self.selected_table is None and self.my_table:
            self.all_machines = False
            self.treeWidget.clear()
            self.search_lineEdit.clear()
            self.data_to_show = search_in_my_machines(text_to_search)
            for index, item in enumerate(self.data_to_show):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                except Exception as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\nERROR: {error}')

        elif self.selected_table is None and self.all_machines:
            self.treeWidget.clear()
            self.search_lineEdit.clear()
            self.data_to_show = search_in_all_tables(text_to_search)  # data_to_show έχει τη μορφή [[κάτι, δεύτερο],
            # [τρίτο,τέταρτο],[πέμπτο]]
            for index in range(len(self.data_to_show)):
                for index, item in enumerate(self.data_to_show[index]):
                    try:
                        self.qitem = TreeWidgetItem(self.treeWidget,
                                                    [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                                     item.τύπος,
                                                     item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                     str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"),
                                                     str(item.χρέωση)])
                    except Exception as error:
                        self.qitem = TreeWidgetItem(self.treeWidget,
                                                    [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο,
                                                     item.τύπος,
                                                     item.μοντέλο, item.serial, str(item.αρχικός),
                                                     str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                        QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                      f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\nERROR: {error}')

    def search_code_by_table(self):
        text_to_search = self.search_number_lineEdit.text()
        if text_to_search == "" or text_to_search == " ":
            if self.selected_table is not None:
                self.show_data(self.selected_table)
            elif self.my_table:
                self.show_my_machines()
            else:
                self.show_all_machines_data()
            return
        if self.selected_table is not None:
            self.search_number_lineEdit.clear()
            self.treeWidget.clear()
            self.data_to_show = search_code_in_table(self.selected_table, text_to_search)
            for index, item in enumerate(self.data_to_show):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                except Exception as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')

        elif self.selected_table is None and self.my_table:
            self.search_number_lineEdit.clear()
            self.data_to_show = search_code_in_my_machines(text_to_search)
            self.treeWidget.clear()
            for index, item in enumerate(self.data_to_show):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                except Exception as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')
        elif self.selected_table is None and self.all_machines:
            self.search_number_lineEdit.clear()
            self.data_to_show = search_code_in_all_machines(text_to_search)
            self.treeWidget.clear()
            for index, item in enumerate(self.data_to_show):
                try:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(f"{item.αρχικός:n}"),
                                                 str(f"{item.τελικός:n}"), str(f"{item.σύνολο:n}"), str(item.χρέωση)])
                except Exception as error:
                    self.qitem = TreeWidgetItem(self.treeWidget,
                                                [str(item.ID), item.κωδικός, str(item.όροφος), item.γραφείο, item.τύπος,
                                                 item.μοντέλο, item.serial, str(item.αρχικός),
                                                 str(item.τελικός), str(item.σύνολο), str(item.χρέωση)])
                    QtWidgets.QMessageBox.warning(None, "Προειδοποίηση",
                                                  f'Το μηχάνημα με S/N: {item.serial} δεν έχει σωστά δεδομένα\n {error}')

    def show_add_window(self):
        if self.selected_table is None:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Θα πρέπει να επιλέξετε πίνακα\n"
                                                            "Το κουμπί ΔΙΚΑ ΜΟΥ και ΟΛΛΑ ΤΑ ΜΗΧΑΝΗΜΑΤΑ δεν είναι "
                                                            "πίνακας")
            return
        if self.selected_table == Εκτός:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Δεν μπορείτε να προσθέτεται νέο μηχάνημα στα μή ενεργά "
                                                            "μηχανήματα")
            return
        # Αν δεν υπάρχει edit_task_window ή αν ο χρήστης έχει κλείσει το παράθυρο απο το Χ πάνω δεξιά
        # ελέγχουμε αν είναι ορατό
        if self.add_window is None or not self.add_window.isVisible():
            self.add_window = QtWidgets.QWidget()
            self.add_item = Edit_Ui_Form_Window()
            self.add_item.selected_item_id = None
            self.add_item.setupUi(self.add_window)
            self.add_item.selected_table = self.selected_table
            self.add_item.window = self.add_window
            self.add_window.setWindowTitle(
                f"Παράθυρο εισαγωγής μηχανήματος στον πίνακα {self.selected_table.__tablename__}")
            self.add_item.window_closed.connect(lambda: (self.close_add_window(), self.refresh_counter()))
            self.add_item.create_machine()
            self.add_window.show()
            self.add_item.right_frame.hide()
            self.add_item.transport_btn.hide()
            return
        else:
            QtWidgets.QMessageBox.warning(None, "Προσοχή", "Δεν επιτρέπεται να εισάγετε πολλά μηχανήματα ταυτόχρονα!\n"
                                                           "Παρακαλώ κλείστε το παράθυρο εισαγωγής μηχανήματος.")

    def info(self):
        QtWidgets.QMessageBox.about(None, 'Σχετικά',
                                    f"""Author     : Jordanis Ntini<br>
                                    Copyright  : Copyright © 2023<br>
                                    Credits    : ['Athanasia Tzampazi']<br>
                                    Version    : '{VERSION}'<br>
                                    Maintainer : Jordanis Ntini<br>
                                    Email      : ntinisiordanis@gmail.com<br>
                                    Status     : Development<br>
                                    Language   : <a href='https://www.python.org/'>Python</a><br>
                                    Gui        : <a href='https://pypi.org/project/PyQt5/'>PyQt5</a><br>
                                    License    : GPL V3 <a href='https://www.gnu.org/licenses/gpl-3.0.txt'>GNU GENERAL PUBLIC LICENSE</a>""")

    def change_year(self):
        global BASE_PATH, DBASE, SESSION, ENGINE, BASE, CONN, BASE_DIR, db
        self.treeWidget.clear()
        self.selected_year = self.year_lineEdit.text()

        MainWindow.setWindowTitle(f"Μηχανήματα Περιφέρειας Φλώρινας {VERSION}  {self.selected_year}")

        BASE_PATH = f"\\\\192.168.1.200\\Public\\GOOGLE-DRIVE\\ΕΓΓΡΑΦΑ\\--- ΠΕΡΙΦΕΡΕΙΑ ΦΛΩΡΙΝΑΣ\\1. MHXANHMATA\\{self.selected_year}"

        DBASE = os.path.join(BASE_PATH, "Μηχανήματα.db")
        BASE_DIR = os.path.join(BASE_PATH, "ΑΡΧΕΙΑ")
        ENGINE = create_engine(f"sqlite:///{DBASE}")
        SESSION = sessionmaker(bind=ENGINE)()
        BASE = declarative_base()
        # conn = session.bind
        CONN = ENGINE.connect()

        # Ενημέρωση του αρχείου db
        db.dbase = DBASE
        db.engine = ENGINE
        db.session = SESSION
        db.conn = CONN
        try:
            db.session.close_all_sessions()
        except AttributeError:
            pass
        self.refresh_counter()


def backup():
    global DBASE
    filename = os.path.basename(DBASE)
    file_without_extension = os.path.splitext(filename)
    extension = pathlib.Path(filename).suffix
    today_str = today.replace('/', '_')
    try:
        #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
        file_to_save = QtWidgets.QFileDialog.getSaveFileName(None, 'Αποθήκευση αρχείου',
                                                             f'backup_{file_without_extension[0]}_'
                                                             + f"{today_str}" + f'{extension}')

        if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήσει άκυρο ο χρήστης
            return

        shutil.copy(os.path.abspath(DBASE), file_to_save[0], follow_symlinks=False)
        QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχείο {file_to_save[0]} αποθηκεύτηκε επιτυχώς')
    except TypeError:  # Αν δεν πατήσει αποθήκευση
        return


def to_excel():
    global DBASE
    needed_tables = tables
    data_frames = []

    filename = os.path.basename(DBASE)
    file_without_extension = os.path.splitext(filename)
    today_str = today.replace('/', '-')
    # try:
    #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
    file_to_save = QtWidgets.QFileDialog.getSaveFileName(None, 'Αποθήκευση αρχείου',
                                                         f'{file_without_extension[0]}'
                                                         + f"_{today_str}" + '.xlsx')
    if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήσει άκυρο ο χρήστης
        return
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_to_save[0], engine="xlsxwriter")
    for table in needed_tables:
        df_query = select(table)
        df_data = pd.read_sql(df_query, con=conn)
        df_data.to_excel(writer, sheet_name=table.__tablename__, index=False)
    writer.save()
    QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {file_to_save[0]} αποθηκεύτηκε '
                                                        f'επιτυχώς')
    os.startfile(file_to_save[0])
    return


def create_year():
    global YEARS, today_obj, YEARS_PATH
    try:
        last_year = sorted(YEARS, reverse=True)[0]
        next_year_to_create = int(last_year) + 1
        next_year_dir = os.path.join(YEARS_PATH, str(next_year_to_create))
        if not os.path.exists(next_year_dir):
            os.makedirs(next_year_dir)
            machines_file = os.path.join(BASE_PATH, f"1. ΜΗΧΑΝΗΜΑΤΑ {today_obj.year}.xlsx")
            new_machines_file_destination = os.path.join(next_year_dir, f"1. ΜΗΧΑΝΗΜΑΤΑ {next_year_to_create}.xlsx")
            new_dbase_file_destination = os.path.join(next_year_dir, "Μηχανήματα.db")

            shutil.copy(os.path.abspath(DBASE), new_dbase_file_destination, follow_symlinks=False)
            shutil.copy(os.path.abspath(machines_file), new_machines_file_destination, follow_symlinks=False)
            # Μεταφορά τελικών εκτυπώσεων στις αρχικές εκτυπώσεις για να έχει σύνολο 0
            all_data = []
            # Νεο session για ασφάλεια
            new_engine = create_engine(f"sqlite:///{new_dbase_file_destination}")
            new_session = sessionmaker(bind=new_engine)()
            new_base = declarative_base()
            new_conn = new_engine.connect()
            for table in tables:
                data = new_session.query(table).all()
                for item in data:
                    item.αρχικός = item.τελικός
                    item.σύνολο = 0
                    item.ημερ_αρχι = item.ημερο_τελικ
                    item.ημερο_τελικ = " "

            new_session.commit()
            new_session.close()
            QtWidgets.QMessageBox.information(None, "Προσοχή", f"Ο φάκελος {next_year_to_create} δημιουργήθηκε\n"
                                                               f"Παρακαλώ ξεκινήστε το πρόγραμμα απο την αρχή")

        else:
            QtWidgets.QMessageBox.warning(None, "Προσοχή", f"Ο φάκελος {next_year_to_create} υπάρχει")
    except Exception as error:
        print(f"Error create_year() {error}")
        QtWidgets.QMessageBox.critical(None, "ΣΦΆΛΜΑ", f"{error}")
        traceback.print_exc()
        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
