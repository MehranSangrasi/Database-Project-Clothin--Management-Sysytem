
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
from fpdf import FPDF

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

mycursor = mydb.cursor()


path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))
absolutePath = path + "//"



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "mainwindow.ui", self)
        self.setWindowTitle("SAMS - Customer Application")
        self.SignUpC1.clicked.connect(self.SignUpfunction)
        self.LoginButtonc.clicked.connect(self.LoginFunction)
        self.SignUpButton.clicked.connect(self.SignUp)
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.tabWidget.tabBar().setVisible(False)

    
    def BacktoLoginfunction(self):
        self.tabWidget.setCurrentIndex(0)
   
    def LoginFunction(self):
        un=self.username.text()
        pa=self.password.text()
        query="SELECT customer_id FROM customerlogin where username='"+un+"' and password='"+pa+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if(len(result))>0: 
            #print(result[0][0])
            self.new= UserWindow(result[0][0]);
            self.new.show();
            self.close();
        else:
            self.message.setText("Username or password Incorrect")

    def SignUpfunction(self):
        self.tabWidget.setCurrentIndex(1) 
    def SignUp(self):
        f_name=self.f_name.text()
        l_name=self.l_name.text()
        username=self.username_n.text()
        password=self.password_n.text()
        city=self.city.text()
        address=self.address.toPlainText()
        question=self.question.currentText()
        answer=self.answer.value()
        contact=self.contact.text().split(",")
        
        query="SELECT customer_id FROM customerlogin where username='"+username+"';"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if len(result)>0:
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Username already exist")
        elif(len(username)<6 or len(password)<6):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Username and Password should be greater than 6 characters")
        elif(f_name=="" or l_name=="" or username=="" or password=="" or city=="" or address=="" or contact==""):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Please fill all the fields")
        elif(checkcontact(contact)==False):
            self.message_2.setText("")
            QtTest.QTest.qWait(100)
            self.message_2.setText("Please enter valid contact number")
        else:
            query="SELECT max(customer_id) FROM customer;"  
            mycursor.execute(query)
            result = mycursor.fetchall()
            id=result[0][0]+1
            query="INSERT INTO customer VALUES ("+str(id)+",'"+f_name+"','"+l_name+"','"+city+"','"+address+"');"
            mycursor.execute(query);
            mydb.commit()
            print("Customer added")
            for i in contact:
                query="INSERT INTO customer_contact VALUES ("+str(id)+",'"+i+"');"
                mycursor.execute(query);
                mydb.commit()
                print("Contact added")
            query="INSERT INTO customerlogin VALUES ("+str(id)+",'"+username+"','"+password+"','"+question+"',"+str(answer)+");"
            mycursor.execute(query);
            mydb.commit()
            self.message_3.setText("Account Created Successfully")
def checkcontact(contact):
    if (contact==['']):
        return False
    for i in contact:
        if(len(i)!=11) or i.isnumeric()==False:
            return False
