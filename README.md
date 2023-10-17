# NYU DevOps Project: Inventory
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)


## Overview

This is a repository is the project of the **Inventory Squad** for the NYU masters class **CSCI-GA.2820-001 DevOps and Agile Methodologies**. This project is a [Flask](https://flask.palletsprojects.com/) app contains one inventory of all of the products that an e-commerce web site sells. And keep track of the detailed information of the inventory items (id, name, quantity, condition etc.) with the [SQLAlchemy](https://www.sqlalchemy.org/) database model. Also, the app implements the management features like **Add**, **Get**, **Delete**, **Update** and **List** (not yet implemented) items in the inventory database by using the RESTful API.

## Run
The Flask app now runs on the local machine. To start the app, type the following command in the shell:

```bash
make run
```

After the shell showing the message indicate the app is running successfully, you can access the homepage of the app and use RESTful API to interact with the app.

To access the home page of the app, you can go to <http://localhost:8000/>. This page will provide you some information about the app.

## RESTful API usage

To create a new item in the inventory, you can use the directory `/inventory` of the app with the method of `POST`.

To get an item with specified id, you can use the directory `/inventory/<iid>` of the app with the method of `GET`, where `<iid>` is the id of the item.

To update an item, you can use the directory `/inventory/<iid>` of the app with the method of `PUT`, where `<iid>` is the id of the item.

To delete an item, you can use the directory `/inventory/<iid>` of the app with the method of `DELETE`, where `<iid>` is the id of the item.

## Test

The development of the project follows TDD practices. The tests are in the directory `./tests`. Now the test coverage is 96%. To run the tests, type the following command in the shell:

```bash
make test
```
