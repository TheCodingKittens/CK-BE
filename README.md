# CK-BE

A Fastapi Backend that will communicate inbetween the CLI & the frontend. 



"""
Integration with FastAPI.
=========================

To test, first, start the server:

    $ poetry run uvicorn async_main:app

Then, in another shell, create a customer:

    $ curl -X POST  "http://localhost:8000/customer" -H 'Content-Type: application/json' -d '{"first_name":"Andrew","last_name":"Brookins","email":"a@example.com","age":"38","join_date":"2020
-01-02"}'
    {"pk":"01FM2G8EP38AVMH7PMTAJ123TA","first_name":"Andrew","last_name":"Brookins","email":"a@example.com","join_date":"2020-01-02","age":38,"bio":""}

Get a copy of the value for "pk" and make another request to get that customer:

    $ curl "http://localhost:8000/customer/01FM2G8EP38AVMH7PMTAJ123TA"
    {"pk":"01FM2G8EP38AVMH7PMTAJ123TA","first_name":"Andrew","last_name":"Brookins","email":"a@example.com","join_date":"2020-01-02","age":38,"bio":""}

You can also get a list of all customer PKs:

    $ curl "http://localhost:8000/customers"
    {"customers":["01FM2G8EP38AVMH7PMTAJ123TA"]}
"""
