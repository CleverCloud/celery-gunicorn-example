# Celery and Gunicorn on Clever Cloud

Deploy this application using Celery and Gunicorn. To follow this tutorial, you need a [Clever Cloud account](https://console.clever-cloud.com) and [Clever Tools](https://github.com/CleverCloud/clever-tools):

```bash
npm i -g clever-tools
clever login
```

You can also install Clever Tools with [many packages managers](https://www.clever-cloud.com/developers/doc/cli/install/).

## Create resources

Create and configure a Python application:

```bash
git clone https://github.com/CleverCloud/celery-gunicorn-example
cd celery-gunicorn-example

clever create -t python
clever env set CC_PYTHON_BACKEND "gunicorn"
clever env set CC_PYTHON_MODULE "app:server"
clever env set CC_PRE_RUN_HOOK "bash workers.sh"
```

## Deploy the application

Everything is now ready, just deploy the application and open it:

```bash
clever deploy
clever open
```

## Usage

You can now use the application by making a GET request to the following URL:

`https://<your-app-url>?text=This%20is%20a%20demo`

You can also add operations to the request by adding the following parameters:

- `reverse`: reverse the text
- `uppercase`: convert the text to uppercase
- `lowercase`: convert the text to lowercase
- `repeat_count`: repeat the text a number of times specified

For example, to reverse the text, you can make a GET request to the following URL:

`http://<your-app-url>?text=Hello%20world!&reverse=true`

You can also combine multiple operations:

`http://<your-app-url>?text=Hello%20world!&reverse=true&uppercase=true&repeat_count=3`
