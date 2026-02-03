import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Flipkart Clone", layout="wide")

# Header
st.header("Flipkart Clone")

# Search bar
search_query = st.text_input("Search for products, brands, and more")

# Banner
st.image("https://via.placeholder.com/1024x200?text=Banner+Image", use_column_width=True)

# Product categories
st.subheader("Categories")
cols = st.columns(4)
categories = ["Electronics", "Fashion", "Home", "Beauty"]

for col, category in zip(cols, categories):
    col.image("https://via.placeholder.com/150", caption=category, use_column_width=True)

# Featured products
st.subheader("Featured Products")
products = [
    {"name": "Product 1", "price": "$100", "image": "https://via.placeholder.com/200"},
    {"name": "Product 2", "price": "$150", "image": "https://via.placeholder.com/200"},
    {"name": "Product 3", "price": "$200", "image": "https://via.placeholder.com/200"},
    {"name": "Product 4", "price": "$250", "image": "https://via.placeholder.com/200"},
]

cols = st.columns(4)
for col, product in zip(cols, products):
    col.image(product["image"], use_column_width=True)
    col.write(product["name"])
    col.write(product["price"])

# Footer
st.markdown("---")
st.write("© 2024 Flipkart Clone. All rights reserved.")
