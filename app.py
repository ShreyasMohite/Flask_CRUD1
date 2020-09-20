from flask import Flask,render_template,redirect,request,url_for,session
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField
from wtforms.validators import Email,Length,DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app=Flask(__name__)
app.config["SECRET_KEY"]="3UHJENDCASDO2IKJEBNHDC"
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:''@localhost/testdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
bootstrap=Bootstrap(app)


class Usser(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(30),nullable=False,unique=True)

    def __init__(self,name,email):
        self.name=name
        self.email=email

class Form(FlaskForm):
    name=StringField("Username",validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField("Submit")


@app.route("/")
@app.route("/home")
def home():
    user=Usser.query.all()
    return render_template("Home.html",title="Home",user=user)


@app.route("/add",methods=['GET','POST'])
def Adduser():
    form=Form()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        mydata=Usser(name,email)
        db.session.add(mydata)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('Adduser.html',title="Adduser",form=form)

@app.route("/delete/<id>",methods=['GET','POST'])
def delete(id):
    user=Usser.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit/<id>",methods=['GET','POST'])
def edit(id):
    user=Usser.query.get_or_404(id)
    form=Form()
    if form.validate_on_submit():
        user.name=form.name.data
        user.email=form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method=='GET':
        form.name.data=user.name
        form.email.data=user.email
    return render_template('Adduser.html',form=form,user=user)




if __name__ == "__main__":
    app.run(debug-True)