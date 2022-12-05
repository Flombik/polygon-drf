# Polygon-DRF

[![codecov](https://codecov.io/gh/pavellos21/polygon-drf/branch/main/graph/badge.svg?token=CLFC2117Y7)](https://codecov.io/gh/pavellos21/polygon-drf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Lint & Test](https://github.com/pavellos21/polygon-drf/actions/workflows/lint-and-test.yml/badge.svg?branch=main)](https://github.com/pavellos21/polygon-drf/actions/workflows/lint-and-test.yml)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## About

This is an example of an app that uses polygons to store service areas and then filter by them.
The main goal is to be able to store destination locations without using addresses, zip codes, city names, etc.

If you are looking for something similar, but from a more reputable vendor, take a look at
Google's [Plus Codes](https://plus.codes/). They are designed to accomplish the same goal.

Demo version of the application is hosted on Amazon Web Services.
You're able to check it out [here](http://ec2-3-69-178-101.eu-central-1.compute.amazonaws.com/).

## Usage

The API docs located on `/api/schema/swagger`. I believe that all existing endpoints are covered there.

Some minor notes about filtering service areas:

1. There are 2 query string parameters that was designed for is: `geo_info` and `point`.
2. The first one (`geo_info`) takes GeoJSON compatible data, for instance:
   `/servise-areas/?geo_info={ "type": "Point", "coordinates": [ -5, 10 ] }`
3. The second one (`point`) takes two comma-separated coordinates, for example:
   `/servise-areas/?point=-5,10`
4. If input data incorrect, you'll receive a `400 Bad Request` error code.

## Implementation

To implement this application I've used [Django](https://www.djangoproject.com/)
with [Django Rest Framework](https://www.django-rest-framework.org/) and a little pinch of necessary add-ons.

As a database solution I've chosen [PostgreSQL](https://www.postgresql.org/) with [PostGIS](https://postgis.net/)
extension for it. Exactly PostGIS is the centerpiece of the
project because it provides easy and efficient solution for storing and querying geographical data.

For testing, I've used Django's built-in utilities and the [Factory Boy](https://factoryboy.readthedocs.io/) library to
generate test data.
Test coverage is checked with [Coverage.py](https://coverage.readthedocs.io/).

Automatic deployment to AWS is done on CI using GitHub Actions.