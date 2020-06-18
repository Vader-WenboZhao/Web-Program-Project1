import os

from flask import Flask, render_template, request
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, jsonify, request



res = requests.get("http://127.0.0.1:5000/api/detail/0099771810")
if res.status_code != 200:
    raise Exception("ERROR: API request unsuccessful.")
data = res.json()
print(data)
