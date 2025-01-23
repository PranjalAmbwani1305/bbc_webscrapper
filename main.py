import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_article_links(base_url, keyword):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href.startswith("http"):
                href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"
            if keyword.lower() in a.text.lower() or keyword.lower() in href.lower():
                links.append(href)

        return links
    except Exception as e:
        st.error(f"An error occurred while fetching links: {e}")
        return []

def extract_article(link, keyword):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('div', class_='article-body')
        if content:
            article_text = "\n".join(p.get_text() for p in content.find_all('p'))
        else:
            paragraphs = soup.find_all('p')
            article_text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        if keyword.lower() not in article_text.lower():
            return "No relevant content found for the keyword."
        
        return article_text if article_text else "No article content found."
    except Exception as e:
        return f"Error extracting article: {e}"

def main():
    st.set_page_config(page_title="BBC News Article Scraper", page_icon="📰")
    st.title("BBC News Article Scraper")
    st.write("Search for articles on **BBC News** using a keyword and extract their content dynamically.")

    base_url = "https://www.bbc.com/"

    keyword = st.text_input("Keyword to Search (Any)", "રશિયા યુક્રેન યુદ્ધ")

    if st.button("Find and Extract Articles"):
        if keyword:
            with st.spinner("Searching for articles..."):
                links = fetch_article_links(base_url, keyword)

                if links:
                    st.success(f"Found {len(links)} articles with the keyword '{keyword}':")
                    for i, link in enumerate(links, start=1):
                        st.write(f"**Article {i}:** [Link]({link})")
                        with st.spinner("Extracting article content..."):
                            article_content = extract_article(link, keyword)
                            st.write(f"**Article Content:**\n{article_content}\n")
                else:
                    st.warning(f"No articles found with the keyword '{keyword}'.")
        else:
            st.error("Please enter a keyword.")

if __name__ == "__main__":
    main()
