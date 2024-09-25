import pandas as pd
import ast

def process_matching_verse(matching_verse):
    if isinstance(matching_verse, float):
        return {'Surah': '', 'Verse': '', 'Translation': '', 'Relation': ''}
    
    try:
        verse_dict = ast.literal_eval(matching_verse)
        return {
            'Surah': verse_dict.get('Surah', ''),
            'Verse': verse_dict.get('Verse', ''),
            'Translation': verse_dict.get('Translation', ''),
            'Relation': verse_dict.get('Relation', '')
        }
    except:
        parts = {}
        current_key = ''
        for line in matching_verse.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                current_key = key.strip()
                parts[current_key] = value.strip()
            elif current_key:
                parts[current_key] += ' ' + line.strip()
        
        return {
            'Surah': parts.get('Surah', ''),
            'Verse': parts.get('Verse', ''),
            'Translation': parts.get('Translation', ''),
            'Relation': parts.get('Relation', '')
        }

def process_dataframe(df):
    result = []
    for _, row in df.iterrows():
        verse_parts = process_matching_verse(row['Matching_Verse'])
        result.append({
            'Concept': row['Concept'],
            'Category': row['Category'],
            'Description': row['Description'],
            'Surah': verse_parts['Surah'],
            'Verse': verse_parts['Verse'],
            'Translation': verse_parts['Translation'],
            'Relation': verse_parts['Relation']
        })
    return pd.DataFrame(result)

if __name__ == "__main__":
    # Load the CSV file
    df = pd.read_csv('psychological_concepts_with_verses_batch.csv')
    
    # Process the dataframe
    processed_df = process_dataframe(df)
    
    # Save the processed dataframe
    processed_df.to_csv('processed_psychological_concepts.csv', index=False)
    print("Processed data saved to 'processed_psychological_concepts_batch.csv'")