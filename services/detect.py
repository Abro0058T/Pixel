import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to check

def detect():
    url = 'https://khatri-nipun.netlify.app/'

# Define a file to store the previous version of the webpage content
    previous_content_file = 'previous_content.html'
    
    # Send a GET request to the URL and retrieve the current webpage content
    response = requests.get(url)
    current_content = response.text
    
    # Try to open the file containing the previous version of the webpage content
    try:
        with open(previous_content_file, 'r', encoding='utf-8') as file:
            previous_content = file.read()
    except FileNotFoundError:
        previous_content = None
    
    # If the file didn't exist or the current content is different from the previous content, update the file and extract data
    if previous_content is None or current_content != previous_content:
        print("The website has been updated!")
    
        # Extract data using BeautifulSoup (you can modify this part according to your needs)
        soup = BeautifulSoup(current_content, 'html.parser')
        
        # Example: Extract all the links from the updated webpage
        links = [a['href'] for a in soup.find_all('a')]
        print(links)
        # Save the current content as the new previous content
        with open(previous_content_file, 'w', encoding='utf-8') as file:
            file.write(current_content)
    else:
        print("The website has not been updated.")
    
detect()

