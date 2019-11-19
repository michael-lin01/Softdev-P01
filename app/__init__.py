import os

from flask import Flask, render_template, request, flash, redirect, session, abort

app = Flask(__name__)

app.secret_key = os.urandom(64)

@app.route('/')
def home():
    return render_template("base.html")
