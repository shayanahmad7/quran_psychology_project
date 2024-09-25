import pandas as pd
import re

def extract_verse_info(text):
    surah_match = re.search(r'Surah:\s*(.*?)(?:\n|$)', text, re.IGNORECASE)
    verse_match = re.search(r'Verse:\s*(.*?)(?:\n|Translation:)', text, re.IGNORECASE | re.DOTALL)
    translation_match = re.search(r'Translation:\s*"?(.*?)"?(?:\n|Relation to concept:)', text, re.IGNORECASE | re.DOTALL)
    relation_match = re.search(r'Relation to concept:\s*(.*)', text, re.IGNORECASE | re.DOTALL)

    surah = surah_match.group(1).strip() if surah_match else ''
    verse = verse_match.group(1).strip() if verse_match else ''
    translation = translation_match.group(1).strip() if translation_match else ''
    relation = relation_match.group(1).strip() if relation_match else ''

    # Clean up verse number
    verse = re.sub(r'\s*:\s*', ':', verse)  # Remove spaces around colon
    verse = re.sub(r'(\d+):(\d+):00', r'\1:\2', verse)  # Remove :00 from end
    verse = re.sub(r'\[(\d+):(\d+)\]', r'\1:\2', verse)  # Remove square brackets
    verse = re.sub(r'(\d+)\.(\d+)', r'\1:\2', verse)  # Replace dot with colon

    return surah, verse, translation, relation

def clean_text(text):
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove any remaining quotes
    text = text.replace('"', '').replace("'", "")
    return text

def process_row(row):
    matching_verse = row['Matching_Verse']
    surah, verse, translation, relation = extract_verse_info(matching_verse)
    
    return {
        'Concept': clean_text(row['Concept']),
        'Category': clean_text(row['Category']),
        'Description': clean_text(row['Description']),
        'Surah': clean_text(surah),
        'Verse': clean_text(verse),
        'Translation': clean_text(translation),
        'Relation': clean_text(relation)
    }

def main():
    # Load the CSV file
    input_file = 'psychological_concepts_with_verses.csv'
    output_file = 'cleaned_psychological_concepts3.csv'
    
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    print("Processing and cleaning data...")
    results = []
    for _, row in df.iterrows():
        result = process_row(row)
        results.append(result)
    
    # Create a new DataFrame with the processed results
    result_df = pd.DataFrame(results)
    
    # Save the results to a new CSV file
    print(f"Saving cleaned data to {output_file}...")
    result_df.to_csv(output_file, index=False)
    print(f"Processing complete. Results saved to '{output_file}'")
    
    # Print some statistics
    print("\nData cleaning summary:")
    print(f"Total rows processed: {len(result_df)}")
    print(f"Rows with empty Surah: {result_df['Surah'].isna().sum()}")
    print(f"Rows with empty Verse: {result_df['Verse'].isna().sum()}")
    print(f"Rows with empty Translation: {result_df['Translation'].isna().sum()}")
    print(f"Rows with empty Relation: {result_df['Relation'].isna().sum()}")

if __name__ == "__main__":
    main()

