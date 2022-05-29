# CK-BE
A FastAPI Backend

[![Build Status](https://app.travis-ci.com/TheCodingKittens/CK-BE.svg?branch=main)](https://app.travis-ci.com/TheCodingKittens/CK-BE)
[![Coverage Status](https://coveralls.io/repos/github/TheCodingKittens/CK-BE/badge.svg?branch=main)](https://coveralls.io/github/TheCodingKittens/CK-BE?branch=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=TheCodingKittens_CK-BE&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=TheCodingKittens_CK-BE)

A Fastapi Backend that will communicate with the frontend

Integration with FastAPI.
=========================

To test, first, start the server:

    $ docker-compose up

After the Docker build is complete you can view the documentation here:

    http://localhost:8000/docs

You can view the info about the redis database here:

    http://localhost:8001/

You might need to enter the following info:

    host: redis
    port: 6379
    
You are able to see the data in the Redis DB:

![image](https://user-images.githubusercontent.com/19205392/170887384-b7b3759c-91b5-4138-a25b-9471cc3d64be.png)

