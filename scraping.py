import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_psychological_concepts():
    url = "https://helpfulprofessor.com/psychological-concepts/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    concepts = []
    current_category = ""

    # Find all h3 and ul elements
    elements = soup.find_all(['h3', 'ul'])

    for element in elements:
        if element.name == 'h3':
            current_category = element.text.strip()
        elif element.name == 'ul':
            # Find all li elements within the ul
            list_items = element.find_all('li')
            for item in list_items:
                strong_tag = item.find('strong')
                if strong_tag:
                    concept = strong_tag.text.strip().rstrip(':')
                    description = item.text.replace(strong_tag.text, '').strip()
                    concepts.append({
                        'Category': current_category,
                        'Concept': concept,
                        'Description': description
                    })

    # Create a DataFrame
    df = pd.DataFrame(concepts)
    
    # Add an Index column
    df.insert(0, 'Index', range(1, len(df) + 1))

    return df

if __name__ == "__main__":
    df = scrape_psychological_concepts()
    df.to_csv('psychological_concepts.csv', index=False)
    print(f"Total concepts scraped: {len(df)}")
    print(df.head())