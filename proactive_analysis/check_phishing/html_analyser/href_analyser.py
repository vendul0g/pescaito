from bs4 import BeautifulSoup
from urllib.parse import urlparse

class HrefAnalyser:
    """
    Class to analyze HTML content to count and differentiate between internal and external links
    based on href, src, and action attributes.
    """

    def __init__(self, html, base_url):
        """
        Initialize with HTML content and the base URL of the site to determine the scope of internal links.

        :param html: HTML content as a string
        :param base_url: The base URL of the website for which the HTML is being analyzed
        """
        self.html = html
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc

    def analyse_links(self):
        """
        Analyze the HTML to find all elements with href, src, or action attributes and classify them as internal or external.

        :return: The difference between the number of internal and external links.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        tags = soup.find_all(['a', 'link', 'script', 'img', 'form'])
        internal_count = 0
        external_count = 0
        external_links = []

        for tag in tags:
            urls = []
            if tag.has_attr('href'):
                urls.append(tag['href'])
            if tag.has_attr('src'):
                urls.append(tag['src'])
            if tag.has_attr('action'):
                urls.append(tag['action'])

            for url in urls:
                if "http" in url:  # Check if it is a valid URL with http(s)
                    full_url = url
                    if not full_url.startswith(('http', 'https')):
                        full_url = urlparse(self.base_url)._replace(path=url, params='', query='', fragment='').geturl()
                    if urlparse(full_url).netloc == self.domain:
                        internal_count += 1
                    else:
                        external_count += 1
                        external_links.append(full_url)

        return internal_count - external_count

# Example usage:
html_content = '''
<html>
<head><link rel="stylesheet" href="https://external.com/styles.css"></head>
<body>
<a href="/internal/link">Internal</a>
<a href="https://external.com/page">External Page</a>
<img src="https://external.com/image.jpg"/>
<form action="/form/submit"></form>
<script src="/scripts.js"></script>
</body>
</html>
'''
analyser = HrefAnalyser(html_content, "https://example.com")
result = analyser.analyse_links()
print(result)  # Output the difference between internal and external links
