# data_cleaning.py

import pandas as pd
import re

# File paths
input_file = "psychological_concepts_with_verses.csv"
output_file = "cleaned_verses.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Define a function to clean and split the "Matching_Verse" column into four separate columns
def extract_columns(matching_verse):
    # Regular expression pattern to extract Surah, Verse, Translation, and Relation to Concept
    pattern = r"Surah:\s*(.*?)[\n,]*Verse:\s*(\d+).*?Translation:\s*\"(.*?)\""
    match = re.search(pattern, matching_verse, re.DOTALL)
    
    if match:
        surah = match.group(1)
        verse = match.group(2)
        translation = match.group(3)
        # Assuming Relation to Concept is already captured in the description of the concept
        relation = "Related to psychological concept"
        return pd.Series([surah, verse, translation, relation])
    else:
        # Return None values if the pattern doesn't match
        return pd.Series([None, None, None, None])

# Apply the function to each row in the "Matching_Verse" column
df[['Surah', 'Verse', 'Translation', 'Relation to Concept']] = df['Matching_Verse'].apply(extract_columns)

# Drop the original "Matching_Verse" column
df.drop('Matching_Verse', axis=1, inplace=True)

# Save the cleaned DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"Data cleaning complete. Cleaned data saved to '{output_file}'.")
