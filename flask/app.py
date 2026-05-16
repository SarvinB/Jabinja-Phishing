from flask import Flask, render_template, request
from flask import Response
import subprocess
import json
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
session = requests.Session()
login_check = False
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
data = {}

@app.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    
    global login_check
    global data
    
    if login_check is False:
    
        login_url= "https://jobinja.ir/login/user"
        username = request.form.get("identifier")
        password = request.form.get("password")

        r = session.get(login_url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        csrf = soup.find("input", {"name": "_token"})["value"]

        payload = {
            "identifier": username,
            "password": password,
            "_token": csrf
        }
        
        response = session.post(login_url, data=payload, headers=headers)
        
        if "ورود" in response.text:

            print("*********", response.status_code)
            return render_template("login.html") 
        
        else:
            
            login_check = True
            
            data = get_jobs_applied()
            
            with open("jobs_applied.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            html = get_html("https://jobinja.ir/", "templates/home.html")
                
            return Response(html, mimetype="text/html") 
    else:
        
        data = get_jobs_applied()
        
        with open("jobs_applied.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        html = get_html("https://jobinja.ir/", "templates/home.html")
        
        return Response(html, mimetype="text/html") 
    
@app.route("/jobs/applied/<job_id>/details")
def job_detail(job_id):
    return render_template("login.html") 

@app.route("/<path:any_path>")
def catch_all(any_path):
    
    try:
        html = get_html("https://jobinja.ir/" + any_path)
        return Response(html, mimetype="text/html") 
    
    except:
        
        html = get_html("https://jobinja.ir/")
        return Response(html, mimetype="text/html") 
    
def get_html(url, name="page.html"):

    r = session.get(url, headers=headers)

    replacements = {
        "https://jobinja.ir":
            "http://127.0.0.1:5000",

        "http://127.0.0.1:5000/assets/css/end_user":
            "https://jobinja.ir/assets/css/end_user",

        "{{ data.link }}":
            "http://127.0.0.1:5000/jobs/applied",

        "{{application.details_link}}#similar_job_section":
            "http://127.0.0.1:5000/jobs",

        "{{application.details_link}}":
            "http://127.0.0.1:5000/jobs",

        "{{ application.job_link }}":
            "http://127.0.0.1:5000/jobs/applied",
    }

    html = r.text

    for old, new in replacements.items():
        html = html.replace(old, new)
        
    return html

def get_jobs_applied():
    
    url = "https://jobinja.ir/api/v10/jobs/applied"
    r = session.get(url, headers=headers)
    
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)