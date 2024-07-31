"""
source venv/Scripts/activate
export FLASK_DEBUG=1
flask run
"""

from flask import Flask, render_template
import csv, os, locale
from datetime import datetime
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
    data["skills"].sort(key=lambda x: int(x["Years"]), reverse=True)
    data["communications"].sort(key=lambda x: x["Date"], reverse=True)
    data["experiences"].sort(key=lambda x: x["StartDate"], reverse=True)
    data["projects"].sort(key=lambda x: x["StartDate"], reverse=True)
    return data

"""emplois = [post for post in data["experiences"] if post["Type"] == "emploi"]
for item in emplois:
    print(item["Skills"])
    print(org["Skills"])
    any(f in item["Skills"].split(',') for f in (org["Skills"]).split(','))"""

app = Flask(__name__)
@app.route('/resume')
def resume():
    data = load_data()
    emplois = [post for post in data["experiences"] if post["Type"] == "emploi"]
    skips = ["Maîtrise en philosophie", "Coordonnateur·trice du comité Techno-Secours"] #Things to skips
    return render_template('resume.html', data=data, emplois = emplois, FirstPage = 5, highlighted_skills=[], skips=skips)

@app.route('/cover/<idKey>')
def cover(idKey):
    data = load_data()
    org = [post for post in data["orgs"] if post["IdKey"] == idKey][0]
    skills = org["Skills"].split(', ')

    if len(skills) > 2:
        highlighted_skills = skills[:3]
    skilled = [skill for skill in data["skills"] if skill['Titre'] in highlighted_skills]

    if not "Philosophie" in skills:
        skills.append("Services de santé")


    for category in data.keys():
        if category not in ['user', 'skills']:
            data[category] = [post for post in data[category] if 
                any(f in post["Skills"].split(', ') for f in skills)
                ]
    
    emplois = [post for post in data["experiences"] if post["Type"] == "emploi" and (
               any(f in post["Skills"].split(', ') for f in skills))]
   
    
    with open(f"static/{org['Type']}.txt", encoding="utf-8") as f:
        text = [line for line in f]
    return render_template('cover.html', data=data, emplois = emplois, cover=True, date=date, skills=skills, org=org, text=text, highlighted_skills=highlighted_skills, skilled=skilled, skips=[])


if __name__ == '__main__':
   app.run(debug=True)    