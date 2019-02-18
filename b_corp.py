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
# _url = "https://scrapehero-amazon-product-info-v1.p.rapidapi.com/product-details?asin="
# Create header containing API Key
header = {"X-RapidAPI-Key": "96e175c4f2msh29b17f9b8ee6d33p17dc8ajsn17397f8f8e7d"}

# Create MongoDB client
# set uri
uri = 'mongodb+srv://Crisp-admin:P1ezill4P1e@socialeye1-2fwwc.mongodb.net/admin'
client = MongoClient(uri)

# Connect to specific database in MongoDB instance
db = client['API']

# Connec to specific collection in MongoDB instance
collection = db['b_corp']

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """
    This function responds to a request for /api/b_corp
    with the complete lists of good companies
    :return:        json string of list of companies
    """
    # Returns all from MongoDB collection.
    comps = collection.find({})
    c = {}
    collect = []
    for doc in comps:
        if doc['timestamp']:
            c['timestamp'] = doc['timestamp']
        if doc['bname']:
            c['bname'] = doc['bname']
        if doc['url']:
            c['url'] = doc['url']
            collect.append(c.copy())
    print('------------------------------------------')
    print(collect)
    return collect


def read_one(bname):
    """
    This function responds to a request for /api/b_corp/{bname}
    with one matching company from good companies
    :param lname:   brand name of good company to find
    :return:        brand matching good company name
    """

    # Does this brand exist within brand collection?
    if collection.find_one({"bname": bname}):
        company = collection.find_one({"bname": bname})

    # otherwise, nope, not found
    else:
        abort(
            404, "Good Company with brand name {bname} not found".format(bname=bname)
        )
    return b_corp


def create(b_corp):
    """
    This function creates a new brand in the brand structure
    based on the passed in brand data
    :param person:  brand to create in brand structure
    :return:        201 on success, 406 on person exists
    """
    bname = b_corp.get("bname", None)
    url = b_corp.get("url", None)
    # Does the good company exist already?
    if not collection.find_one({"bname": bname, "bname": bname,}):
        db.b_corp.insert_one({
            "bname": bname,
            "url": url,
            "timestamp": get_timestamp(),
        })
        return make_response(
            "{bname} successfully created".format(bname=bname), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Good Company with brand name {bname} already exists".format(bname=bname),
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
        collection.update_one({"bname": bname}, {"bname": b_corp.get("bname")})
        collection.update_one({"timestamp"}, {"timestamp": get_timestamp()})
        return b_corp[bname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Good Comapny with brand name {bname} not found".format(bname=bname)
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
            404, "Good Company with brand name {bname} not found".format(bname=bname)
        )