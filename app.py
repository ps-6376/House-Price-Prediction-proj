from flask import Flask,render_template,request,redirect
import pymysql as sql
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error


app=Flask("__name__")
@app.route("/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("username")   
        password=request.form.get("password")
        cnf_pass=request.form.get("cnf_pass")
        print(uname)
        print(password)
        print(cnf_pass)
        if password==cnf_pass:   
           try:
               conn=sql.connect(user="root",password="",host="localhost",port=3306,database="house_data")
               cursor=conn.cursor()
               query="insert into  house_cred(username,password,cnf_pass) values(%s,%s,%s);"
               cursor.execute(query,(uname,password,cnf_pass))
           except sql.err.IntegrityError as e:
            #   check condition for duplicate entrys
                if e.args[0] == 1062: 
                    war="this usename already exist" 
                    return render_template("signup.html",war=war)
                else:
                    war=f"there is {e}"
                    return render_template("signup.html",war=war)
           except Exception as e:
               msg=f"there is {e}"
               return render_template("signup.html",msg=msg)
           else:
               print("connection is close")
               conn.commit()
               conn.close()
               return redirect("/login")
        else:
            msg="password and confirm password not match"
            return render_template("signup.html",msg=msg)
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        print("yes methood is post in login")
        uname=request.form.get("uname")
        passw=request.form.get("password")
        try:
            conn=sql.connect(user="root",password="",host="localhost",port=3306,database="house_data")       
            cursor=conn.cursor()
            query="select username,password from house_cred where username=%s AND password=%s;"
            cursor.execute(query,(uname,passw))
            print("username and pass is passed")
            user=cursor.fetchone()
            if user:
                cursor.close()
                conn.close() 
                # conn=sql.connect(user="root",password="",host="localhost",port=3306,database="filedata")       
                # cursor=conn.cursor()
                # q="select company_type from jaipur;"
                # cursor.execute(q)
                # com_types=cursor.fetchall()
                # print(com_types)
                return redirect("/home")
            
            else:
                msgg="invalid credentials"
                return render_template("login.html",msgg=msgg)
        except sql.Error as e:
            msg=f"there is {e}"
            return render_template("login.html",msg=msg) 
    return render_template("login.html")
@app.route("/home",methods=["GET","POST"])
def home():
      if request.method=="POST":
        print("method inside the post")
        log=float(request.form.get("log"))
        lat=float(request.form.get("lat"))
        house_median_age=float(request.form.get("avg_house_age"))
        total_rooms=float(request.form.get("Total_rooms"))
        total_bedrooms=float(request.form.get("total_bedrooms"))
        population=float(request.form.get("population"))
        households=float(request.form.get("households"))
        median_income=float(request.form.get("median_income"))
        house_data=pd.read_csv("housing.csv")

        print(house_data)
        x=house_data.drop(columns=["median_house_value","ocean_proximity"])
        y=house_data["median_house_value"]
        print(x)
        print(y)
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=111)
        # num_col=house_data.columns[:-2]
        # cat_col=house_data.columns[9:]
        # num_col=house_data.columns[:-2]
        # cat_col=house_data.columns[9:]
        num_pipeline=Pipeline([
        ("impute",SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
        ])
    
        num_pipeline.fit(x_train)
        x_train_tr=num_pipeline.transform(x_train)
        # x_test_tr= num_pipeline.transform(x_test)
        print( x_train_tr)
        print(y_train)
      
        model=LinearRegression()
        model.fit(x_train_tr,y_train)
        predict_val = model.predict([[log,lat,house_median_age,total_rooms,total_bedrooms,population, households,median_income]])
        print(predict_val)
        
        y_train_hat=model.predict(x_train_tr)
        print(r2_score(y_train,y_train_hat))
        print(mean_absolute_error(y_train,y_train_hat))
        score=r2_score(y_train,y_train_hat) 
        error=mean_absolute_error(y_train,y_train_hat)
        return render_template("data.html",mean_error=error,score=score,predict_val=predict_val) 
      return render_template("home.html")
  
@app.route("/data",methods=["GET","POST"])
def data():
    return render_template("data.html")
app.run()