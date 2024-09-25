import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import time
import logging
import json

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

def get_matching_verses_batch(batch):
    logging.info(f"Processing batch of {len(batch)} concepts")
    prompt = "For each of the following psychological concepts, provide a relevant verse from the Quran. Include the Surah name, verse number (in the format chapter:verse), the English translation of the verse, and a brief explanation of how the verse relates to the concept. Format your response as a JSON object where each key is the concept name and the value contains the Surah, Verse, Translation, and Relation.\n\n"
    
    for index, row in batch.iterrows():
        prompt += f"Concept: {row['Concept']}\nCategory: {row['Category']}\nDescription: {row['Description']}\n\n"

    try:
        logging.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that finds relevant Quranic verses for psychological concepts."},
                {"role": "user", "content": prompt}
            ]
        )
        logging.info("Received response from OpenAI API")
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error processing batch: {str(e)}")
        return {}

def process_dataframe(df, batch_size=5):
    logging.info(f"Starting to process dataframe with {len(df)} rows")
    results = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        matching_verses = get_matching_verses_batch(batch)
        for index, row in batch.iterrows():
            concept = row['Concept']
            verse_info = matching_verses.get(concept, {})
            results.append({
                'Concept': concept,
                'Category': row['Category'],
                'Description': row['Description'],
                'Matching_Verse': json.dumps(verse_info) if verse_info else ""
            })
        logging.info(f"Completed processing batch {i//batch_size + 1}")
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
        result_df.to_csv('psychological_concepts_with_verses_batch.csv', index=False)
        logging.info("Processing complete. Results saved to 'psychological_concepts_with_verses_batch.csv'")
    except Exception as e:
        logging.error(f"An error occurred in main function: {str(e)}")

if __name__ == "__main__":
    main()