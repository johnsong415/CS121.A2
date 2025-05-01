import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

import os

global_file_count = 0

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content


    if resp.status != 200:
        with open('output.txt', 'a') as f:
            print("ERROR:", file=f)
            print(url, file=f)
            print(resp.status, file=f)
            print(resp.error, file=f)
            print("\n", file=f)
        
        return list()

    else:
        link_list = []
        
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        # get links
        for link in soup.find_all('a'):
            link_string = link.get('href')
            if link_string is not None:
                defragged = urldefrag(link_string).url
                if is_valid(defragged):
                    link_list.append(defragged)

        # get body text
        file_path = "file_results/" + "files" + ".txt"
        with open(file_path, "a") as f:
            f.write("BEGIN FILE HERE\n")
            f.write(resp.url)
            f.write("\n")
            f.write(soup.get_text())
            f.write("END FILE HERE\n")

        with open('output.txt', 'a') as f:
            print("Recorded:", file=f)
            print(url, file=f)
            print("\n", file=f)
            
        return link_list

    
    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        # Stay within domain
        if not re.match(
            r"(www)?((.\.ics\.uci\.edu\/?.?)|(.\.cs\.uci\.edu\/?.?)|(.\.informatics\.uci\.edu\/?.?)|(.\.stat\.uci\.edu\/?.?)|(today\.uci\.edu\/department\/information_computer_sciences\/?.?))" # is ? necessary?; do we *need* to consider if www isn't there?
        , parsed.netloc.lower()):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$"
            + r"" , parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
