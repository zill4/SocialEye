# SocialEye
_The original SocialEye backend. Built using Flask, swagger, gunicorn, and Nginx._

Originally SocialEye was meant to be a Chrome extension that determined if the company you were buying from on Amazon was ethically responsible or not.
The issue and reason for discontinuing this strategy was that information to determine the ethicality of most companies is private, and non-conclusive.

The original data was scraped using BeautifulSoup from websites like B-Corp and Good Companies websites.


The code for the SocialEye API can be broken down into 3 different file types...

# API Specification through Yaml
The Swagger.yml file details the methods that can be called to access different pieces of the API.
These are broken down into Brands in general, Good Company sourced brands, and B-Corp sourced Brands (people is left over boiler plate for testing my API).

# Functions
The B_corp.py, G_comp.py, and brand.py accessed my MongoDB database checked if it was populated and made it accessible through the defined API in the Yaml doc.


# Application specifics
This application was then hosted on a Linux AWS machine that was set up with the micro-service Gunicorn that connected me to the load balance Nginx such that my API was then accessible and returned reliable responses.
