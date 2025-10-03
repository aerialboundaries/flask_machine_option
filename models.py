from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    product_options = relationship("ProductOption", back_populates="product", cascade="all, delete")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    product_options = relationship("ProductOption", back_populates="option", cascade="all, delete")

class ProductOption(Base):
    __tablename__ = "product_options"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)
    product = relationship("Product", back_populates="product_options")
    option = relationship("Option", back_populates="product_options")

