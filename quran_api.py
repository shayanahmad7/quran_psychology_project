import requests
import pandas as pd
import json
import time

def get_verse_details(surah_name, verse_number):
    url = "https://api.quran.com/api/v4/verses/by_key"
    params = {
        "language": "en",
        "words": "true",
        "word_fields": "text_uthmani",
        "audio": "1",
        "verse_key": f"{surah_name}:{verse_number}"
    }
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()['verse']
            return {
                'arabic_text': data['text_uthmani'],
                'audio_url': data['audio']['url'] if data['audio'] else '',
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching verse details for {surah_name}:{verse_number} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                return {'arabic_text': '', 'audio_url': ''}
            time.sleep(2)  # Wait for 2 seconds before retrying

def get_tafsir_link(surah_name, verse_number):
    return f"https://quran.com/{surah_name}/{verse_number}/tafsirs/en-tafsir-ibn-kathir"

def extract_surah_verse(text):
    try:
        parts = text.split(':')
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return None, None

def process_verses(df):
    results = []
    for _, row in df.iterrows():
        try:
            # Try to extract Surah and Verse from the 'Verse' column
            surah, verse = extract_surah_verse(str(row['Verse']))
            
            if surah is None or verse is None:
                # If extraction fails, search for Surah:Verse pattern in all columns
                for col in df.columns[3:]:  # Start from the 4th column (after Description)
                    surah, verse = extract_surah_verse(str(row[col]))
                    if surah is not None and verse is not None:
                        break
            
            if surah is not None and verse is not None:
                verse_details = get_verse_details(surah, verse)
                tafsir_link = get_tafsir_link(surah, verse)
            else:
                print(f"Could not find valid Surah:Verse for concept: {row['Concept']}")
                verse_details = {'arabic_text': '', 'audio_url': ''}
                tafsir_link = ''
            
            results.append({
                'Concept': row['Concept'],
                'Category': row['Category'],
                'Description': row['Description'],
                'Surah': surah,
                'Verse': verse,
                'Translation': row['Translation'] if 'Translation' in row else '',
                'Relation': row['Relation'] if 'Relation' in row else '',
                'Arabic_Text': verse_details['arabic_text'],
                'Tafsir_Link': tafsir_link,
                'Audio_URL': verse_details['audio_url']
            })
        except Exception as e:
            print(f"Error processing row for concept {row['Concept']}: {e}")
    
    return pd.DataFrame(results)

def main():
    try:
        # Load the CSV with matched verses
        df = pd.read_csv('processed_psychological_concepts.csv')
        
        # Process the dataframe
        result_df = process_verses(df)
        
        # Save the results
        result_df.to_csv('final_psychological_concepts_quran_dataset.csv', index=False)
        print("Processing complete. Results saved to 'final_psychological_concepts_quran_dataset.csv'")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()