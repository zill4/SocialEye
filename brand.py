# brand.py 
# Given an ASIN calls RapidAPI and populates DB with brand names.
# TODO: add file for handling requests for Crunchbase, Glassdoor, Yahoo Finance.
"""
This is the brand module and supports all the ReST actions for the
BRAND collection
"""
# Add bson to json dump for pymongo util
from bson.json_util import dumps

# Added for simpler debugging
import pprint

# JSON for parsing 3rd party responses requests
import json

# Request 3rd party API's 
import requests

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort

from pymongo import MongoClient

# Create url for request to 3rd Party API's
url = "https://scrapehero-amazon-product-info-v1.p.rapidapi.com/product-details?asin="
# Create header containing API Key
header = {"X-RapidAPI-Key": "96e175c4f2msh29b17f9b8ee6d33p17dc8ajsn17397f8f8e7d"}

# Create MongoDB client
# set uri
uri = 'mongodb+srv://Crisp-admin:P1ezill4P1e@socialeye1-2fwwc.mongodb.net/admin'
client = MongoClient(uri)

# Connect to specific database in MongoDB instance
db = client['API']

# Connec to specific collection in MongoDB instance
collection = db['brand']

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """
    This function responds to a request for /api/brand
    with the complete lists of brands
    :return:        json string of list of brands
    """
    # Returns all from MongoDB collection.
    brands = collection.find({})
    c = {}
    collect = []
    for doc in brands:
        if doc['timestamp']:
            c['timestamp'] = doc['timestamp']
        if doc['bname']:
            c['bname'] = doc['bname']
            print (c)
            collect.append(c.copy())
    print('------------------------------------------')
    print(collect)
    return collect


def read_one(bname):
    """
    This function responds to a request for /api/people/{bname}
    with one matching brand from brands
    :param lname:   brand name of brand to find
    :return:        brand matching brand name
    """

    # Does this brand exist within brand collection?
    if collection.find_one({"bname": bname}):
        brand = collection.find_one({"bname": bname})

    # otherwise, nope, not found
    else:
        abort(
            404, "Brand with brand name {bname} not found".format(bname=bname)
        )
    return brand

def get_by_asin(asin):
    """
    This function responds to a request for /api/brand/{asin}
    with one matching brand from brands.
    If brand is not in database, it is added.
    :param asin:    product id<string> from amazon to match to brand.
    :return:        brand matching asin brand name.
    """
    # Make http request given asin to RapidAPI.
    r = requests.get(url + asin, headers=header)  
    # Check if request returns good
    if r.status_code == 200:
        # Loads response into a dictionary
        data = json.loads(r.text)
        if data['brand']:
            brand = {'bname': data['brand']}
            create(brand)
        else:
            abort(
                404, "Asin {asin} not valid".format(asin=asin)
            )
    else:
        abort(
            404, "Asin {asin} not valid".format(asin=asin)
        )
    return brand
        

def create(brand):
    """
    This function creates a new brand in the brand structure
    based on the passed in brand data
    :param person:  brand to create in brand structure
    :return:        201 on success, 406 on person exists
    """
    bname = brand.get("bname", None)

    # Does the brand exist already?
    if not collection.find_one({"bname": bname, "bname": bname,}):
        db.brand.insert_one({
            "bname": bname,
            "timestamp": get_timestamp(),
        })
        return make_response(
            "{bname} successfully created".format(bname=bname), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Peron with last name {bname} already exists".format(bname=bname),
        )


def update(bname, brand):
    """
    This function updates an existing brand in the brand structure
    :param lname:   brand name of person to update in the brand structure
    :param person:  brand to update
    :return:        updated brand structure
    """
    # Does this brand exist within people collection?
    if collection.find_one({"bname": bname}):
        collection.update_one({"bname": bname}, {"bname": brand.get("bname")})
        collection.update_one({"timestamp"}, {"timestamp": get_timestamp()})
        return brand[bname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {bname} not found".format(bname=bname)
        )


def delete(bname):
    """
    This function deletes a brand from the brand structure
    :param lname:   brand name of brand to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does this person exist within people collection?
    if collection.find_one({"bname": bname}):
        collection.delete_one({"bname": bname})
        return make_response(
            "{bname} successfully deleted".format(bname=bname), 200
        )
    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {bname} not found".format(bname=bname)
        )