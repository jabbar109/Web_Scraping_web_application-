import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_data(url, scrape_email, scrape_phone, scrape_address):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    email_addresses = []
    phone_numbers = []
    addresses = []

    if scrape_email:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        email_addresses = re.findall(email_pattern, str(soup))

    if scrape_phone:
        phone_pattern = r'(\+92\s?)?(\()?(\d{3})(?(2)\))[-.\s]?(\d{3})[-.\s]?(\d{4})'
        phone_numbers = re.findall(phone_pattern, str(soup))
        phone_numbers = [''.join(number) for number in phone_numbers]

    if scrape_address:
        address_pattern = r'\d+\s[A-Za-z]+\s[A-Za-z]+,\s[A-Za-z]+,\s[A-Za-z]+,\sPakistan'
        addresses = re.findall(address_pattern, str(soup))

    # Pad lists with None values if lengths are inconsistent
    max_length = max(len(email_addresses), len(phone_numbers), len(addresses))
    email_addresses += [None] * (max_length - len(email_addresses))
    phone_numbers += [None] * (max_length - len(phone_numbers))
    addresses += [None] * (max_length - len(addresses))

    return email_addresses, phone_numbers, addresses

# Create a Streamlit web application
st.title("Web Scraper")

# User input fields
url = st.text_input("Enter URL")
scrape_email = st.checkbox("Scrape Email Addresses")
scrape_phone = st.checkbox("Scrape Phone Numbers")
scrape_address = st.checkbox("Scrape Addresses")

# Scrape and display results
if st.button("Scrape"):
    if url:
        email_addresses, phone_numbers, addresses = scrape_data(url, scrape_email, scrape_phone, scrape_address)

        # Create a beautiful table to display the scraped data
        table_data = {'Email': email_addresses, 'Phone': phone_numbers, 'Address': addresses}
        st.subheader("Scraped Data")
        st.table(table_data)
    else:
        st.write("Please enter a URL.")
