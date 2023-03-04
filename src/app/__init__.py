from flask import Flask, render_template , request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db=SQLAlchemy(app)
#db.init_app(app)

class Data(db.Model):
    _tablename_ = "data"

    id = db.Column(db.Integer, primary_key=True)
    rna_id = db.Column(db.String(30), nullable=True) 
    rna_id_ex = db.Column(db.String(30), nullable=True)
    gestion = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/assos')
def assos():
    datas = Data.query.limit(10).all()
    return render_template('assos.html', datas=datas)

@app.route('/delete/<int:data_id>')
def delete(data_id):
    data = Data.query.get(data_id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('assos'))

@app.route('/modifier/<int:data_id>', methods=['GET', 'POST'])
def modifier(data_id):
    data = Data.query.get(data_id)

    if request.method == 'POST':
        data.rna_id = request.form['rna_id']
        data.rna_id_ex = request.form['rna_id_ex']
        data.gestion = request.form['gestion']
        db.session.commit()
        return redirect(url_for('assos'))
    return render_template('modifier.html', data=data)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        rna_id = request.form['rna_id']
        rna_id_ex = request.form['rna_id_ex']
        gestion = request.form['gestion']
        new_data = Data(rna_id=rna_id, rna_id_ex=rna_id_ex, gestion=gestion)
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('assos'))
    return render_template('ajouter.html')

@app.route('/statistiques')
def statistiques():
    datas = Data.query.all()

    # Préparer les données pour le graphique Plotly
    gestion_count = {}
    for d in datas:
        if d.gestion in gestion_count:
            gestion_count[d.gestion] += 1
        else:
            gestion_count[d.gestion] = 1

    gestion_values = list(gestion_count.values())
    gestion_labels = list(gestion_count.keys())
    data = {
        'data': [{'values': gestion_values, 'labels': gestion_labels, 'type': 'pie'}],
        'layout': {'title': 'Répartition des données par gestion'}
    }

    # Renvoyer la page HTML de statistiques avec le graphique Plotly
    return render_template('statistiques.html', graph_data=json.dumps(data))


if __name__ == '_main_':
    app.run()