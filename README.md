# Spinny API CRUD assignment

## Base URL

This project has been deployed to pythonAnyWhere and the baseURL is [https://spinny.pythonanywhere.com](https://spinny.pythonanywhere.com/)

## How to access the API

A complete documenter has been setup for easy readability of APIs that you can find on : [https://documenter.getpostman.com/view/26991752/2s93Y3vg2x](https://documenter.getpostman.com/view/26991752/2s93Y3vg2x)

## How to login and authorize other API?

On the link above you can find an Endpoint **Get Access token** you can hit that with 
`{
    "username" : "SPINNY",
    "password" : "box@12345" 
    }` 
    passed as body.
After hitting the API you will get `access` and `refresh` token. Copy the `access` token and use it as other api's Authorization Token.


