import pandas as pd
from tabulate import tabulate
import random

def load_data(file_path):
    return pd.read_csv(file_path)

def display_concept(concept):
    print("\n" + "=" * 80)
    print(f"Concept: {concept['Concept']}")
    print(f"Category: {concept['Category']}")
    print("-" * 80)
    print(f"Description: {concept['Description']}")
    print("-" * 80)
    print("Quranic Verse:")
    print(f"Surah: {concept['Surah']}")
    print(f"Verse: {concept['Verse']}")
    print(f"Translation: {concept['Translation']}")
    print("-" * 80)
    print(f"Relation to concept: {concept['Relation']}")
    print("-" * 80)
    print(f"Arabic Text: {concept['Arabic_Text']}")
    print(f"Audio URL: {concept['Audio_URL']}")
    print(f"Tafsir Link: {concept['Tafsir_Link']}")
    print("=" * 80)

def display_random_concepts(df, n=5):
    sample = df.sample(n=n)
    concepts_table = sample[['Concept', 'Category']].values.tolist()
    print("\nRandom 5 Psychological Concepts:")
    print(tabulate(concepts_table, headers=['Concept', 'Category'], tablefmt='grid', showindex=True))
    
    while True:
        choice = input("\nEnter the number of the concept you want to view (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        try:
            index = int(choice)
            if 0 <= index < len(sample):
                display_concept(sample.iloc[index])
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def display_all_concepts(df):
    concepts_table = df[['Concept', 'Category', 'Surah', 'Verse']].values.tolist()
    print("\nAll Psychological Concepts:")
    print(tabulate(concepts_table, headers=['Concept', 'Category', 'Surah', 'Verse'], tablefmt='grid', showindex=True))
    
    while True:
        choice = input("\nEnter the number of the concept you want to view in detail (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        try:
            index = int(choice)
            if 0 <= index < len(df):
                display_concept(df.iloc[index])
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def main():
    file_path = 'final_psychological_concepts_quran_dataset.csv'
    df = load_data(file_path)
    
    while True:
        print("\nPsychological Concepts and Quranic Verses Database")
        print("1. View 5 random psychological topics")
        print("2. View the entire database")
        print("3. Quit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            display_random_concepts(df)
        elif choice == '2':
            display_all_concepts(df)
        elif choice == '3':
            print("Thank you for using the database. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()