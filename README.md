# Asyncio demo project

## About

This is just a simple demo project for test asyncio features. There are lots of things which can be improved

## How to run

With Docker power and make it can be very easy:
- `make build`
- `make`

That's all!
If you can't use make see commands [there](https://github.com/solartune/async_demo/blob/master/Makefile)

## Useful commands

Below you can see some useful commands for manipulate docker containers via make:

- `make build` - Creates networks if they don't exist and builds images
- `make` - Runs containers
- `make stop` - Stopps containers
- `make down` - Stops containers and removes containers, networks, volumes, and images
- `make reload` - Reloads gunicorn in the application container
- `make restart` - Restarts the application container
- `make logs-app` - Shows last 200 logs from the application container
- `make tests` - Runs tests

## Auth system

```
NOTE!
This project uses JWT token for authorization in the system.
```
Since all methods required the authorization you need login to the system and use JWT token in headers `Authorization: <your token>`
After this you have 5 minutes before your token expires

## API and Swagger UI

You can test project API by Swagger UI.
Follow this [link](http://127.0.0.1:8000/api/doc).
There you can see API reference and test end-points.

## Know issues

- Messages like `Task was destroyed but it is pending!` after running tests
