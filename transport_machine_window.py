# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transport_machine_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import traceback
from settings import VERSION, root_logger
from db import tables, get_offices_from_table, Εκτός
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import db
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_Transport_Machine_Window(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()  # Το Signal πρέπει να είναι εκτός __init__ δε δουλεύει αλλιώς

    def __init__(self):
        super(Ui_Transport_Machine_Window, self).__init__()
        self.selected_machine = None
        self.tables = tables
        try:
            self.tables.remove(Εκτός)
        except ValueError:  # ValueError: list.remove(x): x not in list
            pass
        self.selected_machine_table = None
        self.all_tables = [table.__tablename__.upper() for table in self.tables]
        self.new_table = None
        self.selected_table_offices = None

    def setupUi(self, Transport_Machine_Window):
        Transport_Machine_Window.setObjectName("Form")
        Transport_Machine_Window.resize(602, 278)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/transport_copier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Transport_Machine_Window.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Transport_Machine_Window)
        self.gridLayout.setObjectName("gridLayout")
        self.transport_machine_label = QtWidgets.QLabel(Transport_Machine_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.transport_machine_label.setFont(font)
        self.transport_machine_label.setStyleSheet("background-color: rgb(170, 0, 0);\n"
                                                   "color: rgb(255, 255, 255);")
        self.transport_machine_label.setAlignment(QtCore.Qt.AlignCenter)
        self.transport_machine_label.setObjectName("transport_machine_label")
        self.gridLayout.addWidget(self.transport_machine_label, 0, 0, 1, 1)
        self.select_ypiresia_label = QtWidgets.QLabel(Transport_Machine_Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_ypiresia_label.sizePolicy().hasHeightForWidth())
        self.select_ypiresia_label.setSizePolicy(sizePolicy)
        self.select_ypiresia_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.select_ypiresia_label.setFont(font)
        self.select_ypiresia_label.setAlignment(QtCore.Qt.AlignCenter)
        self.select_ypiresia_label.setObjectName("select_ypiresia_label")
        self.gridLayout.addWidget(self.select_ypiresia_label, 1, 0, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        # New customer combobox
        self.new_ypiresia_lineEdit = QtWidgets.QLineEdit(Transport_Machine_Window)
        self.new_ypiresia_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.new_ypiresia_lineEdit.setObjectName("new_ypiresia_lineEdit")
        self.new_ypiresia_lineEdit.setFont(font)
        self.new_ypiresia_lineEdit.setReadOnly(True)
        self.ypiresia_completer = QtWidgets.QCompleter()
        self.ypiresia_completer.popup().setFont(font)
        self.new_ypiresia_lineEdit.setCompleter(self.ypiresia_completer)

        self.new_ypiresia_combobox = QtWidgets.QComboBox(Transport_Machine_Window)
        self.new_ypiresia_combobox.setMinimumSize(QtCore.QSize(0, 30))
        self.new_ypiresia_combobox.setFont(font)
        self.new_ypiresia_combobox.setObjectName("new_ypiresia_combobox")
        self.new_ypiresia_combobox.setLineEdit(self.new_ypiresia_lineEdit)
        self.new_ypiresia_combobox.addItems(self.all_tables)
        self.new_ypiresia_combobox.currentIndexChanged.connect(self.get_offices)
        self.gridLayout.addWidget(self.new_ypiresia_combobox, 2, 0, 1, 1)

        self.office_label = QtWidgets.QLabel(Transport_Machine_Window)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.office_label.setFont(font)
        self.office_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.office_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.office_label.setStyleSheet("background-color: rgb(89, 89, 89);\n"
                                        "color: rgb(255, 255, 255);")
        self.office_label.setLocale(QtCore.QLocale(QtCore.QLocale.Greek, QtCore.QLocale.Greece))
        self.office_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.office_label.setAlignment(QtCore.Qt.AlignCenter)
        self.office_label.setObjectName("copier_notes_label")
        self.gridLayout.addWidget(self.office_label, 3, 0, 1, 1)

        self.office_lineEdit = QtWidgets.QLineEdit(Transport_Machine_Window)
        self.office_lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.office_lineEdit.setObjectName("office_lineEdit")
        self.office_lineEdit.setFont(font)

        self.office_combobox = QtWidgets.QComboBox(Transport_Machine_Window)
        self.selected_table_offices = get_offices_from_table(self.selected_machine_table)
        self.office_combobox.addItems(self.selected_table_offices)
        self.office_combobox.setMinimumSize(QtCore.QSize(0, 30))
        self.office_combobox.setFont(font)
        self.office_combobox.setObjectName("office_combobox")
        self.office_combobox.setLineEdit(self.office_lineEdit)
        self.gridLayout.addWidget(self.office_combobox, 4, 0, 1, 1)

        self.transport_machine_toolButton = QtWidgets.QToolButton(Transport_Machine_Window)
        self.transport_machine_toolButton.setMinimumSize(QtCore.QSize(0, 50))
        self.transport_machine_toolButton.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.transport_machine_toolButton.setFont(font)
        self.transport_machine_toolButton.setStyleSheet("background-color: rgb(104, 104, 104);\n"
                                                        "color: rgb(255, 255, 255);")
        self.transport_machine_toolButton.setIcon(icon)
        self.transport_machine_toolButton.setIconSize(QtCore.QSize(40, 40))
        self.transport_machine_toolButton.setShortcut("Ctrl+S")
        self.transport_machine_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.transport_machine_toolButton.setObjectName("transport_machine_toolButton")
        self.transport_machine_toolButton.clicked.connect(self.transport_machine)
        self.gridLayout.addWidget(self.transport_machine_toolButton, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Transport_Machine_Window)
        QtCore.QMetaObject.connectSlotsByName(Transport_Machine_Window)

    def retranslateUi(self, Transport_Machine_Window):
        _translate = QtCore.QCoreApplication.translate
        Transport_Machine_Window.setWindowTitle(
            _translate("Transport_Machine_Window", f"Μεταφορά μηχανήματος {VERSION}"))
        self.transport_machine_label.setText(_translate("Transport_Machine_Window", "Μεταφορά σε νέα υπηρεσία"))
        self.select_ypiresia_label.setText(_translate("Transport_Machine_Window", "Επιλογή υπηρεσίας"))
        self.office_label.setText(_translate("Transport_Machine_Window", "Επιλογή γραφείου"))
        self.transport_machine_toolButton.setText(_translate("Transport_Machine_Window", "  Μεταφορά"))

    def transport_machine(self):
        """
        Αποθήκευση μεταφοράς μηχανήματος σε νέα υπηρεσία
        Έλεγχος αν έχουμε επιλέξει μηχάνημα
        Έλεγχος αν το εμφανιζόμενο τεχτ στο self.new_ypiresia_lineEdit είναι στη λίστα του all_tables
            Καλείτε
                όταν πατάμε το κουμπί "Μεταφορά" self.transport_btn.clicked στο edit_window.py
        :return:
        """
        if not self.selected_machine:
            QtWidgets.QMessageBox.critical(None, "Σφάλμα",
                                           f"Δεν έχετε επιλέξει μηχάνημα!")
            return
        else:  # Αν είναι ίδια υπηρεσία ίδιο γραφείο
            if self.new_ypiresia_lineEdit.text() == self.selected_machine.__tablename__.upper() \
                    and self.office_lineEdit.text() == self.selected_machine.γραφείο:
                self.new_ypiresia_lineEdit.setStyleSheet("background-color: red;" "color: white;")
                self.office_lineEdit.setStyleSheet("background-color: red;" "color: white;")
                QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Έχετε επιλέξει ίδια υπηρεσία και ίδιο γραφείο!")
                return
            # αν είναι ίδια υπηρεσία διαφορετικό γραφείο
            elif self.new_ypiresia_lineEdit.text() == self.selected_machine.__tablename__.upper() \
                    and self.office_lineEdit.text() != self.selected_machine.γραφείο:
                self.new_ypiresia_lineEdit.setStyleSheet("background-color: green;" "color: white;")
                self.office_lineEdit.setStyleSheet("background-color: green;" "color: white;")
                answer = QtWidgets.QMessageBox.question(None, 'Προσοχή', f"Σίγουρα θέλετε να μεταφέρετε το "
                                                                         f"{self.selected_machine.μοντέλο}\n"
                                                                         f"στή ίδια υπηρεσία αλλά σε νέο γραφείο\n"
                                                                         f"{self.office_lineEdit.text()};",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:
                    self.selected_machine.γραφείο = self.office_lineEdit.text()
                    db.session.commit()
                    QtWidgets.QMessageBox.information(None, "Πληροφορία", "Το μηχάνημα μεταφέρθηκε επιτυχώς!")
                    db.session.close()
                    self.close()

            else:
                self.new_ypiresia_lineEdit.setStyleSheet("background-color: green;" "color: white;")
                self.office_lineEdit.setStyleSheet("background-color: green;" "color: white;")
                new_ypiresia_index = self.all_tables.index(self.new_ypiresia_lineEdit.text())
                self.new_ypiresia = self.tables[new_ypiresia_index]
                # self.new_customer_lineEdit.setText(self.new_customer.Επωνυμία_Επιχείρησης)
                answer = QtWidgets.QMessageBox.question(None, 'Προσοχή', f"Σίγουρα θέλετε να μεταφέρετε το "
                                                                         f"{self.selected_machine.μοντέλο}\n"
                                                                         f"απο {self.selected_machine_table.__tablename__} "
                                                                         f"στή υπηρεσία\n"
                                                                         f"{self.new_ypiresia.__tablename__.upper()}"
                                                                         f" γραφείο {self.office_lineEdit.text()};",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No)
                if answer == QtWidgets.QMessageBox.Yes:
                    try:
                        new_item_to_add = self.new_ypiresia(κωδικός=self.selected_machine.κωδικός,
                                                            τύπος=self.selected_machine.τύπος,
                                                            μοντέλο=self.selected_machine.μοντέλο,
                                                            serial=self.selected_machine.serial,
                                                            γραφείο=self.office_lineEdit.text(),
                                                            αρχικός=self.selected_machine.αρχικός,
                                                            ημερ_αρχι=self.selected_machine.ημερ_αρχι,
                                                            τελικός=self.selected_machine.τελικός,
                                                            ημερο_τελικ=self.selected_machine.ημερο_τελικ,
                                                            σύνολο=self.selected_machine.σύνολο,
                                                            toner_original=self.selected_machine.toner_original,
                                                            toner_symbato=self.selected_machine.toner_symbato,
                                                            drum=self.selected_machine.drum,
                                                            χρέωση=self.selected_machine.χρέωση,
                                                            σχόλια=self.selected_machine.σχόλια)
                        db.session.add(new_item_to_add)
                        db.session.delete(self.selected_machine)
                        QtWidgets.QMessageBox.information(None, "Πληροφορία", "Το μηχάνημα μεταφέρθηκε επιτυχώς!")
                        db.session.commit()
                        db.session.close()
                        self.close()
                    except Exception as error:
                        traceback.print_exc()
                        QtWidgets.QMessageBox.critical(None, "Σφάλμα",
                                                       f"Κάτι δεν πήγε καλά!\nΟι αλλαγές δεν αποθηκευτήκαν!\n{error}")
                        return

    def get_offices(self):
        new_ypiresia_index = self.all_tables.index(self.new_ypiresia_lineEdit.text())
        self.selected_new_table = self.tables[new_ypiresia_index]
        self.selected_table_offices = get_offices_from_table(self.selected_new_table)
        self.office_combobox.clear()
        self.office_combobox.addItems(self.selected_table_offices)
        self.office_completer = QtWidgets.QCompleter(self.selected_table_offices)
        self.office_lineEdit.setCompleter(self.office_completer)
        return

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore()  # if you want the window to never be closed


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    Transport_Machine_Window = QtWidgets.QWidget()
    ui = Ui_Transport_Machine_Window()
    ui.setupUi(Transport_Machine_Window)
    Transport_Machine_Window.show()
    sys.exit(app.exec_())
