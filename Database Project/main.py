
import mysql.connector
import sys
from PyQt5 import QtWidgets, QtCore, uic,QtTest
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pathlib import Path
import os
from urllib import request
import mysql.connector


# mydb = mysql.connector.connect(
#   host="sql6.freemysqlhosting.net",
#   user="sql6585479",
#   password="UlH7IWS76K",
#   database="sql6585479"
# )
mydb = mysql.connector.connect(
  host="sql6.freemysqlhosting.net",
  user="sql6586886",
  password="DBvmexKzNM",
  database="sql6586886"
)

import cloudinary
cloudinary.config( 
  cloud_name = "dtmkcicmp", 
  api_key = "561596993519957", 
  api_secret = "4YCRnvBSG8VKCqkL4r481qja9Yo" 

)
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

mycursor = mydb.cursor()

path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//gui//"


     
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "mainwindow.ui", self)
        self.setWindowTitle("Clothing Management System")
        self.tabWidget.tabBar().setVisible(False)
        self.LoginButton.clicked.connect(self.loginfunction)
        self.delivery.clicked.connect(self.deliveryfunction)
        self.additem.clicked.connect(self.additemfunction)
        self.report.clicked.connect(self.reportfunction)
        self.logout.clicked.connect(self.logoutfunction)
    def loginfunction(self):
        un=self.username.text()
        pa=self.password.text()
        query="SELECT operator_id FROM operator where username='"+un+"' and password='"+pa+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if(len(result))>0: 
            #print(result[0][0])
            self.tabWidget.setCurrentIndex(1)
        else:
            self.message.setText("Username or password Incorrect")
    def deliveryfunction(self):
        self.new = delivery()
        self.new.show()
        self.close()
    def additemfunction(self):
        self.new = additem()
        self.new.show()
        self.close()
        
    def reportfunction(self):
        self.new = report()
        self.new.show()
        self.close()
    def logoutfunction(self):
        self.new = MainWindow()
        self.new.show()
        self.close()
    
####################################### Login Class ###########################################    
class delivery(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "m_deliveryboy.ui", self)
        self.setWindowTitle("SAMS")
        self.parent = parent
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.addButton.clicked.connect(self.addfunction)
    #     self.SignUpC1.clicked.connect(self.SignButtonC)
        
    # def SignButtonC(self):
    #     self.tabWidget.setCurrentIndex(2) 
    def BacktoLoginfunction(self):
        self.new = MainWindow()
        self.new.show()
        self.new.tabWidget.setCurrentIndex(1)
        self.close()
    def addfunction(self):
        f_name=self.f_name.text()
        l_name=self.l_name.text()
        username=self.username_n.text()
        password=self.password_n.text()
        city=self.city.text()
        contact=self.contact.text().split(",")
        cnic=self.cnic.text()
        query="SELECT cnic_no FROM delivery_boy where cnic_no='"+cnic+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if len(result)>0:
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("CNIC already exist")
        elif(len(username)<6 or len(password)<6):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Username and Password should be greater than 6 characters")
        elif(f_name=="" or l_name=="" or username=="" or password=="" or city==""  or contact==""):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Please fill all the fields")
        elif(checkcontact(contact)==False):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Please enter valid contact number")
        elif (len(cnic)!=13 or not cnic.isnumeric()):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Please enter valid cnic number")
        else:
            
            query="INSERT INTO delivery_boy VALUES ('"+f_name+"','"+l_name+"','"+username+"','"+password+"','"+city+"','"+cnic+"');"
            mycursor.execute(query);
            mydb.commit()
            print("Customer added")
            for i in contact:
                query="INSERT INTO delivery_contac VALUES ('"+cnic+"','"+i+"');"
                mycursor.execute(query);
                mydb.commit()
                print("Contact added")
            
            self.message_3.setText("Account Created Successfully")
class additem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "inseritem.ui", self)
        self.setWindowTitle("SAMS")
        self.loc=""
        self.parent = parent
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.uploadbutton.clicked.connect(self.uploadfunction)
        self.add.clicked.connect(self.addfunction)
    def addfunction(self):
        na=self.name.text()
        color=self.color.text()
        size=self.size1.currentText()
        category=self.category.currentText()
        price=self.price.value()
        gender=self.gender.currentText()
        query= "SELECT Category_id FROM categories where Category_name='"+category+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        categoryid=result[0][0]
        mycursor.callproc("generate_product_id")

        for x in mycursor.stored_results():
            results = x.fetchall()
        productid=results[0][0]
        
        if(na=="" or color==""):
            self.message.setText("Please fill all the fields")
        elif(self.loc==""):
            self.message.setText("Please upload the image")
        elif(price==0):
            self.message.setText("Please enter the price")
        else:
            query="INSERT INTO products values("+str(categoryid)+","+str(productid)+",'"+na+"','"+size+"','"+color+"','"+self.loc+"',"+str(price)+",'"+gender+"');"
            mycursor.execute(query)
            mydb.commit()
            self.message.setText("Item Added")
    def uploadfunction(self):
        path=QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.gif *.png *.jpeg *.bmp *.webp)")
        path=path[0]
        url=upload(path)
        self.loc=url['secure_url']
        self.message.setText("Image Selected")
    def BacktoLoginfunction(self):
        self.new = MainWindow()
        self.new.show()
        self.new.tabWidget.setCurrentIndex(1)
        self.close()
 
class report(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "report.ui", self)
        self.setWindowTitle("SAMS")
        self.parent = parent
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        query="SELECT count(*) FROM customer;"
        mycursor.execute(query)
        result=mycursor.fetchall()
        self.customer.setText(str(result[0][0]))
        query="SELECT count(*) from orders;"
        mycursor.execute(query)
        result=mycursor.fetchall()
        self.orders.setText(str(result[0][0]))
        query="SELECT count(*) from delivery_boy;"
        mycursor.execute(query)
        result=mycursor.fetchall()
        self.delivery.setText(str(result[0][0]))
        query="SELECT sum(payment) from payments;"
        mycursor.execute(query)
        result=mycursor.fetchall()
        self.revenue.setText(str(result[0][0]))
        query="SELECT count(*) from products where category_id=101;"
        mycursor.execute(query)
        self.shoes.setText(str(mycursor.fetchall()[0][0]))
        query="SELECT count(*) from products where category_id=101;"
        mycursor.execute(query)
        self.shirts.setText(str(mycursor.fetchall()[0][0]))
        query="SELECT count(*) from products where category_id=102;"
        mycursor.execute(query)
        self.bottoms.setText(str(mycursor.fetchall()[0][0]))
        query="SELECT count(*) from products where category_id=103;"
        mycursor.execute(query)
        self.suits.setText(str(mycursor.fetchall()[0][0]))
        query="SELECT count(*) from products where category_id=104;"
        mycursor.execute(query)
        self.accessories.setText(str(mycursor.fetchall()[0][0]))
        query="SELECT count(*) from products where category_id=105;"
        mycursor.execute(query)
        self.shirts.setText(str(mycursor.fetchall()[0][0]))
        
    def BacktoLoginfunction(self):
        self.new = MainWindow()
        self.new.show()
        self.new.tabWidget.setCurrentIndex(1)
        self.close()
        
def checkcontact(contact):
    if (contact==['']):
        return False
    for i in contact:
        if(len(i)!=11) or i.isnumeric()==False:
            return False
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
   # app.setStyleSheet(stylesheet)
    window = MainWindow()
    
    window.show()
    app.exec_();
    