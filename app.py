#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = "Albin TCHOPBA"
# __copyright__ = "Copyright 2020 Albin TCHOPBA and contributors"
# __credits__ = ["Albin TCHOPBA and contributors"]
# __license__ = "GPL"
# __version__ = "3"
# __maintainer__ = "Albin TCHOPBA"
# __email__ = "Albin TCHOPBA <atchopba @ gmail dot com"
# __status__ = "Production"


from flask import Flask, render_template, request, redirect
import treatment as t
from treatment import UrlClass

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", urls=UrlClass().get_all_urls())

@app.route("/reinit")
def reinit_db():
    UrlClass().reinit_db()
    return redirect("/")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    url_ = request.form["url"]
    url_short = t.generate_url()
    print("=> url_short : "+ url_short)
    turl = t.TURL(url_, url_short)
    id_ = UrlClass().insert_url(turl)
    if id_:
        return redirect("/")
    else:
        return render_template("index.html", urls=UrlClass().get_all_urls(), error_msg="Erreur produite! Veuillez recommencer!" )

@app.route("/delete/<int:id_>")
def delete_url(id_):
    UrlClass().delete_url(id_)
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
