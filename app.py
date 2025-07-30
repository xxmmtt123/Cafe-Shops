from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=True)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[str] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[str] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[str] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[str] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))

    # Optional: this will allow each cafe object to be identified by its title when printed.
    def __repr__(self):
        return f'<Cafe {self.name}>'
with app.app_context():
    db.create_all()
    
# with app.app_context():
#     cafes = Cafe.query.all()
#     for cafe in cafes:
#         print(cafe.coffee_price)

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField("Cafe location on Google Maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location name", validators=[DataRequired()])
    has_sockets = SelectField("Has sockets", choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    has_toilet = SelectField("Has toilet", choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    has_wifi = SelectField("Has Wifi", choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    can_take_calls = SelectField("Can take calls", choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Average coffee price', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    result = db.session.execute(
        db.select(Cafe)
    )
    all_cafes = result.scalars().all()
    return render_template("index.html", all_cafes=all_cafes)

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            has_wifi=bool(int(form.has_wifi.data)),
            has_toilet=bool(int(form.has_toilet.data)),
            has_sockets=bool(int(form.has_sockets.data)),
            can_take_calls=bool(int(form.can_take_calls.data)),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)