import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import os
from datetime import datetime, timedelta
def fetch_yesterdays_articles_bleeping_computer():
    base_url = "https://www.bleepingcomputer.com/news/security/"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        yesterday = datetime.now() - timedelta(1)
        yesterday_str = yesterday.strftime('%B %d, %Y')

        for article in soup.find_all("div", class_="bc_latest_news_text"):
            date_tag = article.find("li", {"class":"bc_news_date"})
            if date_tag and date_tag.text.strip() == yesterday_str:
                a_tag = article.find("a", href=True)
                if a_tag:
                    link = a_tag["href"]
                    if link.startswith('http'):
                        links.append(link)
        
        print(f"Found {len(links)} articles from yesterday in bleepingcomputer.")
        return links
    else:
        print(f"Failed to retrieve page: Status Code {response.status_code}")
        return []
def fetch_all_articles_it_connect():
    base_url = "https://www.it-connect.fr/actualites/actu-securite/"
    response = requests.get(base_url)
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = yesterday.strftime('%d/%m/%Y')  # Corrected date format

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []

        for article in soup.find_all("article", class_=lambda value: value and value.startswith("post-")):
            date_tag = article.find("time", {"class": "entry-date"})
            if date_tag and date_tag.text.strip() == yesterday_str:
                link = article.find("a", href=True)["href"]
                links.append(link)
        
        print(f"Found {len(links)} articles from yesterday in ITCONNECT.")
        return links
    else:
        print(f"Failed to retrieve page: Status Code {response.status_code}")
        return []
def fetch_links_the_hacker_news():
    url = "https://thehackernews.com/search/label/Vulnerability"
    response = requests.get(url)
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = yesterday.strftime('%b %d, %Y')  
    links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for part in soup.find_all("div", class_="item-label"):
            date_tag = part.find("span", class_="h-datetime")
            if date_tag:
                date_text = date_tag.text.strip()
                
                date_text = ''.join(filter(lambda x: x in set(chr(i) for i in range(128)), date_text))
                try:
                    article_date = datetime.strptime(date_text, '%b %d, %Y').strftime('%b %d, %Y')
                    if article_date == yesterday_str:
                        link = part.find_parent("div", class_="body-post").find("a", class_="story-link")
                        if link and 'href' in link.attrs:
                            links.append(link['href'])
                except ValueError as e:
                    print(f"Error parsing date: {date_text} - {e}")
        print(f"Found {len(links)} articles from yesterday in the_hacker_news.")
        return links
    else:
        print(f"Failed to fetch links. Status Code: {response.status_code}")
        return []


def clean_summary_bleeping_computer(summary):
    soup = BeautifulSoup(summary, 'html.parser')
    
    unwanted_selectors = [
        'div.cz-related-article-wrapp',
        'div.cz-full-bio-wrapp',
        'div.cz-news-tags-wrap'
    ]
    
    for selector in unwanted_selectors:
        for elem in soup.select(selector):
            elem.decompose()  
    cleaned_summary = soup.get_text(separator=' ', strip=True)
    return cleaned_summary
def clean_summary_it_conncet(summary_html):
    soup = BeautifulSoup(summary_html, 'html.parser')
    end_patterns = [
        'Source :', 'Source:', 'Voir bio complète', 'See Full Bio'
    ]
    for pattern in end_patterns:
        if pattern in summary_html:
            summary = summary_html.split(pattern)[0]
            break
    
    unwanted_selectors = [
        'div.aioseo-author-bio-compact',  
        'div.source',                      
        'div.author-bio-link', 
        'div.author-socials',
        'div.bio',                         
        'div[role="note"]',                
        'span.some-class',                 
        'footer',                         
        'nav',                            
        'header',
        'p > a[href*="bleepingcomputer.com"]'
    ]
    
    for selector in unwanted_selectors:
        for elem in soup.select(selector):
            elem.extract()  
    
    cleaned_summary = soup.get_text(strip=True)
    return cleaned_summary
