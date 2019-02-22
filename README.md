# Checkout Order Total Kata

## Requirements
- Python 3.6

## Running
Clone this repository onto your machine and `cd` into it via the command line. Run `python3 main.py` to start the application.

## Testing
Application is being written and tested on Ubuntu 18.04 with the Python 3.6.5 interpreter that comes pre-installed.

Tests are located in the `tests` directory and are separated into three files. The helpers tests are for functions defined in the `src/helpers.py` file. The server tests are for functions that are used on the server side to compute values. The client tests are for requests that a client would run to alter the state of the application.

To run this application's tests, run the application with the `--test` flag like so: `python3 main.py --test`. All tests will run and then the application will shut down.
