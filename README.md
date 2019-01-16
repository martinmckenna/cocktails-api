## Getting Started

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

The following endpoints are available

| Endpoints | Request Body Params | Query Params |
|-----------|--------------------|---------------|
| `GET /cocktails` |  | **name** - [string] filter by name of the cocktail <br><br> **ing_list** - [comma seperated Ints] a list of ingredients that you want to request cocktails for. Please note that if you provide the ID for "Gin," for example, "Gin and Tonic" will not be returned becasue you need to provide ALL ingredients. This can be altered with the `will_shop` param <br><br> **will_shop** - ["true" or "false"] in conjunction with the `ing_list` param, returns a list of cocktails that match some ingredients passed. So "Gin and Tonic" will return if you pass the ID for "Gin" in the `ing_list` param and this param is set to "true" |
| `GET /cocktail/:id` |  |
| `POST /cocktails` | **name** - [String] The name of the cocktail <br> **glass** - [String] What glass is the cocktail served in? <br> **finish** - ["shaken" or "stirred" or null] Self-explanatory <br> **Ingredients** - [Array of Objects] Each object must contain the following keys <br> <ul><li>**id** - [Int] the id of the ingredient</li><li>**ounces** - [Float] how many ounces does this ingredient use?</li><li>**step** - [Int] what step does this ingredient come in the cocktail recipie?</li><li>**action** - [String] what action do you perform with this ingredient? Examples include "muddle", "add", "squeeze"</li></ul>   |
| `PUT /cocktails/:id` | Same as POST /cocktails | |
| `DELETE /cocktails/:id` | |
| `GET /ingredients` | | **name** - [String] filter ingredients list by name |
| `GET /ingredients/:id` | |
| `POST /ingredients`| **name** - [String] name of the ingredient <br> **ing_type** - [string] What type of ingredient is this? Examples include "liquor", "fruit", "juice" | |
| `PUT /ingredients/:id` | same as POST /ingredients | |
| `DELETE /ingredients/:id` | |




