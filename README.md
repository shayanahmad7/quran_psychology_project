# Psychological Concepts and Quranic Verses Matcher

This project aims to create a database that matches psychological concepts with relevant verses from the Quran. It involves web scraping, data processing, API interactions, and a user interface for exploring the final dataset.

## Project Structure

1. `scraping.py`: Scrapes psychological concepts from a website.
2. `verse_matching.py`: Matches each concept with a relevant Quranic verse using GPT-3.5.
3. `data_cleaning.py`: Cleans and structures the matched data.
4. `quran_api.py`: Fetches additional details about Quranic verses from an API.
5. `main.py`: Provides a user interface to explore the final dataset.

## Setup and Installation

1. Clone this repository:
   https://github.com/shayanahmad7/quran_psychology_project

2. Create a virtual environment and activate it:
   `python -m venv venv
   source venv/bin/activate`

   On Windows,use
   `venv\Scripts\activate`

4. Install the required packages:
   `pip install -r requirements.txt`

5. Create a `.env` file in the project root and add your OpenAI API key:
   `OPENAI_API_KEY=your_api_key_here`


## Running the Project

Follow these steps in order:

1. Scrape psychological concepts:
   `python scraping.py`

This will create `psychological_concepts.csv`.

2. Match concepts with Quranic verses:
  `python verse_matching.py`

This will create `psychological_concepts_with_verses.csv`.

3. Clean and structure the data:
  `python data_cleaning.py`

This will create `cleaned_psychological_concepts.csv`.

4. Fetch additional Quranic verse details:
   `python quran_api.py`

This will create `final_psychological_concepts_quran_dataset.csv`.

5. Run the user interface:
   `python main.py`

   This will allow you to explore the final dataset interactively.

## File Descriptions

- `scraping.py`: Uses BeautifulSoup to scrape psychological concepts from https://helpfulprofessor.com/psychological-concepts/.
- `verse_matching.py`: Uses OpenAI's GPT-3.5 to match each psychological concept with a relevant Quranic verse.
- `data_cleaning.py`: Cleans and structures the data from the GPT-3.5 output.
- `quran_api.py`: Interacts with the Quran.com API to fetch additional details about the verses.
- `main.py`: Provides a command-line interface for users to explore the final dataset.

## Output Files

- `psychological_concepts.csv`: Initial scraped data.
- `psychological_concepts_with_verses.csv`: Concepts matched with Quranic verses.
- `cleaned_psychological_concepts.csv`: Cleaned and structured data.
- `final_psychological_concepts_quran_dataset.csv`: Final dataset with additional Quranic verse details.

## Notes

- Ensure you have a stable internet connection when running `verse_matching.py` and `quran_api.py`.
- The project uses rate limiting to avoid overwhelming APIs. Be patient when running these scripts.
- Make sure your OpenAI API key is valid and has sufficient credits.

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
