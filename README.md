# Basic documentation


## Config

### Python version
*Python 3.11*

### Requirements file
*[requirements.txt]requirements.txt*

### Tests file
*[test_cases.py]test_functionality.py*

### Tests
For testing we are using *pytest*.

We are only checking if main functionality returns correct statistics for each given case.

## Run

Fill in bot token in *[credentials.py]credentials.py*, then
add 'sampleDB' in project structure (directory from Mongo 'dump').

1. `docker volume create --name database`
2. `docker network create -d bridge container_network`
3. `docker compose up -d` <- wait for start
4. `pip3.12 install --upgrade pip && pip3.12 install -r requirements.txt`
5. `python3.12 entry_funcionality.py`
6. `python3.12 bot.py`

## Test

Run `pytest` in root directory of the project

