"""
source venv/Scripts/activate
export FLASK_DEBUG=1
flask run
"""

from flask import Flask, render_template
import csv, os, locale
from datetime import datetime
#import plotly.figure_factory as ff
#import plotly.express as px
from textwrap import wrap

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

date = datetime.today().strftime("%d %B %Y")

def load():
    """
    Load all csv files from static into data as their name
    """
    d = {}
    directory = os.getcwd()
    static = os.path.join(directory,"static/data")
    for file in os.listdir(static):
        if file.endswith(".csv"):
            with open(f"{static}/{file}", 'r', encoding='utf-8') as csvfile:
                name = os.path.basename(file).split(".")[0]
                spamreader = csv.DictReader(csvfile, delimiter=";", quotechar='|')
                rows = []
                for row in spamreader:
                    rows.append(row)
                d[name] = rows
    return d

def load_data():
    data = load()
    data["skills"].sort(key=lambda x: int(x["YoE"]), reverse=True)
    data["communications"].sort(key=lambda x: x["Date"], reverse=True)
    data["experiences"].sort(key=lambda x: x["StartDate"], reverse=True)
    data["projects"].sort(key=lambda x: x["StartDate"], reverse=True)
    data["etudes"].sort(key=lambda x: x["StartDate"], reverse=True)
    return data

def load_txt():
    """
    Load all csv files from static into data as their name
    """
    d = {}
    directory = os.getcwd()
    static = os.path.join(directory,"static/txt/frq")
    for file in os.listdir(static):
        if file.endswith(".txt"):
            with open(f"{static}/{file}", 'r', encoding='utf-8') as f: 
                name = os.path.basename(file).split(".")[0]
                text = f.read()
                text = text.replace("*", "·")
                text = text.split("\n")
                d[name] = text
    return d

def filter(data, skills):
    if not "Philosophie" in skills and not "Services de santé" in skills:
        skills.append("Services de santé")
    highlighted_skills = skills
    if len(skills) > 2:
        highlighted_skills = skills[:3]
    skilled = [skill for skill in data["skills"] if skill['Title'] in highlighted_skills]
    
    #Filter all categories so that only relevant skills are present
    for category in data.keys():
        if category not in ['user', 'skills', 'echeanciers']:
            data[category] = [post for post in data[category] if 
                any(f in post["Skills"].split(', ') for f in skills)
                ]
            
    #Changes actual job to today and adds the possibility of changing dateformat too. 
    for category in data.keys(): 
        if category not in ['user', 'skills', 'echeanciers', 'orgs']:
            for post in data[category]:
                if category == "communications":
                    post["Date"] = datetime.strptime(post["Date"], "%Y-%m-%d").strftime("%Y")
                else:
                    post["StartDate"] = datetime.strptime(post["StartDate"], "%Y-%m-%d").strftime("%b %Y")
                    if post["EndDate"] == "9999" or post["EndDate"] =="":
                        post["EndDate"] = "auj.  "
                    else:
                        post["EndDate"] = datetime.strptime(post["EndDate"], "%Y-%m-%d").strftime("%b %Y")
                

    #Changes all * to · for neutral words (in french)
    for category in data.keys(): 
        if category not in ['user', 'echeanciers']:
            for post in data[category]:
                for entry in post.keys():
                    try:
                        post[entry] = post[entry].replace("*", "·")
                    except:
                        pass
    
    relevant_jobs = [post for post in data["experiences"] if post["Type"] == "emploi" and 
                     any(f in post["Skills"].split(', ') for f in skills)][:2]
    
    emplois = [post for post in data["experiences"] if post["Type"] == "emploi" and post not in relevant_jobs]
    
    """emplois = [post for post in data["experiences"] if post["Type"] == "emploi" and ((
               any(f in post["Skills"].split(', ') for f in skills)) and post not in relevant_jobs)]"""
    
    certif = [post for post in data["etudes"] if post["Type"] == "certification"]

    """
    Change all * to the stuff.
    """
    
    return (highlighted_skills, skilled, data, emplois, certif, relevant_jobs)

app = Flask(__name__)
@app.route('/resume')
def resume():
    skips = ["Maîtrise en philosophie", "Coordonnateur·trice du comité Techno-Secours"] #Things to skips
    skills = ["Gestion de projets", "Analyse de données", "Soutien informatique"]
    FirstPage = 4
    data = load_data()
    highlighted_skills, skilled, data, emplois, certif, relevant_jobs = filter(data, skills)
    return render_template('resume.html', data=data, emplois = emplois, FirstPage=FirstPage, highlighted_skills=highlighted_skills, skips=skips, certif=certif, relevant_jobs=relevant_jobs)

@app.route('/cover/<type>/<idKey>')
def cover(idKey, type):
    data = load_data()
    org = [post for post in data["orgs"] if post["IdKey"] == idKey][0]
    skills = org["Skills"].split(', ')
    highlighted_skills, skilled, data, emplois, certif, relevant_jobs = filter(data, skills)
    FirstPage=4
    with open(f"static/txt/cv/{org['Type']}.txt", encoding="utf-8") as f:
        text = [line.replace("*", "·") for line in f]

    if type == "plain":
        return render_template('cover_plain.html', data=data, emplois = emplois, cover=True, date=date, skills=skills, org=org, text=text, highlighted_skills=highlighted_skills, skilled=skilled, skips=[], certif=certif, relevant_jobs=relevant_jobs)
    
    else:
        return render_template('cover.html', data=data, FirstPage=FirstPage, emplois = emplois, cover=True, date=date, skills=skills, org=org, text=text, highlighted_skills=highlighted_skills, skilled=skilled, skips=[], certif=certif, relevant_jobs=relevant_jobs)

@app.route('/<variable>')
def generic(variable):
    data = load_data()
    texts = load_txt()
    return render_template(f"/frq.html", variable=variable, data=data, texts=texts)

@app.route('/frq/<item>')
def frq(item):
    data = load_data()
    texts = load_txt()
    emplois = [post for post in data["experiences"] if post["Type"] == "emploi"]
    return render_template(f"/frq/{item}.html", data=data, item=item, texts=texts, emplois=emplois)

@app.route('/crsh/<item>')
def crsh(item):
    data = load_data()
    texts = load_txt()
    emplois = [post for post in data["experiences"] if post["Type"] == "emploi"]
    return render_template(f"/frq/{item}.html", data=data, item=item, texts=texts, emplois=emplois, crsh=True)

@app.route("/gantt")
def create_img():
    data = load_data()
    df = [dict(Task=d['task'], Start=d['start'], Finish=d['end'], Resource=d["category"]) for d in data["echeanciers"]]
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource", width=700, height=600)
    fig.update_yaxes(showgrid=True)
    fig.update_xaxes(showgrid=True)
    fig.update_layout( # customize font and legend orientation & position
    font_family="Times",
    font_size=12,
    margin=dict(l=20, r=20, t=20, b=20),
    )
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    title="Catégories",
    y=1.02,
    xanchor="right",
    x=1
    ))
    img = fig.to_html()
    #fig.write_image("static/img/gantt.jpeg")
    return  img


if __name__ == '__main__':
   app.run(debug=True)    