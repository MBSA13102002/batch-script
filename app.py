from flask import Flask,render_template,request,redirect, url_for,abort
import random 
import os
import json,ast
import firebase_admin
from firebase_admin import credentials,storage as strg
cred = credentials.Certificate("./portfoliomanagement-16f09-firebase-adminsdk-9inmb-24030872d5.json")
from firebase import Firebase
from werkzeug.utils import secure_filename 
admin = firebase_admin.initialize_app(cred, {
      'storageBucket': 'portfoliomanagement-16f09.appspot.comd'})
def rand_pass():
    pass_data = "qwertyuiopasdfgjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.sample(pass_data, 10))
    return password
def handle_catch(caller, on_exception):
    try:
         return caller()
    except:
         return on_exception
        
# config = {
#     "apiKey": "AIzaSyA1h6NqVizacIpvyUExiPzUy7LKbT5VV4c",
#    "authDomain": "hackilo-edutech.firebaseapp.com",
#     "databaseURL": "https://hackilo-edutech-default-rtdb.firebaseio.com",
#     "projectId": "hackilo-edutech",
#     "storageBucket": "hackilo-edutech.appspot.com",
#     "messagingSenderId": "432434540165",
#     "appId": "1:432434540165:web:e364ec66e0ae0e8e6cc3ec",
#     "measurementId": "G-HVEVSTM0XC"
# }
config = {
    "apiKey": "AIzaSyBQUpIYvs0WKfP5IMD4TE2IWTvpb5U34Cc",
   "authDomain": "portfoliomanagement-16f09.firebaseapp.com",
    "databaseURL": "https://portfoliomanagement-16f09.firebaseio.com",
    "projectId": "portfoliomanagement-16f09",
    "storageBucket": "portfoliomanagement-16f09.appspot.com",
    "messagingSenderId": "505793158040",
    "appId": "1:505793158040:web:14b9466a349235ef8b69ed",
    "measurementId": "G-MRCWJ4R5RJ"
}

firebase = Firebase(config)
db = firebase.database()
storage = firebase.storage()
bucket = strg.bucket()
app = Flask(__name__)


app.config['UPLOAD_EXTENSIONS'] = ['.png','.jpg','jpeg','.webp','.PNG','.JPG','.JPEG','.WEBP'] 
app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048


# =========================================================

Types_Of_Questions = db.child("Question_Types").get()

# =======================================================



@app.errorhandler(413)
def too_large(e):    
    return "File is too large", 413 


@app.route("/",methods = ['GET','POST'])
def home():
    Chapter_List = db.child("Chapter_List").get()
    if request.method == 'POST':
        Chapter_Name=request.form.get("Chapter_Name")
        id =random.randint(10000,99999)
        data = {
            "ChapterName":Chapter_Name,
            "Chapter_ID":id,
            "No_of_Questions":0,
            "Topics_List":" "
        }
        db.child("Chapter_List").push(data)
        Chapter_List_New = db.child("Chapter_List").get()
        return render_template("index.html",Chapter_List = Chapter_List_New,handle_catch=handle_catch)
    return render_template("index.html",Chapter_List = Chapter_List,handle_catch=handle_catch)




@app.route("/chapter/<string:chapter_key>/",methods = ['GET','POST'])
def chapter_details(chapter_key):
    if request.method == 'POST':
        Question=request.form.get("Question")
        Question_Type=request.form.get("Question_Type")
        id =random.randint(100000,999999)
        data = {
            "Question":Question,
            "Question_Type":Question_Type,
            "Question_ID":id,
            "Question_Level":"",
            "OPT_JSON":" ",
            "Topics_List":" ",
            "Explanation":" "
        }
        number = db.child("Chapter_List").child(chapter_key).child("No_of_Questions").get()
        db.child("Chapter_List").child(chapter_key).child("No_of_Questions").set(number.val()+1)
        db.child("Chapter_List").child(chapter_key).child("Question_List").push(data)
        Chapter_List_New = db.child("Chapter_List").get()
        ques_types = db.child("Question_Types").get()
        for item in Chapter_List_New.each():
            if (item.key()==chapter_key):
                chapter=item
                return render_template("chapter_detail.html",chapter=chapter,ques_types=ques_types,handle_catch=handle_catch)
    chapter_data = db.child("Chapter_List").get()
    ques_types = db.child("Question_Types").get()
    for item in chapter_data.each():
        if (item.key()==chapter_key):
            chapter=item
            return render_template("chapter_detail.html",chapter=chapter,ques_types=ques_types,handle_catch=handle_catch)




