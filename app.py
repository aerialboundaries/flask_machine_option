from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Product, Option, ProductOption

app = Flask(__name__)

# ---------- DATABASE_URL ----------
# WSL + peer認証なのでユーザー名はmasato、パスワード不要
# 自分の環境に合わせてdbnameを変更してください
DATABASE_URL = "postgresql+psycopg:///masato"

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, future=True)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# ---------- HOME PAGE ----------
@app.route("/")
def index():
    session = Session()
    products = session.query(Product).all()
    options = session.query(Option).all()

    # ← DetachedInstanceError 対策: joinedloadで関連をまとめて取得
    relations = session.query(ProductOption) \
        .options(
            joinedload(ProductOption.product),
            joinedload(ProductOption.option)
        ).all()

    session.close()
    return render_template("index.html", products=products, options=options, relations=relations)

# ---------- PRODUCT ----------
@app.route("/add_product", methods=["GET","POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        session = Session()
        session.add(Product(name=name))
        session.commit()
        session.close()
        return redirect(url_for("index"))
    return render_template("add_product.html")

@app.route("/edit_product/<int:id>", methods=["GET","POST"])
def edit_product(id):
    session = Session()
    product = session.get(Product, id)
    if request.method == "POST":
        product.name = request.form.get("name")
        session.commit()
        session.close()
        return redirect(url_for("index"))
    session.close()
    return render_template("edit_product.html", product=product)

@app.route("/delete_product/<int:id>")
def delete_product(id):
    session = Session()
    product = session.get(Product, id)
    session.delete(product)
    session.commit()
    session.close()
    return redirect(url_for("index"))

# ---------- OPTION ----------
@app.route("/add_option", methods=["GET","POST"])
def add_option():
    if request.method == "POST":
        name = request.form.get("name")
        session = Session()
        session.add(Option(name=name))
        session.commit()
        session.close()
        return redirect(url_for("index"))
    return render_template("add_option.html")

@app.route("/edit_option/<int:id>", methods=["GET","POST"])
def edit_option(id):
    session = Session()
    option = session.get(Option, id)
    if request.method == "POST":
        option.name = request.form.get("name")
        session.commit()
        session.close()
        return redirect(url_for("index"))
    session.close()
    return render_template("edit_option.html", option=option)

@app.route("/delete_option/<int:id>")
def delete_option(id):
    session = Session()
    option = session.get(Option, id)
    session.delete(option)
    session.commit()
    session.close()
    return redirect(url_for("index"))

# ---------- PRODUCTOPTION ----------
@app.route("/add_relation", methods=["GET","POST"])
def add_relation():
    session = Session()
    products = session.query(Product).all()
    options = session.query(Option).all()
    if request.method == "POST":
        product_id = request.form.get("product_id")
        option_id = request.form.get("option_id")
        description = request.form.get("description")
        session.add(ProductOption(product_id=product_id, option_id=option_id, description=description))
        session.commit()
        session.close()
        return redirect(url_for("index"))
    session.close()
    return render_template("add_relation.html", products=products, options=options)

@app.route("/edit_relation/<int:id>", methods=["GET","POST"])
def edit_relation(id):
    session = Session()
    relation = session.get(ProductOption, id)
    products = session.query(Product).all()
    options = session.query(Option).all()
    if request.method == "POST":
        relation.product_id = request.form.get("product_id")
        relation.option_id = request.form.get("option_id")
        relation.description = request.form.get("description")
        session.commit()
        session.close()
        return redirect(url_for("index"))
    session.close()
    return render_template("edit_relation.html", relation=relation, products=products, options=options)

@app.route("/delete_relation/<int:id>")
def delete_relation(id):
    session = Session()
    relation = session.get(ProductOption, id)
    session.delete(relation)
    session.commit()
    session.close()
    return redirect(url_for("index"))

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)

