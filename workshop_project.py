from collections import Counter
import re
import unicodedata
import string

def clean_text(text):
    # Remove newline characters
    text = text.replace("\n", " ")
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation using regex
    text = re.sub(r'[^\w\s]', '', text)

    # # Remove non-letter characters and convert to lowercase
    text = ''.join([char.lower() for char in text if char in string.ascii_letters])
    
    # Normalize accent marks and tildes
    text = unicodedata.normalize('NFD', text)
    text = ''.join([char for char in text if unicodedata.category(char) != 'Mn'])  # Remove accents
    
    return text

# Function to get the start and end of the book content
def extract_book_content(text):
    start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK"
    
    # Extract the content between the markers
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        raise ValueError("Start or End markers not found in the text")
    
    return text[start_index:end_index]

# Function to count character frequencies
def count_frequencies(text, clean=False):
    if clean:
        text = clean_text(text)
    
    # Count character frequencies
    frequencies = Counter(text)
    
    # Sort results by occurrences
    sorted_frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_frequencies

# Function to process the file
def process_file(file_path, clean=False):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Extract the book content
    book_content = extract_book_content(text)
    
    # Count frequencies
    return count_frequencies(book_content, clean=clean)

def main():

    # File paths for the biggest files per language
    files = {
        'de': '../books/gutenberg/de-10223-8_UTF8.txt',
        'fr': '../books/gutenberg/fr-10682-8_UTF8.txt',
        'es': '../books/gutenberg/es-11529-8_UTF8.txt',
        'en': '../books/gutenberg/en-10012-8_UTF8.txt'
    }

    for lang, file_path in files.items():
        print(f"Processing {file_path} ({lang})...")
        
        # Count character occurrences (after cleaning)
        clean_frequencies = process_file(file_path, clean=True)
        print(f"Character frequencies (cleaned text) for {lang}:")
        for char, freq in clean_frequencies.items():
            print(f"{repr(char)}: {freq}")
        
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
