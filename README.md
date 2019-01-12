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