@app.route("/chapter/topic/<string:chapter_key>/",methods = ['GET','POST'])
def chapter_topic_add(chapter_key):
    if request.method == 'POST':
        Topic_Name=request.form.get("Topic_Name")
        data = {
         "Topic_Name":Topic_Name
        }
        db.child("Chapter_List").child(chapter_key).child("Topics_List").push(data)
        return redirect(url_for('chapter_details',chapter_key=chapter_key))


@app.route("/chapter/category/<string:chapter_key>/",methods = ['GET','POST'])
def chapter_category_add(chapter_key):
    if request.method == 'POST':
        HTMLDATA=request.form.get("quescategoryhtmldata")
        data = {
         "DATA":HTMLDATA
        }
        db.child("Chapter_List").child(chapter_key).child("Categories_Data").set(data)
        return redirect(url_for('chapter_details',chapter_key=chapter_key))






@app.route("/chapter/topic/delete/<string:chapter_key>/<string:topic_key>",methods = ['GET','POST'])
def chapter_topic_delete(chapter_key,topic_key):
    # if request.method == 'POST':
    topic_name = db.child("Chapter_List").child(chapter_key).child("Topics_List").child(topic_key).child("Topic_Name").get().val()
    db.child("Chapter_List").child(chapter_key).child("Topics_List").child(topic_key).remove()
    try:
        for item in db.child("Chapter_List").child(chapter_key).child("Question_List").get().each():
            try:
                for key,value in item.val()['Topics_List'].items():
                    if value==topic_name:
                        db.child("Chapter_List").child(chapter_key).child("Question_List").child(item.key()).child("Topics_List").child(key).remove()
                            
            except:
                pass
    except: 
        pass
    return redirect(url_for('chapter_details',chapter_key=chapter_key))





@app.route("/question/<string:chapter_key>/<string:question_key>/",methods = ['GET','POST'])
def question_detail(chapter_key,question_key):
    if request.method == 'POST':
        Question=request.form.get("Question")
        Question_Type=request.form.get("Question_Type")
        Question_Ids=request.form.get("Question_Tag_Ids")
        Options_Ids=request.form.get("Options_Tag_Ids")
        Explanation = request.form.get("Explanation")
        # y = json.loads(Options_Ids)
        if Options_Ids!="":
            y = ast.literal_eval(Options_Ids)
        else:
            y=" "
        # l=[]
        # m = Options_Ids.split(",")
        # for i in m:
        #     if (i==''):
        #         m.remove(i)
        # for i in range(len(m)):
        #     l.append(random.randint(1000,9999))
        # k = dict(zip(l,m))
        update_data = {
            "Question":Question,
            "Question_Type":Question_Type,
            "TAG_Ids":Question_Ids,
            "OPT_JSON":y,
            "Explanation":Explanation
           

            
        }
        db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).update(update_data)
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))

    Chapter_Data = db.child("Chapter_List").get()
    for item in Chapter_Data.each():
        if (item.key()==chapter_key):
            for key,value in item.val()["Question_List"].items():
                if(key==question_key):
                    return render_template("question_detail.html",question_data=value,chapter_key = chapter_key,question_key = key,ques_types = Types_Of_Questions,img_data = db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Images").get(),topic_list = item.val()["Topics_List"],category_list_string = item.val()['Categories_Data']['DATA'],user_category_array = db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Categories_Data_Array").get().val(), handle_catch=handle_catch)





@app.route("/question/topic/<string:chapter_key>/<string:question_key>",methods = ['GET','POST'])
def question_topic_add(chapter_key,question_key):
    if request.method =='POST':
        topic_JSON = request.form.get("topics_values")
        if topic_JSON!="":
            y = ast.literal_eval(topic_JSON)
        else:
            y=" "
        
        db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Topics_List").set(y)
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))

