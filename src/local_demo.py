import csv, sqlite3
from pathlib import Path
from decimal import Decimal
from datetime import date, datetime
DATA=Path(__file__).resolve().parents[1]/'data/orders.csv'

def setup(db):
    db.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,customer INTEGER,day TEXT,status TEXT,cents INTEGER,updated_at TEXT)')

def load(db,rows):
    count=0
    with db:
        for r in rows:
            oid,cid=int(r['order_id']),int(r['customer_id'])
            cents=Decimal(r['amount'])*100
            status=r['status']; day=date.fromisoformat(r['order_date']).isoformat(); stamp=datetime.fromisoformat(r['updated_at']).isoformat()
            if oid<=0 or cid<=0 or status not in ('PAID','CANCELLED') or not cents.is_finite() or cents<0 or cents!=cents.to_integral_value():
                raise ValueError('invalid order; batch rolled back')
            count+=db.execute('INSERT INTO orders VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET customer=excluded.customer,day=excluded.day,status=excluded.status,cents=excluded.cents,updated_at=excluded.updated_at WHERE excluded.updated_at>orders.updated_at',(oid,cid,day,status,int(cents),stamp)).rowcount
    return count

def gold(db):
    return db.execute("SELECT day,count(*),sum(cents) FROM orders WHERE status='PAID' GROUP BY day ORDER BY day").fetchall()

if __name__=='__main__':
    db=sqlite3.connect(':memory:'); setup(db)
    with DATA.open() as f: rows=list(csv.DictReader(f))
    print('First writes:',load(db,rows),'Replay writes:',load(db,rows)); print('Daily paid orders and revenue cents:',gold(db))
