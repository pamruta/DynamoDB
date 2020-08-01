
import boto3
import json
from boto3.dynamodb.conditions import Attr

# connect to database
dynamo = boto3.resource('dynamodb')
# load table
table = dynamo.Table('Artist')

# fetch data with given filters
def fetch_data(city_name="", country_name="", job_role="", tool=""):

    # filter by city
    if(city_name):
        filter_expr = Attr('address.city').eq(city_name)

    # filter by country
    if(country_name):

        try:
            filter_expr
        except NameError:
            filter_expr = Attr('address.country').eq(country_name)
        else:
            filter_expr = filter_expr & Attr('address.country').eq(country_name)

    # filter by job function
    if(job_role):

        try:
            filter_expr
        except NameError:
            filter_expr = Attr('skills').contains(job_role)
        else:
            filter_expr = filter_expr & Attr('skills').contains(job_role)

    # filter by tools and technologies
    if(tool):

        try:
            filter_expr
        except NameError:
            filter_expr = Attr('tools').contains(tool)
        else:
            filter_expr = filter_expr & Attr('tools').contains(tool)

    # scan table by applying filter conditions
    try:
        filter_expr
    except NameError:
        # no filters, scan entire table
        result = table.scan()
    else:
        # apply filter
        result = table.scan(FilterExpression=filter_expr)

    # return results
    return(json.dumps(result['Items'], indent=2))

# add new profile into database
def add_item(item):
    table.put_item(Item=item)

# create REST API with python flask
import flask
from flask import request
from flask import render_template
app = flask.Flask(__name__)

# root domain
@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

# API to fetch data from database
@app.route("/fetch", methods=['GET'])
def get_data():

    # filter data by location
    if 'city' in request.args:
        city = request.args['city']
    else:
        city = ""

    if 'country' in request.args:
        country = request.args['country']
    else:
        country = ""

    # filter data by technology, skill or job function
    if 'tool' in request.args:
        tool = request.args['tool']
    else:
        tool = ""

    if 'job_role' in request.args:
        job_role = request.args['job_role']
    else:
        job_role = ""

    return fetch_data(city_name=city, country_name=country, job_role=job_role, tool=tool)

# start service at given port
import sys
if(len(sys.argv) == 2):
    port_no = sys.argv[1]
else:
    port_no = 5000

app.run(host='0.0.0.0', port=port_no, debug=True)
