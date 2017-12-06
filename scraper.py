import urllib2, requests, json, os, errno
from bs4 import BeautifulSoup

gists = json.load(open('codeLinks.json'))
for num, info in gists['blocks'].iteritems():
    if len(num) <= 7:
        url = 'https://gist.github.com/%(user)s/%(number)s' % {'user': info['userId'], 'number': num}

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # search for actual code content on page
        data = soup.find('div', attrs={'class':'repository-content gist-content'})
        if data is not None:
            lines = [] # to contain the lines of code
            for entry in data: # sections / table containers
                table = entry.find('table')
                if table != -1:
                    rows = table.find_all('tr')
                    for row in rows:
                        tds = row.find_all('td')
                        if len(tds) >= 2: # if table data contains info
                            lines.append(tds[1].text)

            # create meta data
            metaUrl = "files2/%s/meta.json" % num

            # create directories if don't exist
            if not os.path.exists(os.path.dirname(metaUrl)):
                try:
                    os.makedirs(os.path.dirname(metaUrl))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            meta_file = open(metaUrl, "w")
            info['number'] = num
            info['url'] = url
            print info
            print
            json.dump(info, meta_file)
            meta_file.close()

            # create file containing project code
            text_file = open("files2/%s/code.js" % num, "w")
            for line in lines:
                text_file.write('%s\n' % line.encode("utf-8"))
            text_file.close()