def clean_summary_the_hacker_news(summary_html):
    soup = BeautifulSoup(summary_html, 'html.parser')
    unwanted_selectors = [                
        'footer',                         
        'nav',                            
        'header',
        'div.cf'
    ]
    
    for selector in unwanted_selectors:
        for elem in soup.select(selector):
            elem.extract()  
    
    cleaned_summary = soup.get_text(strip=True)
    return cleaned_summary
def extract_cve_identifiers(text):
    cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')
    return cve_pattern.findall(text)
def fetch_cvss_score(cve_id):
    headers={
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Accept-Language': 'en-US,en;q=0.9',
             'Referer':'https://www.google.com/',
             'Connection': 'keep-alive',
             }
    url=f"https://www.cvedetails.com/cve/{cve_id}/"
    response=requests.get(url, headers=headers)
    if response.status_code==200:
        soup=BeautifulSoup(response.content,'html.parser')
        cvss_score_elem=soup.find('div',{'class':'cvssbox'})
        if cvss_score_elem:
            cvss_score=cvss_score_elem.get_text().strip()
            return cvss_score
        else :
            print(f"CVSS score not found for the {cve_id}")
            return None
    else:
     print(f"Failed to fetch CVSS score for {cve_id}")
    return None
def determine_severity(cvss_score):
    try:
        cvss_score = float(cvss_score)
        if cvss_score >= 0.0 and cvss_score < 4.0:
            return "Low"
        elif cvss_score >= 4.0 and cvss_score < 7.0:
            return "Medium"
        elif cvss_score >= 7.0 and cvss_score < 9.0:
            return "High"
        elif cvss_score >= 9.0 and cvss_score <= 10.0:
            return "Critical"
        else:
            return "Unknown"
    except ValueError:
        print(f"Invalid CVSS score: {cvss_score}")
        return "Unknown"
def scrape_article_details_bleeping_computer(links):
    articles = []
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    session = requests.Session()
    
    for link in links:
        time.sleep(random.uniform(1, 3))  
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        response = session.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for article in soup.find_all("div", class_="article_section"):
       
                title_tag = soup.find("h1", )
                summary_tag = soup.find("div", {"class": "articleBody"})
                published_date_tag = soup.find("li", {"class": "cz-news-date"})

            if title_tag and summary_tag and published_date_tag:
                title = title_tag.get_text(strip=True)
                summary = str(summary_tag)
                cleaned_summary = clean_summary_bleeping_computer(summary)
                cve_identifiers = extract_cve_identifiers(cleaned_summary) 
                cvss_scores = []
                severities = []
                published_date = published_date_tag.get_text(strip=True)
                for cve_id in cve_identifiers:
                    cvss_score = fetch_cvss_score(cve_id)
                    if cvss_score:
                        severity = determine_severity(cvss_score)
                    else:
                        severity = "Unknown"
                        cvss_score = "Unknown"  

                    cvss_scores.append(cvss_score)
                    severities.append(severity)
                source=link
            

                articles.append({
                    "title": title,
                    "source": source,
                    "summary": cleaned_summary,
                    "published_date": published_date,
                     "cve_identifiers": ', '.join(cve_identifiers) if cve_identifiers else 'None',
                    "cvss_scores": ', '.join(filter(None, cvss_scores)), 
                    "severities": ', '.join(filter(None, severities))
                })
                print(f"Scraped article: {title}")  
            else:
                print(f"Missing data in article: {link}")  
        else:
            print(f"Failed to retrieve article from {link}: Status Code {response.status_code}")
    
    return articles
