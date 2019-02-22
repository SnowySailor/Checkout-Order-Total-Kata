import unittest
from tests.servertests  import MakeServerTests
from tests.clienttests  import MakeClientTests
from tests.helperstests import MakeHelpersTests

def run_tests():
    test_classes = [MakeServerTests, MakeClientTests, MakeHelpersTests]
    suite  = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_class_factory in test_classes:
        tests = loader.loadTestsFromTestCase(test_class_factory('http://localhost:19546'))
        suite.addTests(tests)
    unittest.TextTestRunner(verbosity=1).run(suite)
