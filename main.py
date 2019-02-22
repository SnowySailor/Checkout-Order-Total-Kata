# For testing
from tests.runner import run_tests

# For app
from src.helpers import is_in_list
from src.server import run_server
import sys

def main():
    # Must start the server before we can run any tests
    run_server()
    # Run tests and exit application if desired
    if is_in_list(sys.argv, '--test'):
        run_tests()
        sys.exit()

    print('Running...')

if __name__ == '__main__':
    main()
