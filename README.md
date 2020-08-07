# profil-software-recruitment

## Description
It is a console project made for recruitment purposes. It loads json data based on https://randomuser.me/ api,
manipulates it, inserts it into sqlite database using <b>peewee</b> ORM and then get's user requested data through CLI
based on <b>click</b> module.

## Requirements
<ul>
<li>python 3.7+</li>
<li>pip</li>
<li>virtualenv</li>
</ul>

## Installation:

Create virtual environment
```pythonregexp
$ virtualenv venv
```
Activate virtual enviornment
```pythonregexp
$ path\to\venv\Scripts\activate.bat
```
Install dependencies
```pythonregexp
$ pip install -r requirements.txt
```

## Usage

Run a {command}:
```pythonregexp
$ python cli {command}
```

List of commands:
```pythonregexp
$ python cli --help
```

