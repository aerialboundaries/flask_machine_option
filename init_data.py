from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product, Option

# ---------- DATABASE_URL ----------
# WSL + peer認証の場合、ユーザー名をmasatoにしてパスワードは不要
# 自分の環境に合わせてdbnameを変更してください
DATABASE_URL = "postgresql+psycopg:///masato"

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, future=True)
Base.metadata.create_all(engine)

session = Session()

# ---------- INITIAL DATA ----------
if not session.query(Product).first():
    products = [Product(name=f"Product{i}") for i in range(1, 11)]
    options = [Option(name=f"Option{i}") for i in range(1, 11)]
    session.add_all(products + options)
    session.commit()
    print("Initial data inserted")
else:
    print("Data already exists")

session.close()

