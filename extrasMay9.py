"""
@app.route('/wiki/<title>/infobox')
def wikibox(title):
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    text = ''
    #items = []
    regex = re.compile('infobox.*')
    for info in soup.find('table', {"class":regex}):
        for data in info.find_all('tr'):
            #text += info.text
            #text += "\n"
            dataStr = data.text.replace('\xa0', ' ')
            dataStr = dataStr.replace('\n',' ')
            dataStr = dataStr.replace('\ufeff',' ')
            #items.append(dataStr)
            text += dataStr
        #text += "\n"
    return text
    #return json.dumps(items)
"""

@app.route('/wiki/<title>/table')
def wikitable2(title):
    tableStuff = ""
    regex = re.compile('\u\w*')   
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    tableList = []
    tableStr = ""
    for stuff in soup.find_all('table'):
        #tableStuff += stuff.get_text()
        tableStr = stuff.get_text()
        tableStr = tableStr.replace(regex.pattern, ' ')
        tableStr = tableStr.replace('\xa0', ' ')
        tableStr = tableStr.replace('\n',' ')
        tableStr = tableStr.replace('\ufeff',' ')
       
        tableStr = tableStr.strip()
        tableList.append(tableStr)
    return json.dumps(tableList)

@app.route('/wiki/<title>/tableByHeader')
def wikitableH(title):
    headerText = ""
    sections = {}
    count = 0
    #nonAllowed = ["Bibliography", "General references", "Citations", "Contents", "Navigation menu", "Notes", "References", "See also", "External links"]
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    

    for header in soup.find_all('h3'):
        paras = ""
        hName = header.text
        for tbl in header.find_all('table'):
             
            rows = tbl.find_all('tr')
            #tblName = count
            #tblName = tbl['class']

            """
            td = tr.find_all('td', "class":"infobox-data")
            th = tr.find_all('th', {"class":"infobox-header"})
            thLabel = tr.find_all('th', {"class":"infobox-label"})
            """
            tempDict = {}
            for tr in rows:
                td = tr.find_all('td')
                th = tr.find('th')
                nextNode = tr
                if th != None:           
                    if td == None:
                        nextTh = tr.nextSibling.find('th')
                        nextTd = tr.nextSibling.find_all('td')
                        row = [i.text for i in nextTd]
                        tempDict.update({nextTh.text:row})
                    else:
                        row = [i.text for i in td]
                        tempDict.update({th.text:row})
            count+=1
            sections.update({hName:tempDict})   

    return sections


@app.route('/wiki/<title>/bestTable')
def wikibesttable(title):
    headerText = ""
    tables = {}
    count = 0
    
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    col_name = ""
    col_text = ""
    
    stuff = {}
    count = 0
    for tbl in soup.find_all('table'):
        
        rows = tbl.findAll('tr')
        #tblName = count
        tblName = tbl['class']

        """
        td = tr.find_all('td', "class":"infobox-data")
        th = tr.find_all('th', {"class":"infobox-header"})
        thLabel = tr.find_all('th', {"class":"infobox-label"})
        """
        tempDict = {}
        for tr in rows:
            td = tr.find_all('td')
            th = tr.find('th')
            nextNode = tr
            if th != None:           
                if td == None:
                    nextTh = tr.nextSibling.find('th')
                    nextTd = tr.nextSibling.find_all('td')
                    row = [i.text for i in nextTd]
                    tempDict.update({nextTh.text:row})
                else:
                    row = [i.text for i in td]
                    tempDict.update({th.text:row})
        count+=1
        stuff.update({tblName:tempDict})   

    return stuff
    """
    for row in rows:
        cols =row.find_all('td')
        for col in cols:
            if col.has_attr('class'):
                col_name = col.text
            else:
                col_text = col.text
            tables.update({col_name:col_text})
    
    for tables in soup.find_all('table'):
        table_name = 
        if header.text.find("edit") != -1:
                end = header.text.find('[')
                hName = header.text[:end]
        if hName not in nonAllowed:
            nextNode = header
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break
                if isinstance(nextNode, NavigableString):
                    paras += nextNode.strip()
                if isinstance(nextNode, Tag):
                    if nextNode.name == 'h2':
                        break
                    paras += nextNode.get_text(strip=True).strip()
                sections.update({hName:paras})
                count += 1
        """
    #return tables

    """
@app.route('/wiki/<title>/infoTable')
def wikiinfoTable(title):
    tableDict = {}

    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    regex = re.compile('infobox.*')
    for info in soup.find('table', {"class":regex}):
        tableRows = []             
        t_headers = info.find('th')

        if t_headers is not None:
            #row = []
            for th in t_headers:                 
                txt = unicodedata.normalize('NFC', th.get_text())
                txt = txt.replace('\xa0', '')
                txt = txt.replace(u'\u2013', u'-')
                txt = txt.strip()
                if len(txt) > 0 and len(txt) < 100:
                    row.append(txt)
            if row:
                tableRows.append(row)
        t_rows = info.find_all('tr')            
        for tr in t_rows:
            th = tr.find('th')
            t_head = th.text

            td = tr.find_all('td')
            row = []
            for i in td: 
                txt = unicodedata.normalize('NFC', i.text)
                txt = txt.replace('\xa0', '')
                txt = txt.strip()
                if len(txt) > 0 and len(txt) < 100:
                    row.append(txt)
            if row:
                tableRows.append(row)
        tableDict.update({header.text:tableRows})
        
    return tableDict

@app.route('/wiki/<title>/bestTable')
def wikibesttable(title):
    headerText = ""
    tables = {}
    count = 0
    
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    col_name = ""
    col_text = ""
    
    stuff = {}
    count = 0
    for tbl in soup.find_all('table'):
        
        rows = tbl.findAll('tr')
        #tblName = count
        tblName = tbl['class']

        
        #td = tr.find_all('td', "class":"infobox-data")
        #th = tr.find_all('th', {"class":"infobox-header"})
        #thLabel = tr.find_all('th', {"class":"infobox-label"})
        
        tempDict = {}
        for tr in rows:
            td = tr.find_all('td')
            th = tr.find('th')
            nextNode = tr
            if th != None:           
                if td == None:
                    nextTh = tr.nextSibling.find('th')
                    nextTd = tr.nextSibling.find_all('td')
                    row = [i.text for i in nextTd]
                    tempDict.update({nextTh.text:row})
                else:
                    row = [i.text for i in td]
                    tempDict.update({th.text:row})
        count+=1
        stuff.update({tblName:tempDict})   

    return jsonify(stuff)




@app.route('/wiki/<title>/<section>')
def wiki(title, section):
    text = "" + section
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    for para in soup.find_all('p'):
        text += para.text
    #global stud_name
    return text



@app.route('/wiki/<title>/table/<identifier>')
def wikitable(title, identifier):
    tableStuff = ""
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    
    for stuff in soup.find_all('table', {"class":identifier}):
        tableStuff += stuff.get_text()
    

    return tableStuff
