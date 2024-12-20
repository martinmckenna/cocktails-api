## Getting Started

### Deploying

Once the new code has been pulled on the server, run:

```
sudo docker-compose build app
sudo docker-compose up app -d
```

If this doesn't work, try:

```
sudo docker-compose down --rmi all --remove-orphans
sudo docker-compose up -d
```

### Set up Virutal Env

1. Make sure you have virtualenv installed

```bash
pip3 install venv
```

2. Create a virutalenv with Python3

```bash
virtualenv -p python3 your-dir-name-here
```

3. Activate the virtualenv

```bash
source your-dir-name-here/bin/activate
```

4. Deactivate the virtualenv

```bash
deactivate
```

### Install Requirements

While in the venv, first make sure you have the correct version of python

```bash
$ which python
/your-dir-name-here/env/bin/python
```

Then

```bash
pip install -r requirements.txt
```

### Create a local MySQL server

Run the folllowing

```bash
brew install mysql
brew tap homebrew/services
```

Verify the installation succeeded with

```bash
mysql -V
```

Start and Stop MySQL Server

```bash
brew services start mysql
```

```bash
brew services stop mysql
```

### Running the Project

Run the following while `cd`ed into the project root

```bash
python3 app.py
```

## Using the API

### Authenticating

Once logged in successfully, a token will return. In each request, use the `x-access-token` header with the token provided
by login to successfully make a request

The following endpoints are available

| Endpoints | Request Body Params | Query Params |
|-----------|--------------------|---------------|
| `GET /cocktails` |  | **name** - [String] filter by name of the cocktail <br><br> **ing_list** - [comma seperated Ints] a list of ingredients that you want to request cocktails for. Please note that if you provide the ID for "Gin," for example, "Gin and Tonic" will not be returned becasue you need to provide ALL ingredients. This can be altered with the `will_shop` param <br><br> **will_shop** - ["true" or "false"] in conjunction with the `ing_list` param, returns a list of cocktails that match some ingredients passed. So "Gin and Tonic" will return if you pass the ID for "Gin" in the `ing_list` param and this param is set to "true" <br><br> **page** what page you want - will return list of 25 results |
| `GET /cocktail/:id` |  |
| `POST /cocktails` | **name** - [String] The name of the cocktail <br> **glass** - [String] What glass is the cocktail served in? <br> **finish** - ["shaken" or "stirred" or null] Self-explanatory <br> **Ingredients** - [Array of Objects] Each object must contain the following keys <br> <ul><li>**id** - [Int] the id of the ingredient</li><li>**ounces** - [Float] how many ounces does this ingredient use?</li><li>**step** - [Int] what step does this ingredient come in the cocktail recipie?</li><li>**action** - [String] what action do you perform with this ingredient? Examples include "muddle", "add", "squeeze"</li><li>**unit** - [String] what is the unit of measurement for this ingredient?</li></ul>   |
| `PUT /cocktails/:id` | Same as POST /cocktails | |
| `DELETE /cocktails/:id` | |
| `GET /ingredients` | | **name** - [String] filter ingredients list by name <br><br> **page** what page you want - will return list of 25 results |
| `GET /ingredients/:id` | |
| `POST /ingredients`| **name** - [String] name of the ingredient <br> **ing_type** - [string] What type of ingredient is this? Examples include "liquor", "fruit", "juice" | |
| `PUT /ingredients/:id` | same as POST /ingredients | |
| `DELETE /ingredients/:id` | |
| `GET /users` | | **name** - [String] filter by name of the cocktail <br><br> **page** what page you want - will return list of 25 results |
| `GET /users/:public_id` | |
| `POST /users` | **name** - [String] username <br> **password** - [String] user password | |
| `DELETE /users/:public_id` | |
| `PUT /users/:pub_id` | **cocktails** - [List of Ints] array of ints that match with the cocktails this user wants to favorite | |
| `PUT /users/:public_id/promote`| |
| `GET /login` | | **Basic Authentication** - gives you an auth token that lasts 30 minutes