class UserWindow(QtWidgets.QMainWindow):
    def __init__(self,id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "user.ui", self)
        self.setWindowTitle("SAMS - Customer Application")
        self.id=id
        self.orderid=0
        self.userid1.setText(str(id))
        self.ordercontains=[]
        self.message3.setVisible(False)
        self.tabWidget.tabBar().setVisible(False)
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.BacktoLogin2.clicked.connect(self.BacktoLoginfunction)
        self.manageaccount.clicked.connect(self.mannageAccount)
        self.orderstatus.clicked.connect(self.orderStatus)
        self.Searchitem.clicked.connect(self.searchItem)
        self.logout.clicked.connect(self.logoutfunction)
        self.name.clicked.connect(self.namefunction)
        self.password_2.clicked.connect(self.passwordfunction)
        self.address_2.clicked.connect(self.addressfunction)
        self.question_2.clicked.connect(self.questionfunction)
        self.OrderDetail.layout = QtWidgets.QHBoxLayout(self.OrderDetail)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.OrderDetail.layout.addWidget(self.scrollArea)
        self.checkout.clicked.connect(self.checkoutfunction)
    def questionfunction(self):
        question=self.question.currentText()
        answer=self.answer.value()
        pa=self.password.text()
        query="SELECT customer_id FROM customerlogin where customer_id="+str(self.id)+" and password='"+pa+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        if(len(result)==0):
            self.message.setText("Incorrect Password")
        else:
            query="UPDATE customerlogin SET question='"+question+"',answer="+str(answer)+" where customer_id="+str(self.id)+";"
            self.message.setText("Question Updated Successfully")
    def addressfunction(self):
        ad=self.address.toPlainText()
        city=self.city.text()
        pa=self.password.text()
        query="SELECT customer_id FROM customerlogin where customer_id="+str(self.id)+" and password='"+pa+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        if(len(result)==0):
            self.message.setText("Incorrect Password")
        elif(ad=="" or city==""):
            self.message.setText("Please fill all the fields")
        else:
            query="UPDATE customer SET address='"+ad+"',city='"+city+"' where customer_id="+str(self.id)+";"
            mycursor.execute(query)
            mydb.commit()
            self.message.setText("Address Updated Successfully")
    def passwordfunction(self):
        pa=self.password.text()
        pan=self.password_n.text()
        
        query="SELECT customer_id FROM customerlogin where customer_id="+str(self.id)+" and password='"+pa+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        
        if (pan==""):
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Please fill all the fields")
        elif(len(result)==0):
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Incorrect Password")
        elif(len(pan)<6):
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Password should be greater than 6 characters")
        else:
            query="UPDATE customerlogin SET password='"+pan+"' WHERE customer_id="+str(self.id)+";"
            mycursor.execute(query)
            mydb.commit()
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Password Changed Successfully")
    def namefunction(self):
        pa=self.password.text()
        f_name=self.f_name.text()
        l_name=self.l_name.text()
        
        query="SELECT customer_id FROM customerlogin where customer_id="+str(self.id)+" and password='"+pa+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        if (f_name=="" or l_name==""):
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Please fill all the fields")
        elif(len(result)==0):
            self.message.setText("")
            QtTest.QTest.qWait(100)
            self.message.setText("Incorrect Password")
        else:
            query="UPDATE customer SET first_name='"+f_name+"',last_name='"+l_name+"' where customer_id="+str(self.id)+";"
            mycursor.execute(query)
            mydb.commit()
            self.message.setText("First Name and Last Name Updated Successfully")
    def logoutfunction(self):
        self.new= MainWindow()
        self.new.show()
        self.close()
    def searchItem(self):
        self.new= SearchWindow(self.id);
        self.new.show();
        self.close();
    def orderStatus(self):
        self.tabWidget.setCurrentIndex(2)
        query="SELECT order_id,order_date from orders where order_id in (SELECT order_id from order_status where order_status='active') and customer_id ="+str(self.id)+";"
        mycursor.execute(query)
        result=mycursor.fetchall()
        if len(result)>0:
            self.message3.setVisible(False)
            self.orderid=result[0][0]
            orderdate=result[0][1]
            query="SELECT product_id,quantity from order_contains where order_id= "+str(self.orderid)+";"
            mycursor.execute(query)
            result=mycursor.fetchall()
            self.ordercontains=result
            sum=0
            x=0
            for i in result:
                quantity=i[1]
                query="SELECT product_name,price from products where product_id="+str(i[0])+";"
                mycursor.execute(query)
                result1=mycursor.fetchall()
                name=result1[0][0]
                price=result1[0][1]
                p=itemslide(name,price,quantity,i[0],self.orderid, self)
                self.gridLayout.addWidget(p,x,0)
                x+=1
                sum+=price*quantity
            self.total.setText(str(sum))
            self.OrderDate.setText(str(orderdate))
        else:
            self.message3.setVisible(True)
            self.message3.setText("No Active Orders")
    def mannageAccount(self):
        self.tabWidget.setCurrentIndex(1)
   
    def BacktoLoginfunction(self):
        self.tabWidget.setCurrentIndex(0)
    def checkoutfunction(self):
        #GENERATE PDF bill
        # save FPDF() class into a
        # variable pdf
        query="SELECT order_id,order_date from orders where order_id in (SELECT order_id from order_status where order_status='active') and customer_id ="+str(self.id)+";"
        mycursor.execute(query)
        result=mycursor.fetchall()
        if len(result)>0:
            pdf = FPDF()
            
            # Add a page
            pdf.add_page()
            
            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size = 15)
        
            # create a cell
            #adding image to page top center
            pdf.image("logo.png",x=80,y=10,w=40,h=40)
            #adding 5 blank lines
            for i in range(1,6):
                pdf.cell(200, 10, txt = "", ln = i, align = 'C')
            pdf.cell(200, 10, txt = "Bill",  ln = 7, align = 'C')
            #adding line after bill
            pdf.cell(200, 10, txt = "_____________________________________________________", ln = 8, align = 'C')
            
            # add another cell
            pdf.cell(200, 10, txt = "Total Amount:"+self.total.text(), ln = 10, align = 'C')
            pdf.cell(200, 10, txt = "", ln = 11, align = 'C')
            pdf.cell(200, 10, txt = "Order Date:"+self.OrderDate.text(), ln = 12, align = 'C')
            pdf.cell(200, 10, txt = "", ln = 13, align = 'C')
            pdf.cell(200, 10, txt = "Order ID:"+str(self.orderid), ln = 14, align = 'C')
            pdf.cell(200, 10, txt = "", ln = 15, align = 'C')
            
            pdf.cell(200, 10, txt = "Order Contains:", ln = 16, align = 'C')
            x=17
            for i in self.ordercontains:
                pdf.cell(200, 10, txt = "Product ID:"+str(i[0])+" Quantity:"+str(i[1]), ln = x, align = 'C')
                x+=1
            pdf.cell(200, 10, txt = "Thank You for Shopping with us", ln = x+3, align = 'C')
                    
            # save the pdf with name .pdf
            pdf.output("Bill_"+str(self.orderid)+".pdf")  
            query = "UPDATE order_status SET order_status='completed' where order_id="+str(self.orderid)+";"
            mycursor.execute(query)
            mydb.commit()
            query = "SELECT city from customer where customer_id="+str(self.id)+";"
            mycursor.execute(query)
            city=mycursor.fetchall()
            query = "INSERT into checkout values("+str(self.orderid)+",'"+city[0][0]+"',"+self.total.text()+");"
            mycursor.execute(query)
            mydb.commit()
            self.cleargrid()
            self.total.setText("0")
            
    def cleargrid(self):
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)
        
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
      
    def run(self):
        self.parent.searchfunction()
    
