from tkinter import *
root=Tk()
import pyrebase
config ={
  "apiKey": "AIzaSyCCF5YTqq35piJ8B6Od7ymPthLqmqLwsxE",
    "authDomain": "pybase-44f1b.firebaseapp.com",
    "databaseURL": "https://pybase-44f1b-default-rtdb.firebaseio.com",
    "projectId": "pybase-44f1b",
    "storageBucket": "pybase-44f1b.appspot.com",
    "serviceAccount":"pybase-44f1b-firebase-adminsdk-cvqbt-d2e92b4ae1.json"
}

# firebase_storage = pyrebase.initialize_app(config) 
# storage=firebase_storage.storage()
# storage.child("D:/wifi.txt").put("D:/wifi.txt")
root.mainloop()