def scrape_article_details_it_connect(links):
    articles = []

    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            title_tag = soup.find("h1", class_="cm-entry-title")
            summary_tag = soup.find("div", class_="cm-entry-summary")
            date_tag = soup.find("time", class_="entry-date")

            if title_tag and summary_tag and date_tag:
                title = title_tag.get_text(strip=True)
                summary_html = str(summary_tag)
                cleaned_summary = clean_summary_it_conncet(summary_html)
                cve_identifiers = extract_cve_identifiers(cleaned_summary) 
                cvss_scores = []
                severities = []

                for cve_id in cve_identifiers:
                    cvss_score = fetch_cvss_score(cve_id)
                    if cvss_score:
                        severity = determine_severity(cvss_score)
                    else:
                        severity = "Unknown"
                        cvss_score = "Unknown"  

                    cvss_scores.append(cvss_score)
                    severities.append(severity)

             
                published_date_str = date_tag.get("datetime", "")
                published_date = re.search(r'\d{4}-\d{2}-\d{2}', published_date_str)
                published_date = datetime.strptime(published_date.group(), '%Y-%m-%d').date() 
                source=link
                
                articles.append({
                    "title": title,
                    "source":source,
                    "summary": cleaned_summary,
                    "published_date": published_date,
                    "cve_identifiers": ', '.join(cve_identifiers) if cve_identifiers else 'None',
                    "cvss_scores": ', '.join(filter(None, cvss_scores)),  
                    "severities": ', '.join(filter(None, severities))
                    
                })
            else:
                print(f"Missing required tags for article: {link}")

    return articles
def fetch_detailed_links_the_hacker_news(links):
    articles = []
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
          
            title_tag = soup.find("h1", class_="story-title")
            for source in soup.find_all("h1" , class_="story-title"):
                summary_tag = soup.find("div", class_="articlebody")
                date_tag = soup.find("span", class_="author")
            
            if title_tag and summary_tag and date_tag:
            
                title = title_tag.get_text(strip=True)
                summary_html = summary_tag.get_text(strip=True)
                summary = clean_summary_the_hacker_news(summary_html)
                
                published_date = date_tag.get_text(strip=True)
    
             
                cve_identifiers = extract_cve_identifiers(summary) 
                
                if cve_identifiers is None:
                    print(f"No CVE identifiers found for article: {link}")
                    cve_identifiers = []  

               
                cvss_scores = []
                severities = []

                for cve_id in cve_identifiers:
                    cvss_score = fetch_cvss_score(cve_id)
                    if cvss_score:
                        severity = determine_severity(cvss_score)
                    else:
                        severity = "Unknown"
                        cvss_score = "Unknown"

                    cvss_scores.append(cvss_score)
                    severities.append(severity)
               
                
                source=link
                articles.append({
                    "title": title,
                    "source":source,
                    "summary":summary,
                    "published_date": published_date,
                    "cve_identifiers": '\n '.join(cve_identifiers) if cve_identifiers else 'None',
                    "cvss_scores": '\n '.join(filter(None, cvss_scores)),
                    "severities": '\n'.join(filter(None, severities))
                    
                })
            else:
                print(f"Missing required tags for article: {link}")
        else:
            print(f"Failed to fetch article: {link}. Status Code: {response.status_code}")

    return articles
def save_article_to_file(article, bulletin_number):
    
    title = article.get('title', 'Unknown Title')
    date = article.get('published_date', 'Unknown Date')
    cve = article.get('cve_identifiers', 'None')
    cvss = article.get('cvss_scores', 'Unknown')
    description = article.get('summary', 'No description available')
    source = article.get('source', 'No source available')


yesterday_articles_the_hacker_news = fetch_links_the_hacker_news()
print(yesterday_articles_the_hacker_news)
yesterday_articles_it_connect = fetch_all_articles_it_connect()
print(yesterday_articles_it_connect )
# Example usage
yesterday_articles_bleeping = fetch_yesterdays_articles_bleeping_computer()
print(yesterday_articles_bleeping )
bleeping_computer_articles = scrape_article_details_bleeping_computer(yesterday_articles_bleeping)
it_connect_articles = scrape_article_details_it_connect(yesterday_articles_it_connect)
hacker_news_articles = fetch_detailed_links_the_hacker_news(yesterday_articles_the_hacker_news)

all_articles = bleeping_computer_articles + it_connect_articles + hacker_news_articles
yesterday = datetime.now() - timedelta(1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
df = pd.DataFrame(all_articles)
file_name = f"{yesterday_str}_articles.csv"
df.to_csv(file_name, index=False, encoding='utf-8')
print(f"Articles saved to {file_name}")
