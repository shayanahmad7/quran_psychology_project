import requests
import pandas as pd
import time
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_verse_details(surah, verse):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani"
    params = {
        "verse_key": f"{surah}:{verse}",
    }
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            verses = data.get('verses', [])
            if verses:
                verse_data = verses[0]
                arabic_text = verse_data.get('text_uthmani', '')
                
                # Get audio information
                audio_url = f"https://verses.quran.com/{surah}/{verse}.mp3"
                
                logging.info(f"Successfully fetched data for {surah}:{verse}")
                return {
                    'arabic_text': arabic_text,
                    'audio_url': audio_url,
                }
            else:
                logging.warning(f"No verse data found for {surah}:{verse}")
                return {'arabic_text': '', 'audio_url': ''}
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching verse details for {surah}:{verse} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                return {'arabic_text': '', 'audio_url': ''}
            time.sleep(2)

def get_tafsir_link(surah, verse):
    return f"https://quran.com/{surah}/{verse}/tafsirs/en-tafsir-ibn-kathir"

def extract_verse_info(row):
    surah = row.get('Surah', '')
    verse = row.get('Verse', '')
    translation = row.get('Translation', '')
    
    if surah and verse:
        return surah, verse, translation
    
    # If Surah and Verse are not separate columns, try to extract from Translation
    match = re.search(r'(\d+):(\d+)', translation)
    if match:
        return match.group(1), match.group(2), translation
    
    return None, None, None

def process_row(row):
    surah, verse, translation = extract_verse_info(row)
    if surah and verse:
        verse_details = get_verse_details(surah, verse)
        tafsir_link = get_tafsir_link(surah, verse)
        result = {
            'Surah': surah,
            'Verse': verse,
            'Translation': translation,
            'Arabic_Text': verse_details['arabic_text'],
            'Audio_URL': verse_details['audio_url'],
            'Tafsir_Link': tafsir_link
        }
        logging.info(f"Processed data: {result}")
        return result
    logging.warning(f"No valid Surah:Verse found in row")
    return {
        'Surah': '',
        'Verse': '',
        'Translation': '',
        'Arabic_Text': '',
        'Audio_URL': '',
        'Tafsir_Link': ''
    }

def main():
    try:
        # Load the CSV with matched verses
        df = pd.read_csv('processed_psychological_concepts.csv')
        logging.info(f"Loaded CSV with {len(df)} rows")
        
        # Process the dataframe
        results = []
        total_rows = len(df)
        for index, row in df.iterrows():
            try:
                logging.info(f"Processing row {index + 1}/{total_rows}")
                result = process_row(row)
                full_result = {**row.to_dict(), **result}
                results.append(full_result)
                logging.info(f"Completed processing row {index + 1}")
            except Exception as e:
                logging.error(f"Error processing row {index + 1}: {e}")
                results.append(row.to_dict())
            time.sleep(1)  # Add a delay to avoid overwhelming the API
        
        result_df = pd.DataFrame(results)
        
        # Save the results
        result_df.to_csv('final_psychological_concepts_quran_dataset.csv', index=False)
        logging.info("Processing complete. Results saved to 'final_psychological_concepts_quran_dataset.csv'")
        
        # Log column information
        logging.info(f"Columns in the result DataFrame: {result_df.columns.tolist()}")
        for col in ['Arabic_Text', 'Audio_URL', 'Tafsir_Link']:
            non_empty = result_df[col].notna().sum()
            logging.info(f"Non-empty values in {col}: {non_empty}/{len(result_df)}")
        
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()