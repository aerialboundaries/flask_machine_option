#!/bin/bash
# -----------------------------------------------
# Flask Machine Option App Setup Script
# -----------------------------------------------
# This script will create the project folder,
# necessary files (app.py, models.py, templates),
# and a virtual environment with required packages.
# -----------------------------------------------

# Project folder
PROJECT_NAME="flask_machine_option"
mkdir -p $PROJECT_NAME/templates
cd $PROJECT_NAME || exit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create requirements.txt
cat <<EOL > requirements.txt
Flask==2.3.6
SQLAlchemy==2.0.22
psycopg[binary]==3.2.2
EOL

# Install dependencies
pip install -r requirements.txt

# Create models.py
cat <<EOL > models.py
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    options = relationship("ProductOption", back_populates="product", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("ProductOption", back_populates="option", cascade="all, delete-orphan")

class ProductOption(Base):
    __tablename__ = "product_options"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)
    product = relationship("Product", back_populates="options")
    option = relationship("Option", back_populates="products")
EOL

# Create app.py
cat <<'EOL' > app.py
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product, Option, ProductOption

app = Flask(__name__)

# DATABASE CONFIGURATION
DATABASE_URL = "postgresql+psycopg:///masato"  # Adjust dbname if needed
engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, future=True)
Base.metadata.create_all(engine)

# ROUTES
@app.route("/")
def index():
    session = Session()
    products = session.query(Product).all()
    options = session.query(Option).all()
    relations = session.query(ProductOption).all()
    session.close()
    return render_template("index.html", products=products, options=options, relations=relations)

# PRODUCT CRUD
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

# OPTION CRUD
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

# RELATION CRUD
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

if __name__ == "__main__":
    app.run(debug=True)
EOL

# Create templates
TEMPLATES=("index.html" "add_product.html" "edit_product.html" "add_option.html" "edit_option.html" "add_relation.html" "edit_relation.html")
for file in "${TEMPLATES[@]}"; do
cat <<EOL > templates/$file
<!DOCTYPE html>
<html>
<head>
    <title>${file}</title>
</head>
<body>
<h1>${file}</h1>
<form method="POST">
    Name: <input type="text" name="name"><br>
    <input type="submit" value="Submit">
</form>
<a href="/">Back to Home</a>
</body>
</html>
EOL
done

echo "Setup complete. Activate your virtual environment with:"
echo "source venv/bin/activate"
echo "Then run: python app.py"

