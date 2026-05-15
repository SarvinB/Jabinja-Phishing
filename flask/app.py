from flask import Flask, render_template, request
from flask import Response
import subprocess
import json
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
data = {}

# your custom logic that generates next HTML content
# render_template("https%3A%2F%2Fjobinja.ir.html")
# https%3A%2F%2Fjobinja.ir%2Fcv-builder

@app.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    
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

    # headers = {
    #     "Referer": login_url,
    #     # "X-Requested-With": "XMLHttpRequest",
    #     "User-Agent": "Mozilla/5.0"
    # }

    response = session.post(login_url, data=payload, headers=headers)
    
    if "ورود" in response.text:
        
        # print(response.status_code)
        # print(response.url)
        # print(response.headers)
        # print(username, password)
        
        # html = get_html("https://jobinja.ir")
        # with open("templates/home.html", "w", encoding="utf-8") as f:
        #     f.write(html)
        # return Response(html, mimetype="text/html")

        print("*********", response.status_code)
        return render_template("login.html") 
    
    else:
        
        global data
        data = get_jobs_applied()
        
        with open("jobs_applied.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        html = get_html("https://jobinja.ir/", "templates/home.html")
        

        # with open("templates/home.html", "r", encoding="utf-8") as f:
        #     html = f.read()
            
        return Response(html, mimetype="text/html") 
    
@app.route("/jobs/applied/<job_id>/details")
def job_detail(job_id):
    return render_template("login.html") 

@app.route("/<path:any_path>")
def catch_all(any_path):
    
    # html = get_html("https://jobinja.ir/jobs/applied")
    try:
        html = get_html("https://jobinja.ir/" + any_path)
        return Response(html, mimetype="text/html") 
    
    except:
        
        html = get_html("https://jobinja.ir/")
        return Response(html, mimetype="text/html") 
    
def get_html(url, name="page.html"):

    r = session.get(url, headers=headers)
    
    # print(r.text)
    

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
    
    # soup = BeautifulSoup(r.text, "html.parser")
    
    # for tag in soup.find_all("a", href=True):
        
    #     if "https://jobinja.ir/assets/css/end_user" in tag["href"]:
    #         pass
        
    #     elif "jobinja.ir" in tag["href"]:
    #         tag["href"] = tag["href"].replace(
    #             "https://jobinja.ir/",
    #             "http://127.0.0.1:5000/"
    #         )
    
    # with open(name, "w", encoding="utf-8") as f:
    #     f.write(html)
        
    return html

def get_jobs_applied():
    
    url = "https://jobinja.ir/api/v10/jobs/applied"
    r = session.get(url, headers=headers)
    
    return r.json()

    # print(data["applications"]["data"][0]["short_id"])
    
# def get_job_details_url():

#     applications = []
    
#     for job in data["applications"]["data"]:
        
#         dict = {"short_id": job["short_id"], "details_link": job["details_link"]}
        
#         applications.append(job["details_link"])
    
#     # applications = json.dumps(applications)
#     return str(applications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)