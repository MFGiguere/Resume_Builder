parameters = {
    "type": "plain", #plain or fancy are the choices
    "projects": True, #Wheter your resume contains a "project" sections for IT or research project. Projects are defined in projects.csv. 
    "skips": [], #Things to skips by default on resume
    "skills": ["Services de santé", "Soutien informatique", "Analyse de données"], #Skills to use by default to filter experiences on resume
    "dateFormat": "%b %Y", #For date format. (not yet implemented)
    "sections": ["certifications", "projets-techno", "projects-recherche"], #List of optional sections in page 2 of the resume. ["benevolat", "certifications", "communications", "projets-techno", "projects-recherche"]
    "intro": "Je suis à la recherche d'expériences qui me permettront de développer mes compétences professionnelles afin d'intégrer à temps plein le domaine de la recherche."#Overrides aboutme if not empty. 
}