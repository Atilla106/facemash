# facemash [![Build Status](https://travis-ci.org/Atilla106/facemash.svg?branch=master)](https://travis-ci.org/Atilla106/facemash)
## Introduction

This a website whose main goal is to use Polymer (and sort wallpapers).
We also use Flask and sqlalchemy for the backend (but all the fun is in the elements ! :D)

## Install

### Front

```
npm install -g gulp bower
npm install
bower install
gulp test
```

### Back

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Run a local instance

### Front

`gulp serve`

### Back

`cd serve && python main.py`

## Deploy

`gulp` create all static files in `dist/`.
Use gunicorn to deploy the back

## Contribute

Feel free to submit issues & PRs, we love them !
