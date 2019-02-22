# For testing
from tests.runner import run_tests

# For app
from src.helpers import is_in_list
from src.server import run_server
import sys
import time

def main():
    # Must start the server before we can run any tests
    run_server()

    # Run tests and exit application if desired
    if is_in_list(sys.argv, '--test'):
        run_tests()
        sys.exit()

    # Run a continuous loop because the http server thread is running as
    # a daemon, so the program will exit once the main thread is finished
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Catch the keybord interrupt from ctrl-c in the command line for
        # a graceful exit
        pass

if __name__ == '__main__':
    main()