class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self,id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(absolutePath + "usersearch.ui", self)
        self.setWindowTitle("SAMS - Customer Application")
        self.customerid=id
        self.id=id
        self.userid1.setText(str(id))
        self.BacktoLogin.clicked.connect(self.BacktoLoginfunction)
        self.search.clicked.connect(self.runLongTask)
        self.productsWidget.layout = QtWidgets.QHBoxLayout(self.productsWidget)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.productsWidget.layout.addWidget(self.scrollArea)
        self.productsWidget.setVisible(False)
        self.message.setVisible(False)
        self.loading.setVisible(False)
    
    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.showCards)
        self.thread.start()
    
    def showCards(self, arr):
        if(not len(arr)): 
            self.cleargrid()
        else:
            self.AddPostCard(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9],arr[10])
          
    def searchfunction(self):
        self.worker.progress.emit([])
        self.loading.setVisible(True)
        
        category=self.category.currentText()
        gender=self.gender.currentText()
        size=self.size.currentText()
        query="SELECT category_id FROM categories where category_name='"+category+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        categoryid=result[0][0]
        query="SELECT product_id,product_name,product_color,product_photo,price from products where category_id="+str(categoryid)+" and product_size='"+size+"' and gender='"+gender+"';"
        mycursor.execute(query)
        result=mycursor.fetchall()
        print(result)
        if (len(result)==0):
            self.productsWidget.setVisible(False)
            self.message.setVisible(True)
        else:
            self.message.setVisible(False)
            self.productsWidget.setVisible(True)
            x=0
            
            for i in result:
                arr = [self.customerid,i[0],size,i[3],i[1],i[4],i[2],category,gender,x//2,x%2]
                self.worker.progress.emit(arr)
                x=x+1
        
        self.loading.setVisible(False)
        self.worker.finished.emit()
    def cleargrid(self):
        for i in reversed(range(self.gridLayout.count())): 
         self.gridLayout.itemAt(i).widget().setParent(None)
    def AddPostCard(self,customerid,id,size,photo,name,price,color,category,gender,i,j):     
        p=PostCard(customerid,id,photo,size,name,price,color,category,gender)
        self.gridLayout.addWidget(p,i,j)
    def BacktoLoginfunction(self):
        self.new= UserWindow(self.id);
        self.new.show();
        self.close();
class PostCard(QtWidgets.QWidget):
    def __init__(self,customerid,id,photo,size,product_name,price,color,category,gender, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "postCard.ui", self)
        self.setWindowTitle("")
        self.customerid=customerid
        self.id=id
        self.price=price
        self.color=color
        self.category=category
        self.gender=gender
        self.parent = parent
        self.size.setText(size)
        self.name.setText(product_name)
        data = request.urlopen(photo).read()
        self.im = QPixmap()
        self.im.loadFromData(data)
        self.image.setPixmap(self.im)
        self.open.clicked.connect(self.open1)
    def open1(self):
        self.new= itempage(self.customerid,self.id,self.im,self.size.text(),self.name.text(),self.price,self.color);
        self.new.show()
class itemslide(QtWidgets.QWidget):
        def __init__(self,name,price,quantity,product_id,order_id, parent=None):
            super().__init__()
            uic.loadUi(absolutePath + "item.ui", self)
            self.setWindowTitle("SAMS")
            self.parent = parent
            self.name.setText(name)
            self.amount.setText(str(price))
            self.quantity.setText(str(quantity))
            self.total.setText(str(price*quantity))
            self.product_id = product_id
            self.order_id = order_id
            self.deleteButton.clicked.connect(self.deleteItem)
            
        def deleteItem(self):
            self.deleteButton.setEnabled(False)
            query = "DELETE FROM order_contains WHERE product_id = " + str(self.product_id) + " AND order_id = " + str(self.order_id) + ";"
            mycursor.execute(query)
            mydb.commit()
            self.parent.cleargrid()
            self.parent.orderStatus()

class itempage(QtWidgets.QWidget):
    def __init__(self,customerid,id,photo,size,product_name,price,color, parent=None):
        super().__init__()
        uic.loadUi(absolutePath + "itempage.ui", self)
        self.setWindowTitle("SAMS")
        self.parent = parent
        self.id=id
        self.customerid=customerid
        self.picture.setPixmap(photo)
        self.name.setText(product_name)
        self.color.setText(color)
        self.price.setText(str(price)+" Rs")
        self.size.setText(size)
        self.buy.clicked.connect(self.buy1)
        self.back.clicked.connect(self.back1)
    def back1(self):
        self.close()
    def buy1(self):
        quantity=self.quantity.value()
        if (quantity==0):
            self.message.setText("Quantity cannot be 0")
        else:
            query="Select order_id from order_status where order_id in (select order_id from orders where customer_id ="+str(self.customerid)+" ) and order_status='active'; "    
            mycursor.execute(query)
            result=mycursor.fetchall()
            if len(result)>0:   # Triggers if the customer has an active order
                orderid=result[0][0]
                query="INSERT INTO order_contains VALUES ("+str(orderid)+","+str(self.id)+","+str(quantity)+");"
                mycursor.execute(query)
                mydb.commit()
                self.message.setText("Item added to cart")
            else:
                mycursor.callproc('generate_order_id')
                for result1 in mycursor.stored_results():
                    result=result1.fetchall()
                #print(result)
                orderid=result[0][0]
                query="INSERT INTO orders VALUES ("+str(orderid)+","+str(self.customerid)+",now());"
                mycursor.execute(query)
                mydb.commit()
                query="INSERT INTO order_status VALUES ("+str(orderid)+",'active');"
                mycursor.execute(query)
                mydb.commit()
                query="INSERT INTO order_contains VALUES ("+str(orderid)+","+str(self.id)+","+str(quantity)+");"
                mycursor.execute(query)
                mydb.commit()
                self.message.setText("Item added to cart")


        
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
   # app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    app.exec_();
    