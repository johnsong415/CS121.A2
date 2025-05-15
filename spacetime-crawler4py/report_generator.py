import hashlib
from urllib.parse import urlparse, urldefrag
from collections import Counter, defaultdict

STOPWORDS_PATH = "spacetime-crawler4py/stopwords.txt"
FILES_TXT_PATH = "spacetime-crawler4py/files.txt"
REPORT_PATH = "spacetime-crawler4py/crawler_report.txt"


'''Loads all stopwords that were taken from https://www.ranks.nl/stopwords'''
def load_stopwords(filepath):
    with open(filepath, 'r') as f:
        return set(word.strip().lower() for word in f.readlines())

'''Cleans up the text from a page and tokenizes it according to Assignment 1, then filters based on
   stopwords and other criteria'''
def clean_and_tokenize(text, stopwords=STOPWORDS_PATH):
    tokens = []
    token_current = ""
    for char in text:
        if char.isalnum() and char.isascii():
            token_current += char.lower()
        elif token_current:
            if token_current and token_current not in stopwords and not token_current.isdigit() and len(token_current) > 1:
                tokens.append(token_current)
            token_current = ""
    return tokens

'''Parses text of each pages file, and gets key metrics for the report.
   Counter idea from https://docs.python.org/3/library/collections.html#collections.Counter'''
def parse_file_txt(lines, stopwords):
    unique_urls = set()
    word_counts = Counter()
    subdomain_counts = defaultdict(int)

    current_url = None
    current_text = []
    longest_url = None
    max_word_count = 0

    for line in lines:
        line = line.strip()
        if line == "BEGIN FILE HERE":
            current_url = None
            current_text = []
        elif current_url is None:
            current_url = urldefrag(line).url
        elif line == "END FILE HERE":
            if current_url:

                unique_urls.add(current_url)
                if "pdf" in current_url.lower() or current_url.lower().endswith(".pdf"):
                  continue
                words = clean_and_tokenize(' '.join(current_text), stopwords)
                word_counts.update(words)

                if len(words) > max_word_count:
                    max_word_count = len(words)
                    longest_url = current_url

                parsed = urlparse(current_url)
                domain = parsed.netloc.lower()
                if domain.startswith("www."):
                  domain = domain[4:]
                if domain.endswith(".uci.edu"):
                    subdomain_counts[domain] += 1
        else:
            current_text.append(line)

    return unique_urls, word_counts, subdomain_counts, longest_url, max_word_count

'''Writes formatted report from crawl to file'''
def write_report(output_path, unique_urls, word_counts, subdomain_counts, longest_url, max_word_count):
    top_words = word_counts.most_common(50)
    sorted_subdomains = sorted(subdomain_counts.items())

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"1. Total Unique Pages: {len(unique_urls)}\n\n")
        f.write(f"2. Longest Page: {longest_url} ({max_word_count} words)\n\n")

        f.write("3. Top 50 Words:\n")
        for word, count in top_words:
            f.write(f"{word}: {count}\n")

        f.write("\n4. Subdomains Found:\n")
        for domain, count in sorted_subdomains:
            f.write(f"{domain}, {count}\n")
