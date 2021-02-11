from flask import Flask, render_template, request, redirect
from superscraper import superScraper
from exporter import exporter

db = {}

app = Flask("DayLast")

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/search",methods=['GET'])
def search():
  keyword = request.args.get('keyword')
  keyword = keyword.lower()
  
  fromDb = db.get(keyword)
  if fromDb: # review the database
    full_results = fromDb
  else:
    full_results = superScraper(keyword)
    db[keyword] = full_results

  len_results = len(full_results)
  return render_template('search.html',keyword=keyword,full_results=full_results,len_results=len_results)

@app.route("/export")
def export():
  try:
    keyword = request.args.get('keyword')
    if not keyword:
      raise Exception()

    fromDb = db.get(keyword)
    if not fromDb: # review the database
      raise Exception()

    exporter(fromDb,keyword)
    return redirect("/")
  except:
    print("error")
    return redirect("/")
  
app.run()