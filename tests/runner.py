import unittest
from tests.servertests              import MakeServerTests
from tests.clienttests              import MakeClientTests
from tests.helperstests             import MakeHelpersTests
from tests.getordertests            import MakeGetOrderTests
from tests.createitemtests          import MakeCreateItemTests
from tests.itemdetailstests         import MakeItemDetailsTests
from tests.createordertests         import MakeCreateOrderTests
from tests.additemtoordertests      import MakeAddItemToOrderTests
from tests.removeitemfromordertests import MakeRemoveItemFromOrderTests

def run_tests():
    test_classes = [MakeServerTests, MakeClientTests, MakeHelpersTests, MakeGetOrderTests,
        MakeCreateItemTests, MakeItemDetailsTests, MakeCreateOrderTests,
        MakeAddItemToOrderTests, MakeRemoveItemFromOrderTests]
    suite  = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_class_factory in test_classes:
        tests = loader.loadTestsFromTestCase(test_class_factory('http://localhost:19546'))
        suite.addTests(tests)
    unittest.TextTestRunner(verbosity=1).run(suite)
