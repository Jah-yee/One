"""
Test database main methods (create, delete, insert, update, select)
"""

import unittest
import os

from typing import override
from database.db import *
from database.methods import DbMethods

class TestDatabase(unittest.TestCase):
    db: DatabaseManager | None = None
    db_path: str | None = None
    db_methods: DbMethods | None = None

    @override
    def setUp(self) -> None:
        self.db_path = "tests/db/test_database.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        self.db = get_db_manager(self.db_path)
        create_table(self.db)
        self.db_methods = DbMethods()

    @override
    def tearDown(self) -> None:
        if self.db is not None:
            self.db.close()
        if self.db_path is not None and os.path.exists(self.db_path):
            os.remove(self.db_path)
        super().tearDown()

    def test_create_task(self):
        print("\n #############Testing create_task...#############")
        assert self.db is not None
        assert self.db_methods is not None
        time = self.db_methods.formatDate("2027-04-10 13:50")
        
        create_task(
            name="make a coffee",
            time_remaining=time,
            description="buy ingredients",
            db=self.db
        )
        create_task(
            name="make a cake",
            time_remaining=time,
            description="buy ingredients",
            db=self.db
        )

        view_tasks(self.db)
        
    def test_delete_task(self):
        print("\n #############Testing delete_task...#############")
        assert self.db is not None

        task_name = "make a coffee"
        create_task(task_name, time_remaining=None, db=self.db)
        create_task("make a cake", time_remaining=None, db=self.db)
        self.assertTrue(verify_task(task_name, self.db))

        delete_task(task_name, self.db)

        view_tasks(self.db)
        self.assertFalse(verify_task(task_name, self.db))
        


   
if __name__ == '__main__':
    unittest.main()