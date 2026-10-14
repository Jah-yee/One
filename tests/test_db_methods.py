"""
Test database auxiliary methods
"""

import unittest
from typing import override

from database.methods import DbMethods


class TestDatabaseMethods(unittest.TestCase):
    db_methods: DbMethods | None = None

    @override
    def setUp(self) -> None:
        super().setUp()
        self.db_methods = DbMethods()
        
    def test_formal_date(self):
        db_methods = self.db_methods
        assert db_methods is not None
        result = db_methods.formatDate("10/04/2027 13:50")
    
        if result is None:
            self.fail("formatDate returned None for a valid date string.")
        self.assertEqual(result.year, 2027)
        self.assertEqual(result.month, 10)
        self.assertEqual(result.day, 4)
        self.assertEqual(result.hour, 13)
        self.assertEqual(result.minute, 50)
        print(f"Format date returned: {result}")

if __name__ == '__main__':
    unittest.main()