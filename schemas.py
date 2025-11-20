"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Restaurant app schemas

class MenuItem(BaseModel):
    """
    Menu items available at the restaurant
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Dish description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Category, e.g., Starters, Mains, Desserts, Drinks")
    is_vegetarian: bool = Field(False, description="Vegetarian option")
    is_spicy: bool = Field(False, description="Spicy dish indicator")

class Reservation(BaseModel):
    """
    Table reservations
    Collection name: "reservation"
    """
    name: str = Field(..., description="Guest name")
    email: Optional[str] = Field(None, description="Contact email")
    phone: str = Field(..., description="Contact phone number")
    date: str = Field(..., description="Date of reservation (YYYY-MM-DD)")
    time: str = Field(..., description="Time of reservation (HH:MM)")
    guests: int = Field(..., ge=1, le=20, description="Number of guests")
    notes: Optional[str] = Field(None, description="Special requests or notes")

class ContactMessage(BaseModel):
    """
    Messages sent from contact form
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., description="Message body")
