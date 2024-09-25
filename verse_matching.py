import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
logging.info("Environment variables loaded")

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if client.api_key:
    logging.info("OpenAI API key set successfully")
else:
    logging.error("Failed to set OpenAI API key")

def get_matching_verse(row):
    logging.info(f"Processing concept: {row['Concept']}")
    prompt = f"""
    The psychological concept is "{row['Concept']}" from the category "{row['Category']}".
    Description: {row['Description']}

    Please provide a relevant verse from the Quran that relates to this concept. 
    Include the Surah name, verse number (in the format chapter:verse), 
    the English translation of the verse, and a detailed explanation of how 
    the verse relates to the psychological concept.

    Format your response as follows:
    Surah: [Surah Name]
    Verse: [chapter:verse]
    Translation: [English translation of the verse]
    Relation to concept: [Detailed explanation]
    """

    try:
        logging.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that finds relevant Quranic verses for psychological concepts."},
                {"role": "user", "content": prompt}
            ]
        )
        logging.info("Received response from OpenAI API")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error processing {row['Concept']}: {str(e)}")
        return ""

def process_dataframe(df):
    logging.info(f"Starting to process dataframe with {len(df)} rows")
    results = []
    for index, row in df.iterrows():
        logging.info(f"Processing row {index + 1}/{len(df)}")
        matching_verse = get_matching_verse(row)
        results.append({
            'Concept': row['Concept'],
            'Category': row['Category'],
            'Description': row['Description'],
            'Matching_Verse': matching_verse
        })
        logging.info(f"Completed processing row {index + 1}")
        time.sleep(20)  # To avoid hitting rate limits
    
    logging.info("Finished processing all rows")
    return pd.DataFrame(results)

def main():
    logging.info("Starting main function")
    try:
        # Load your psychological concepts CSV
        df = pd.read_csv('psychological_concepts.csv')
        logging.info(f"Loaded CSV file with {len(df)} rows")
        
        # Process the dataframe
        result_df = process_dataframe(df)
        
        # Save the results
        result_df.to_csv('psychological_concepts_with_verses.csv', index=False)
        logging.info("Processing complete. Results saved to 'psychological_concepts_with_verses.csv'")
    except Exception as e:
        logging.error(f"An error occurred in main function: {str(e)}")

if __name__ == "__main__":
    main()