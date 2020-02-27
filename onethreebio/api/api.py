import flask
from flask import request, jsonify, abort
import os, sys
parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentdir)
from lib import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Drug scraping api</h1><p>Route is /api?drug_id=</p>\n"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The drug_id cannot be found.</p>", 404

@app.errorhandler(405)
def gene_not_found(e):
    return "<h1>405</h1><p>The drug_id doesn't have target gene.</p>", 405

# A route to return all of the available entries in our catalog.
@app.route('/api', methods=['GET'])
def api_main():

    query_parameters = request.args

    drug_id = query_parameters.get('drug_id')

    drugurl = create_drugurl(drug_id)
    res, code = process_drugurl(drugurl)

    if code == 200:
        print("retrieving gene info " + drug_id + " successful")
        return jsonify(res), code
    else:
        abort(code, description="Gene not found")


app.run()
