# For testing
import unittest
from tests.servertests  import ServerTests
from tests.clienttests  import ClientTests
from tests.helperstests import HelpersTests

def main():
    # Must start the server before we can run any tests
    run_server()
    # TODO: Only run tests if requested
    run_tests()

def run_server():
    pass

def run_tests():
    test_classes = [ServerTests, ClientTests, HelpersTests]
    suite  = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
