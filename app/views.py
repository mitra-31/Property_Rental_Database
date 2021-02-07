from app import app,mysql,save_images,save_image
from flask import render_template,url_for,request,redirect,session
from datetime import datetime

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id,user_name,password FROM users WHERE user_name = '{0}'".format(username))
        auth = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if auth[1] == username and auth[2] == password:
            session['userid'] = auth[0]
            return redirect("/dashboard")
        else:
            return redirect("/login")
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method =="POST":
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO users(user_name,email_id,phone,adress,city,password) 
                            VALUES(%s,%s,%s,%s)""",(username,email,phone,address,city,password))
        mysql.connection.commit()
        cur.close()
    return render_template("register.html")

@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
    if session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_name FROM users WHERE user_id = '{0}'".format(str(session['userid'])))
        username = cur.fetchone()
        cur.execute("SELECT p_id,p_sellername,p_address,p_city,p_cost,p_thumbnail FROM properties WHERE p_status = 'AVL'")
        Property = cur.fetchall() 
        mysql.connection.commit()
        cur.close()
        return render_template("dashboard.html",username=username[0].upper(),properties=Property)
    
@app.route("/profile",methods=["POST","GET"])
def profile():
    if session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = '{0}'".format(str(session['userid'])))
        UserDetails = cur.fetchone()
        cur.execute(""" SELECT COUNT(p_sellername) 
                        FROM properties  
                        WHERE p_sellername = '{0}'
                        """.format(session['userid']))
        sell = cur.fetchone()
        cur.execute(""" SELECT COUNT(user_id) 
                        FROM sold_properties  
                        WHERE user_id = '{0}'
                        """.format(session['userid']))
        buy = cur.fetchone()
        print(buy)
        mysql.connection.commit()
        cur.close()
        return render_template("profile.html",User=UserDetails,buy=buy[0],sell=sell[0])

@app.route("/logout")
def logout():
    session.pop('userid',None)
    return render_template("home.html")

@app.route("/sell",methods=["POST","GET"])
def sell():
    if session:
        if request.method == "POST":
            price = request.form.get("price")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("z_code")
            thumbnail = save_image(request.files.get("thumbnail"))
            images = request.files.getlist("files[]")
            image = ""
            for img in images:
                image += img.filename +","
            for img in images:
                save_image(img)
            cur = mysql.connection.cursor()
            cur.execute("""INSERT INTO properties(p_sellername,p_address,p_city,p_state,p_zipcode,p_images,p_cost,p_thumbnail,p_status)  
                                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                                    (str(session['userid']),address,city,state,zipcode,image,price,thumbnail,'AVL'))
            mysql.connection.commit()
            cur.close()
    return render_template("selling.html")

@app.route("/buy" ,methods=["POST","GET"])
def buy():
    if session:
        if request.method == "POST":
            pseller = request.form.get("pseller")
            pid = request.form.get("pid")
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT u.user_name,u.email_id,u.phone,p.p_address,p.p_city,p.p_state,p.p_zipcode,p_cost,p_images,p_id,p_sellername
            FROM properties p, users u
            WHERE p.p_id = {0} AND p.p_sellername = {1}
            AND u.user_id = {1} """.format(pid,pseller))
            Property = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            images = Property[8].split(",")
    return render_template("property.html",Property=Property,images=images[1:],user=session['userid'])

@app.route("/payment",methods=["POST","GET"])
def payment():
    if session:
        if request.method == "POST":
            pid = request.form.get("pid")
            pseller = request.form.get("pseller")
            userid = request.form.get("userid")
            cur = mysql.connection.cursor()
            cur.execute("""
            SELECT p_cost
            FROM properties p, users u 
            WHERE p.p_id = {0} AND p.p_sellername = {1}
            AND u.user_id = {1} """.format(pid,pseller))
            cost = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            Total = int(cost[0]) + int(cost[0]) * 28/100        
    return render_template("payment.html",cost=cost[0],Total=Total,pid=pid,userid=session['userid'])

@app.route("/thankyou",methods=["POST","GET"])
def payment_():
    if session:
        print("heloo")
        if request.method == "POST":
            pid = request.form.get("pid")
            userid = request.form.get("userid")
            date = datetime.now()
            cur = mysql.connection.cursor()
            cur.execute(""" UPDATE properties SET p_status = 'sold' WHERE  p_id = {0}""".format(pid))
            cur.execute("INSERT INTO sold_properties(user_id,p_id,date_solded_out) VALUES(%s,%s,%s)",(userid,pid,date))
            mysql.connection.commit()
            cur.close()
    return render_template("thankyou.html")