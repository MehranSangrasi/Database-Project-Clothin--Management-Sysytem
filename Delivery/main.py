
import mysql.connector
import sys
from PyQt5 import QtWidgets, QtCore, uic,QtTest
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pathlib import Path
import os
from urllib import request
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="sql6.freemysqlhosting.net",
  user="sql6586886",
  password="DBvmexKzNM",
  database="sql6586886"
)

mycursor = mydb.cursor()


path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//"



class MainWindow(QtWidgets.QMainWindow):
    cnic=""
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "mainwindow.ui", self)
        self.setWindowTitle("Clothing Management System")
        self.LoginButton.clicked.connect(self.LoginFunction)
        self.SignOutButton.clicked.connect(self.BacktoLoginfunction)
        self.CityButton.clicked.connect(self.ChangeCity)
        self.PendingDeliveriesButton.clicked.connect(self.pendingDeliveryDetails)
        self.BackPendingButton.clicked.connect(self.backToMainMenu)
        self.productsWidget.layout = QtWidgets.QHBoxLayout(self.productsWidget)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.productsWidget.layout.addWidget(self.scrollArea)
        self.PreviousDButton.clicked.connect(self.previousDeliveryDetails)
        
      
      
       
    
        
        #self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.tabWidget.setCurrentIndex(0)

        self.tabWidget.tabBar().setVisible(False)
    
    def BacktoLoginfunction(self):
        self.tabWidget.setCurrentIndex(0)
        self.username.setText("")
        self.password.setText("")

   
    def LoginFunction(self):
        
        un=self.username.text()
        pa=self.password.text()
        query="SELECT cnic_no, city FROM delivery_boy where username='"+un+"' and password='"+pa+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if(len(result))>0: 
            #print(result[0][0])
            self.cnic = result[0][0]
            self.tabWidget.setCurrentIndex(1)
            self.CurrentCity.setText(result[0][1])
        else:
            self.message.setText("Username or password Incorrect")

    def ChangeCity(self):
        city=self.CurrentCity.text()
        query="UPDATE delivery_boy SET city = '"+city+"' WHERE cnic_no = '"+self.cnic+"';"
        mycursor.execute(query)
        mydb.commit()

    def backToMainMenu(self):
        self.tabWidget.setCurrentIndex(1)

    def pendingDeliveryDetails(self):
        
        self.tabWidget.setCurrentIndex(2)
        self.message_2.setVisible(False)
        self.cleargrid()
        query = "SELECT orders.order_id,order_date,city,payment FROM checkout join orders on checkout.order_id=orders.order_id where city= '"+self.CurrentCity.text()+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if(len(result))>0: 
            x=0
            for i in result:
                p=deliveryslide(i[0],i[1],i[2],i[3],self.cnic,self)
                self.gridLayout.addWidget(p,x,0)
                x+=1
        else:
            self.message_2.setVisible(True)
            
    def previousDeliveryDetails(self):
            
        self.tabWidget.setCurrentIndex(2)
        self.message_2.setVisible(False)
        self.cleargrid()
        query = "SELECT orders.order_id,order_date FROM order_delivery join orders on order_delivery.order_id=orders.order_id where cnic= '"+self.cnic+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if(len(result))>0: 
            x=0
            for i in result:
                p=previousSlide(i[0],i[1],self)
                self.gridLayout.addWidget(p,x//2,x%2)
                x+=1
        else:
            self.message_2.setVisible(True)

    def checkcontact(contact):
        if (contact==['']):
            return False
        for i in contact:
            if(len(i)!=11) or i.isnumeric()==False:
                return False
    def cleargrid(self):
            for i in reversed(range(self.gridLayout.count())): 
                self.gridLayout.itemAt(i).widget().setParent(None)
        
class previousSlide(QtWidgets.QWidget):
        def __init__(self,orderid,orderdate,parent=None):
            super().__init__()
            uic.loadUi(absolutePath + "prev.ui", self)
            self.setWindowTitle("SAMS")
            self.parent = parent
            self.orderid.setText(str(orderid))
            self.orderDate.setText(orderdate)
            
class deliveryslide(QtWidgets.QWidget):
        def __init__(self,orderid,orderdate,city,amount,cnic,parent=None):
            super().__init__()
            uic.loadUi(absolutePath + "orders.ui", self)
            self.setWindowTitle("SAMS")
            self.parent = parent
            self.cnic=cnic
            self.orderid.setText(str(orderid))
            self.orderDate.setText(orderdate)
            self.city.setText(city)
            self.amount.setText(str(amount))
            self.accept.clicked.connect(self.acceptOrder)
        def acceptOrder(self):
         
            query = "UPDATE order_status SET order_status = 'delivered' where order_id = "+self.orderid.text()+";"
            mycursor.execute(query)
            mydb.commit()
            query = "Insert into order_delivery values("+self.orderid.text()+", '"+self.cnic+"');"
            mycursor.execute(query)
            mydb.commit()
            self.accept.setEnabled(False)
            query = "SELECT payment FROM checkout where order_id = "+self.orderid.text()+";"
            mycursor.execute(query)
            result = mycursor.fetchall()
            query = "insert into payments values ('"+self.orderid.text()+"', '"+str(result[0][0])+"');"
            mycursor.execute(query)
            mydb.commit()
            query="delete from checkout where order_id = "+self.orderid.text()+";"
            mycursor.execute(query)
            mydb.commit()
            self.parent.pendingDeliveryDetails()
       
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
   # app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    app.exec_();
    