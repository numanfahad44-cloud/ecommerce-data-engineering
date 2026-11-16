import csv,sqlite3,unittest
from src.local_demo import DATA,setup,load,gold
class EcommerceTest(unittest.TestCase):
    def test_replay_and_cancel(self):
        db=sqlite3.connect(':memory:'); setup(db)
        with DATA.open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(load(db,rows),4); self.assertEqual(load(db,rows),0)
        self.assertEqual(gold(db),[('2026-01-01',1,3000),('2026-01-02',1,1550)])
        self.assertEqual(load(db,[dict(rows[1],status='CANCELLED',updated_at='2026-01-03T10:00:00')]),1)
        self.assertEqual(gold(db),[('2026-01-02',1,1550)])
        db.close()
