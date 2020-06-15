from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib

app = Flask(__name__)

engine = create_engine("mysql://root:123456@localhost/cbit")
db = scoped_session(sessionmaker(bind=engine))
# db.init_app(app)


# INSERT INTO user_sha1 VALUES ('member1',SHA1('secretpassword') );
# The magic...

@app.route("/")
def index():
	error_msg = " "
	return render_template("index.html", error_msg = error_msg)

@app.route("/super_admin", methods = ['POST'])
def super_admin():
	if request.method == 'POST':
		name = request.form.get("name")
		pword = request.form.get("pword")
		password = db.execute("SELECT * FROM super_admin where name=:name AND password=:password",{"name": name, "password":hashlib.sha1(pword.encode('utf-8'))})
		if password:
			return render_template("super_admin.html",name = name, pword = pword)
		else:
			return render_template("index.html", error_msg = "Wrong credentials", pword= pword, password = password)


@app.route("/admin", methods = ['POST'])
def admin():
	if request.method == 'POST':
		name = request.form.get("name")
		pword = request.form.get("pword")
		return render_template("admin.html",name = name, pword = pword)

if __name__ == "__main__":
	with app.app_context():
		main()