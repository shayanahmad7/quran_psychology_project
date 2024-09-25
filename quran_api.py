import requests
import pandas as pd
import time
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_verse(translation):
    url = "https://api.quran.com/api/v4/search"
    params = {
        "q": translation,
        "size": 1,
        "language": "en"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get('search', {}).get('results', [])
        if results:
            verse_key = results[0].get('verse_key')
            if verse_key:
                surah, verse = verse_key.split(':')
                return surah, verse
        logging.warning(f"No matching verse found for translation: {translation[:50]}...")
        return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error searching for verse: {e}")
        return None, None

def get_verse_details(surah, verse):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani"
    params = {
        "verse_key": f"{surah}:{verse}",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        verses = data.get('verses', [])
        if verses:
            arabic_text = verses[0].get('text_uthmani', '')
        else:
            arabic_text = ''

        # Get audio information
        audio_url = f"https://verses.quran.com/{surah}/{verse}.mp3"
        
        logging.info(f"Successfully fetched data for {surah}:{verse}")
        return {
            'arabic_text': arabic_text,
            'audio_url': audio_url,
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching verse details for {surah}:{verse}: {e}")
        return {'arabic_text': '', 'audio_url': ''}

def get_surah_name(surah_number):
    url = f"https://api.quran.com/api/v4/chapters/{surah_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('chapter', {}).get('name_simple', '')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching surah name for surah {surah_number}: {e}")
        return ''

def get_tafsir_link(surah, verse):
    surah_name = get_surah_name(surah)
    if surah_name:
        return f"https://quran.com/en/{surah_name.lower().replace(' ', '-')}/{verse}/tafsirs"
    return f"https://quran.com/{surah}/{verse}/tafsirs"

def process_row(row):
    translation = row.get('Translation', '')
    surah, verse = search_verse(translation)
    
    if surah and verse:
        verse_details = get_verse_details(surah, verse)
        tafsir_link = get_tafsir_link(surah, verse)
        result = {
            'Surah': surah,
            'Verse': verse,
            'Arabic_Text': verse_details['arabic_text'],
            'Audio_URL': verse_details['audio_url'],
            'Tafsir_Link': tafsir_link
        }
        logging.info(f"Processed data: {result}")
        return result
    
    logging.warning(f"No valid Surah:Verse found for translation: {translation[:50]}...")
    return {
        'Surah': '',
        'Verse': '',
        'Arabic_Text': '',
        'Audio_URL': '',
        'Tafsir_Link': ''
    }

def main():
    try:
        # Load the CSV with matched verses
        df = pd.read_csv('psychological_concepts_with_verses_parsed.csv')
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
        result_df.to_csv('final_psychological_concepts_quran_dataset2.csv', index=False)
        logging.info("Processing complete. Results saved to 'final_psychological_concepts_quran_dataset3.csv'")
        
        # Log column information
        logging.info(f"Columns in the result DataFrame: {result_df.columns.tolist()}")
        for col in ['Arabic_Text', 'Audio_URL', 'Tafsir_Link']:
            non_empty = result_df[col].notna().sum()
            logging.info(f"Non-empty values in {col}: {non_empty}/{len(result_df)}")
        
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()