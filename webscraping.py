import requests
from bs4 import BeautifulSoup
import csv
import os

# Create a directory for storing the CSV files
output_dir = "scraped_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# List of URLs to scrape
urls = [
    "https://example1.com/",
    "https://example2.com/",
    "https://example3.com/page1/",
    ]

# Loop through each URL
for url in urls:
    response = requests.get(url)  # Send a GET request to the URL
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content
    
    # Extract headings
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    headings_data = [(heading.name, heading.text.strip()) for heading in headings]
    
    # Extract internal links (href attribute starts with '/')
    links = soup.find_all('a', href=True)
  #extract all links whatever the link start 
    internal_links = [(link.text, link['href']) for link in links ]
    
    # Extract image tags with alt text, src, and dimensions
    images = soup.find_all('img', alt=True)
    image_data = [
        (
            img.get('src', 'No source'),  # Image source
            img['alt'],  # Alt text
            img.get('width', 'No width'),  # Image width
            img.get('height', 'No height')  # Image height
        )
        for img in images
    ]
    
    # Create CSV files for each type of data
    domain = url.split("//")[-1].split("/")[0]  # Extract domain name for file naming

    # Save headings to CSV
    headings_csv = os.path.join(output_dir, f"{domain}_headings.csv")
    with open(headings_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Heading Tag", "Text"])
        writer.writerows(headings_data)
    
    # Save internal links to CSV
    links_csv = os.path.join(output_dir, f"{domain}_internal_links.csv")
    with open(links_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Link Text", "URL"])
        writer.writerows(internal_links)
    
    # Save image data (including dimensions) to CSV
    images_csv = os.path.join(output_dir, f"{domain}_images.csv")
    with open(images_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Source", "Alt Text", "Width", "Height"])
        writer.writerows(image_data)
