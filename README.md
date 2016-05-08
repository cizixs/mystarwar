## MyStarWars

Get your own starwar dataset in seconds.

This project will crawl [the official starwar api site](https://swapi.co/) and store the content
in local storage with three format suit for your need: json, mongo and mysql.

This means you will have a full-set, well-formatted star war data one strike away.

## Choose the data format
There are some ways to store your data:

- json file in local filesystem, you have to specific the directory to store the data.
- sqlite: local sqlite database. TODO
- mongodb: TODO
- MySQL: TODO

Before started, decide which one you wanted to use. And follow the instructions below:

### Json files
If you just want to store all data in json files, this is easy.
By default, the program will create a `data` directory under current working path.
And store each type of data in a seperate` .json` file. **Make sure you have the right
permission for reading and writing.**

### MongoDB
You can also store the data into mongodb if you want to. But you have to provide
mongodb connection information includes:

- host and port(localhost:35357 by default)
- username and password(no crendentials by default)
- database name(`starwar` by default)


### MySQL
Just like mongodb way, you can also store the data into MySQL. Provide the following
information as needed:

- host and port
- username and password
- database name

## Getting Started

There are two way to run this code:

### Install from pypi(TODO)

Install the library from pypi:

  pip install mystarwar
  mystarwar -o json

### Run from source

  git clone https://github.com/cizixs/mystarwar
  cd mystarwar
  pip install -r requirements.txt
  python starwar.py --backend json —location /some/direcotory/to/store/

Check out the files or database, and have fun hacking!

Note: 

- Depends on your network condition, this might take several seconds to minutes.
- Do'not run the code too frequently, this might cause pressure for the official site.



## TODO

- Support sqlite, mongo and MySQL backend(Right now, only json data is supported.)
- More verbose and controllable loggingn
- Push code to pypi for installing
- Network error, and databse connection error handling

## Contributing
You can contribute to the repository by sending a PR.