@app.route("/question/category/<string:chapter_key>/<string:question_key>",methods = ['GET','POST'])
def question_category_add(chapter_key,question_key):
    if request.method =='POST':
        categories= request.form.get("ques_specific_categories_htmldata")
        # if categories!="":
        #     y = ast.literal_eval(topic_JSON)
        # else:
        #     y=" "
        
        db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Categories_Data_Array").set(categories.split(','))
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))




@app.route("/upload/<string:chapter_key>/<string:question_key>/",methods = ['GET','POST'])
def photo_upload(chapter_key,question_key):
    if request.method =='POST':
        sai = request.form.get("uploaddd")
        print(str(sai))
        my_files = request.files           
        for item in my_files: 
            uploaded_file = my_files.get(item)  
            uploaded_file.filename = secure_filename(uploaded_file.filename)        
            if uploaded_file.filename != '':            
                file_ext = os.path.splitext(uploaded_file.filename)[1]           
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:            
                abort(400)         
            unique_id =  rand_pass()
            uploaded_file.save(unique_id)  
            storage.child(f"images/{unique_id}").put(unique_id)
            db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Images").push({
                "url":storage.child(f"images/{unique_id}").get_url(None),
                "filename":unique_id
                })
            os.remove(unique_id)
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))



@app.route("/delete/<string:chapter_key>/<string:question_key>/<string:Image_key>/<string:file_name>/",methods = ['GET','POST'])
def delete_upload(chapter_key,question_key,Image_key,file_name):
    if request.method =='POST':
        db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).child("Images").child(Image_key).remove()
        blob = bucket.blob(f'images/{file_name}')
        blob.delete() 
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))




@app.route("/delete/chapter/<string:chapter_key>/",methods = ['GET','POST'])
def chapter_delete(chapter_key):
    Chapter_Data = db.child("Chapter_List").get()
    for item in Chapter_Data.each():
        if (item.key()==chapter_key):
            # ===================================IMAGE REMOVAL=====================
            try:
                for key in item.val()["Question_List"].keys():
                    for key_,value_ in item.val()["Question_List"][key]["Images"].items():
                        img_name = value_["filename"]
                        blob = bucket.blob(f'images/{img_name}')
                        blob.delete() 
            except:
                pass
            # =======================================================================
            db.child("Chapter_List").child(chapter_key).remove()
            return redirect(url_for('home'))
            # return render_template("index.html",Chapter_List = db.child("Chapter_List").get(),handle_catch=handle_catch)

@app.route("/question/level/<string:chapter_key>/<string:question_key>",methods = ['GET','POST'])
def question_level_add(chapter_key,question_key):
    if request.method =='POST':
        level = request.form.get("level")
        db.child("Chapter_List").child(chapter_key).child("Question_List").child(question_key).update({
            "Question_Level":level
        })
        return redirect(url_for('question_detail',chapter_key=chapter_key,question_key=question_key))




@app.route("/chapter/<string:chapter_key_first>/delete/question/<string:chapter_key>/<string:question_key>/",methods = ['GET','POST'])
def question_delete(chapter_key_first,chapter_key,question_key):
    Chapter_Data = db.child("Chapter_List").get()
    for item in Chapter_Data.each():
        if (item.key()==chapter_key):
             for key in item.val()["Question_List"].keys():
                    if(key==question_key):
                        # ===============================================================
                        try:
                            for key_,value_ in item.val()["Question_List"][key]["Images"].items():
                                img_name = value_["filename"]
                                blob = bucket.blob(f'images/{img_name}')
                                blob.delete() 
                        except:
                            pass
                        # ===============================================================
                        db.child("Chapter_List").child(chapter_key).child("Question_List").child(key).remove()
                        number = db.child("Chapter_List").child(chapter_key).child("No_of_Questions").get()
                        db.child("Chapter_List").child(chapter_key).child("No_of_Questions").set(number.val()-1)
                        return redirect(url_for('chapter_details',chapter_key=chapter_key))
            # return render_template("index.html",Chapter_List = db.child("Chapter_List").get(),handle_catch=handle_catch)




app.run()
