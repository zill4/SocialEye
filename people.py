
"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort

from pymongo import MongoClient

# Create MongoDB client

# set uri
uri = 'mongodb+srv://Crisp-admin:P1ezill4P1e@socialeye1-2fwwc.mongodb.net/admin'
client = MongoClient(uri)

# Connect to specific database in MongoDB instance
db = client['API']

# Connec to specific collection in MongoDB instance
collection = db['people']

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Returns all from MongoDB collection.
    people = collection.find({})
    c = {}
    collect = []
    for doc in people:
        if doc['timestamp']:
            c['timestamp'] = doc['timestamp']
        if doc['fname']:
            c['fname'] = doc['fname']
        if doc['lname']:
            c['lname'] = doc['lname']
            collect.append(c.copy())
    print('------------------------------------------')
    return collect
    # Create the list of people from our data
    #return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        person = PEOPLE.get(lname)

    # Does this person exist within people collection?
    if collection.find_one({"lname": lname}):
        person = collection.find_one({"lname": lname})

    # otherwise, nope, not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return person


def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # Does the person exist already?
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
    if not collection.find_one({"lname": lname, "fname": fname,}):
        db.people.insert_one({
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        })
        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Peron with last name {lname} already exists".format(lname=lname),
        )


def update(lname, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()
    # Does this person exist within people collection?
    if collection.find_one({"lname": lname}):
        collection.update_one({"fname": fname}, {"fname": person.get("fname")})
        collection.update_one({"timestamp"}, {"timestamp": get_timestamp()})
        return PEOPLE[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        # return make_response(
        #     "{lname} successfully deleted".format(lname=lname), 200
        # )
    # Does this person exist within people collection?
    if collection.find_one({"lname": lname}):
        collection.delete_one({"lname": lname})
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )
    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )