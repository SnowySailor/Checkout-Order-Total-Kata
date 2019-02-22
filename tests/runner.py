import unittest
from tests.servertests  import ServerTests
from tests.clienttests  import ClientTests
from tests.helperstests import HelpersTests

def run_tests():
    test_classes = [ServerTests, ClientTests, HelpersTests]
    suite  = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
