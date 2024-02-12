from flask import Flask,render_template,url_for,request,redirect,session
from database import get_database
from werkzeug.security import  generate_password_hash,check_password_hash
import google.generativeai as genai
from dotenv import load_dotenv
from os import getenv
from PIL import Image
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import io
import os
load_dotenv()

genai.configure(api_key=getenv("VITE_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')
app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)

# def get_current_user():
#     user=None
#     if 'user' in session:
#         user=session['user']
#         db=get_database()
#         user_cursor=db.execute("select * from users where username=?", [user])
#         user=user_cursor.fetchone()
#         return user

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5/minute"],
    storage_uri="memory://",
)
app=Flask(__name__ )

@app.route('/')
def home():
    # user=get_current_user()
    return render_template('index.html')
@app.route('/about')
def about():
    # user=get_current_user()
    return render_template('about.html')
@app.route('/department')
def department():
    # user=get_current_user()
    return render_template('departments.html')
@app.route('/contactus')
def contact():
    # user=get_current_user()
    return render_template('contact.html')


@app.route('/medimate')
def medimate():
    # user=get_current_user()
    return render_template('medimate.html')


@app.route('/medimate_vision')
def medimate_vision():
    # user=get_current_user()
    return render_template('medimate_vision.html')

@app.route('/medimate_vision')
def medimate_vision():
    # user=get_current_user()
    return render_template('medimate_vision.html')

@app.post('/upload')
@limiter.limit("5/minute")
def upload():
    if 'file' not in request.files:
        return {'error': 'No file part'}

    file = request.files['file']
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))

    try:
        print("Generating with prompt...")
        print(request.form['prompt'])
        print("-"*20)
        response = model.generate_content([request.form['prompt'], img])
        print("Generated!")
        print(response.text)
        print("-"*20)

        return {'result': response.text}, 200
    except Exception as e:
        return f"Sorry, it looks like an error occured from Google's side. Here is more info:\n{str(e)}\nTry again after a bit.", 500







# @app.route('/authenticate_user1',methods=["POST","GET"])
# def register():
#     # user=get_current_user()
#     register_error=None
#     if request.method=="POST":
#         #collect information from form
#         username=request.form['username']
#         password=request.form['password']
        
#         # generat a hash code for password entered by user
#         hash_password=generate_password_hash(password)
        
        
#         #coonect database
#         db=get_database()
        
#         #checking duplicate
#         user_cursor=db.execute("select * from users where username=?",[username])
#         existing_user=user_cursor.fetchone()
        
#         if existing_user:
#             register_error="Email already taken,please enter different email."
#             return render_template("login.html",register_error=register_error)
            
#         # sql query ti insert values in table
#         db.execute("INSERT INTO users(username,password,admin) VALUES(?,?,?)",(username,hash_password,'0')) 
#         # make changes in database
#         db.commit()
#         return redirect(url_for('login'))
#     return render_template('login.html',user=user)




# @app.route('/authenticate_user',methods=["POST","GET"])
# def login():
#     user=get_current_user()
#     error=None
#     if request.method=="POST":
#         #collect information from form
#         username=request.form['username']
#         user_entered_password=request.form['password']
        
#         #coonect database
#         db=get_database()
#         # sql query ti insert values in table
#         user_cursor=db.execute("select * from users where username=? ",[username]) 
#         user=user_cursor.fetchone()
        
#         if user:
#             if check_password_hash(user['password'],user_entered_password):
#                 session['user']=user['username']
#                 return redirect(url_for('home'))
#             else:
#                 error="Password didnot match."
        
#     return render_template('login.html',loginerror=error,user=user)




if __name__=="__main__":
    app.run(debug=True,port=5003)