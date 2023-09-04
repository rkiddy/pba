
import requests as req
import re
import argparse


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--auction')
    return parser.parse_args()


CLEANR = re.compile('<.*?>')


if __name__ == '__main__':

    args = arguments()

    if args.auction is None:
        print("\nPlease give me an auction number with --auction <num>\n\n")
        quit()

    page = 1
    done = False

    books = list()

    while True:

        resp = req.get(f"https://pbagalleries.com/auctions/catalog/id/{args.auction}?page={page}")

        lines = resp.text.split('\n')

        founds = list()

        for line in lines:
            if re.search('class="yaaa"', line):
                item = dict()
                item['yaaa'] = line
                founds.append(item)

            if re.search('class="other-info"', line):
                founds[-1]['other'] = line

            if re.search('class="price-info"', line):
                founds[-1]['price'] = line

        print(f"page {page}, founds # {len(founds)}")

        for found in founds:

            book = dict()

            title = re.sub('  ', ' ', re.sub(CLEANR, ' ', found['yaaa']).strip())

            book['Title'] = title

            info_titles = re.findall(r'<div class="title">.*?</div>', found['other'])
            info_values = re.findall(r'<div class="value">.*?</div>', found['other'])

            for idx in range(len(info_titles)):

                key = info_titles[idx][19:]
                key = key[:-6]
                val = info_values[idx][19:]
                val = val[:-6]
                book[key] = val

            prices = re.sub('  ', ' ', re.sub(CLEANR, ' ', found['price']).strip())
            book['Prices'] = prices
            books.append(book)

        if len(founds) == 0:
            break
        else:
            page += 1

    print("")

    for book in books:

        print(f"Title: {book['Title']}")
        print(f"Headline: {book['Headline']}")
        if 'Author' in book:
            print(f"Author: {book['Author']}")
        if 'Date Published' in book:
            print(f"Date Published: {book['Date Published']}")
        print(f"Prices: {book['Prices']}")
        print("")
