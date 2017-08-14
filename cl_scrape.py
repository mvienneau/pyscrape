import pycurl, json, yagmail, argparse
from StringIO import StringIO
from bs4 import BeautifulSoup

EMAIL_ADDR = 'your_email_address'
TO = 'email@mail.com'
SUBJECT = 'craigslist digest'
PASS = 'your_email_password'
yag = yagmail.SMTP(EMAIL_ADDR, PASS)



def format_results(results):
    """
    Format the dictionary into a nice email
    :param results: The dictionary {title: [price, url]}
    :return:
    """
    contents = []
    for k,v in results.iteritems():
        price = v[0]
        url = v[1]
        contents.append(k)
        contents.append(" %i" % price)
        if "craigslist.org" in url:
            contents.append(url)
        else:
            contents.append("https://boulder.craigslist.org" + url)
    return contents

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process queries and price')
    parser.add_argument('--queries', nargs='+')
    parser.add_argument('--prices', type=int, nargs='+')
    args = parser.parse_args()

    query = args.queries[0]
    max_price = args.prices[0]

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://boulder.craigslist.org/search/sss?query=' + query + '&sort=rel')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    data = buffer.getvalue()

    soup = BeautifulSoup(data)

    d = {}
    items = soup.find_all('a', class_='result-title hdrlnk')
    for title in items:
        try:
            price = title.next_sibling.next_sibling('span', class_='result-price')
            if price:
                price = price[0].text
                price = int(str(price).strip('$'))
                if price < int(max_price):
                    d[str(title.text)] = [price, title['href']]
        except AttributeError as e:
            d[str(title.text)] = [0, title['href']]

    contents = format_results(d)
    with open('results.json', 'w') as fp:
        json.dump(d, fp)

    yag.send(TO, SUBJECT, contents = contents)
