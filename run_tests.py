import unittest
from processor import process_file

class TestBasic(unittest.TestCase):
    def test_csv(self):
        records = process_file(b"contractor_name,payment_amount\nAcme,100\n")
        self.assertEqual(records[0]["title"], "Acme")

if __name__ == "__main__":
    unittest.main()
