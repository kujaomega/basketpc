__author__ = 'kujaomega'
import urllib2
import urllib
import sys
import os.path
from MySQLConnect import MySQLConnect
from bs4 import BeautifulSoup


class BasketParse():
    def __init__(self):
        self.players = 1000

    def getPlayersMarket(self):
        mysql = MySQLConnect()
        mysql.deletePlayersTable()
        mysql.createPlayersTable()
        # count = 1427
        count = 1
        length = 30
        while length == 30:
            url2 = 'http://www.basketpc.com/index.php?mod=busqueda_jugador&pagina=' + `count` + '&orden=ca&sentido=desc&op=&est=T'
            req = urllib2.Request(url2)
            # create a request object
            handle = urllib2.urlopen(req)
            data = handle.read()
            data = data
            # data = data.decode("unicode")
            # data = data.encode("utf8")
            # parser = BeautifulSoup(data, from_encoding='iso-8859-1')
            # data = data.decode('iso-8859-1')
            parser = BeautifulSoup(data)
            # print parser.prettify(formatter=None)
            # data = data.split("<tbody>")
            # data = data[1].split("</tbody>")
            # data = data[0]
            data = []
            table = parser.find('table', attrs={'class':'col-77'})
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            length = len(rows)
            for row in rows:
                cols = row.find_all('td')
                attribs = row.find('a').attrs
                id = attribs['name']
                cols = [ele.text.strip() for ele in cols]
                cols[16] = cols[16][:-1]
                cols.append(id)
                details = self.getPlayerDetails5(id)
                cols = cols + details
                data.append([ele for ele in cols if ele])  # Get rid of empty values

            mysql.insertPlayers(data)
            print count
            count += 1

    def getAuthentication(self, user, password):
        COOKIEFILE = 'cookies.lwp'
        # the path and filename to save your cookies in

        cj = None
        ClientCookie = None
        cookielib = None

        # Let's see if cookielib is available
        try:
            import cookielib
        except ImportError:
            # If importing cookielib fails
            # let's try ClientCookie
            try:
                import ClientCookie
            except ImportError:
                # ClientCookie isn't available either
                urlopen = urllib2.urlopen
                Request = urllib2.Request
            else:
                # imported ClientCookie
                urlopen = ClientCookie.urlopen
                Request = ClientCookie.Request
                cj = ClientCookie.LWPCookieJar()

        else:
            # importing cookielib worked
            urlopen = urllib2.urlopen
            Request = urllib2.Request
            cj = cookielib.LWPCookieJar()
            # This is a subclass of FileCookieJar
            # that has useful load and save methods

        if cj is not None:
        # we successfully imported
        # one of the two cookie handling modules

            if os.path.isfile(COOKIEFILE):
                # if we have a cookie file already saved
                # then load the cookies into the Cookie Jar
                cj.load(COOKIEFILE)

            # Now we need to get our Cookie Jar
            # installed in the opener;
            # for fetching URLs
            if cookielib is not None:
                # if we use cookielib
                # then we get the HTTPCookieProcessor
                # and install the opener in urllib2
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)

            else:
                # if we use ClientCookie
                # then we get the HTTPCookieProcessor
                # and install the opener in ClientCookie
                opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
                ClientCookie.install_opener(opener)
        values = {'campo_login': user,
                          'campo_password': password}
        #We set the user and the pass
        theurl = 'http://www.basketpc.com/index.php?mod=autentificacion'
        # an example url that sets a cookie,
        # try different urls here and see the cookie collection you can make !

        txdata = urllib.urlencode(values)
        # if we were making a POST type request,
        # we could encode a dictionary of values here,
        # using urllib.urlencode(somedict)

        txheaders =  {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
        # fake a user agent, some websites (like google) don't like automated exploration

        try:
            req = Request(theurl, txdata, txheaders)
            # create a request object

            handle = urlopen(req)
            # and open it to return a handle on the url

        except IOError, e:
            print 'We failed to open "%s".' % theurl
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "The error object has the following 'reason' attribute :"
                print e.reason
                print "This usually means the server doesn't exist,',"
                print "is down, or we don't have an internet connection."
            sys.exit()

        #else:
        #    print 'Here are the headers of the page :'
        #    print handle.info()
            # handle.read() returns the page
            # handle.geturl() returns the true url of the page fetched
            # (in case urlopen has followed any redirects, which it sometimes does)

        print
        if cj is None:
            print "We don't have a cookie library available - sorry."
            print "I can't show you any cookies."
        else:
            # print 'These are the cookies we have received so far :'
            # for index, cookie in enumerate(cj):
            #     print index, '  :  ', cookie
            cj.save(COOKIEFILE)                     # save the cookies again
        # url2 = 'http://www.basketpc.com/index.php?mod=busqueda_jugador&pagina=2&orden=&sentido=asc&op=&est=T'
        # req = Request(url2)
        # # create a request object
        # handle = urlopen(req)
        #
        # print handle.read()

    def getPlayerDetails5(self, id):
        """ This method gets the team, the category, fatigue, ef and moral

        :type id: string
        :type self: BasketParse
        """
        url2 = 'http://www.basketpc.com/lib/jugador/ficha_jugador/ver_ficha_jugador.php?id='+id
        req = urllib2.Request(url2)
        # create a request object
        handle = urllib2.urlopen(req)
        data = handle.read()
        parser = BeautifulSoup(data)
        data = []
        if parser.find('a', attrs={'class':'letra_cuerpo'}).contents:
            team = parser.find('a', attrs={'class':'letra_cuerpo'}).contents[0]
        else:
            team = 'sin equipo'
        cat = parser.find_all('span', attrs={'class':'media_jugador'})[1].contents[0].replace(" ", "")
        tab = parser.find('table', attrs={'class':'ficha_jugador'})
        rows = tab.find_all('tr')
        data.append(team)
        data.append(cat)
        for x in range(10, 13):
            cols = rows[x].find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols[1])  # Get rid of empty values
        return data

    def getPlayersByTeams(self, user):
        mysql = MySQLConnect()
        mysql.createPlayersTable4teamsparser()
        mysql.createTeamsTable()

        user = user
        countries = ['SUDAFRICA', 'ALEMANIA', 'ARGENTINA', 'AUSTRALIA', 'BELGICA', 'BRASIL', 'CANADA', 'CHILE', 'CHINA', 'COREA', 'CROACIA', 'EGIPTO', 'ESLOVENIA', 'ESPA\xF1A', 'FRANCIA', 'GRECIA', 'HOLANDA', 'INGLATERRA', 'ISRAEL', 'ITALIA', 'JAPON', 'LITUANIA', 'MEXICO', 'PORTUGAL', 'PUERTO RICO', 'RUSIA', 'SENEGAL', 'SERBIA', 'SUECIA', 'TURQUIA', 'USA', 'VENEZUELA']
        # countries = ['ESPA\xF1A', 'SUDAFRICA', 'ALEMANIA', 'ARGENTINA', 'AUSTRALIA', 'BELGICA', 'BRASIL', 'CANADA', 'CHILE', 'CHINA', 'COREA', 'CROACIA', 'EGIPTO', 'ESLOVENIA', 'FRANCIA', 'GRECIA', 'HOLANDA', 'INGLATERRA', 'ISRAEL', 'ITALIA', 'JAPON', 'LITUANIA', 'MEXICO', 'PORTUGAL', 'PUERTO RICO', 'RUSIA', 'SENEGAL', 'SERBIA', 'SUECIA', 'TURQUIA', 'USA', 'VENEZUELA']
        # divisions = ['1As', '2As', '2Bs', '3As', '3Bs', '3Cs', '3Ds']
        # divisions = ['1As', '2As', '2Bs', '3As', '3Bs', '3Cs', '3Ds', '4As', '4Bs', '4Cs', '4Ds', '4Es', '4Fs', '4Gs', '4Hs']
        divisions = ['1As', '2As', '2Bs']
        for division in divisions:
            print division + '\n'
            for country in countries:
                teams = []
                print country + '\n'
                values = {'pais_equipo': country,
                                  'division_categoria': division}
                url2 = 'http://www.basketpc.com/index.php?mod=clasificacion'
                req = urllib2.Request(url2)
                txdata = urllib.urlencode(values)
                # create a request object
                Request = urllib2.Request
                req = Request(url2, txdata)
                handle = urllib2.urlopen(req)
                data_ranking = handle.read()
                parser = BeautifulSoup(data_ranking)
                data = []
                table_teams = parser.find('table', attrs={'class': 'col-75'})
                table_body = table_teams.find('tbody')
                rows = table_body.find_all('a')
                for row in rows:
                    link = row['href']
                    id_team = link.split('id=')[1]
                    team = row.contents[0].strip().replace("\n", "")
                    team = team.encode('utf8', 'ignore').decode('ascii', 'ignore')
                    # for spain 'ESPA\xF1A' pais.decode('cp1251') pais.decode('latin-1')
                    teams.append([team, id_team, division[0:-1], country.decode('latin-1')])
                    equipo_stats = self.getTeamStats(id_team, team, user)
                    if 0 != len(equipo_stats):
                        mysql.insertPlayersTeamParsing(equipo_stats)
                mysql.insertTeams(teams)

    def getPlayerDetails(self, id, user):
        """ This method gets the team, the category, fatigue, ef and moral

        :type id: string
        :type self: BasketParse
        """
        url2 = 'http://www.basketpc.com/lib/jugador/ficha_jugador/ver_ficha_jugador.php?id=' + str(id)
        req = urllib2.Request(url2)
        # create a request object
        handle = urllib2.urlopen(req)
        data = handle.read()
        parser = BeautifulSoup(data)
        clas = parser.find_all('span', attrs={'class':'media_jugador'})[1].contents[0].replace(" ", "")
        media = parser.find_all('span', attrs={'class':'media_jugador'})[0].contents[0].replace(" ", "")
        tab = parser.find('table', attrs={'class':'ficha_jugador'})
        rows = tab.find_all('tr')
        test = parser.find_all('li')
        if user:
            nombre = test[6].find_all(text=True)[1].strip().replace("\n", "").replace("\t", "")
            edad = test[7].find_all(text=True)[1].strip()
            semana = test[7].find_all(text=True)[3].replace(" ", "")
            nacionalidad = test[8].find_all(text=True)[1].replace(" ", "")
            altura = test[9].find_all(text=True)[1].replace(" ", "")[0:-3]
            peso = test[10].find_all(text=True)[1].replace(" ", "")[0:-2]
            posicion = test[11].find_all(text=True)[1].replace(" ", "")
            clausula = test[21].find_all(text=True)[1].replace(" ", "").replace(".", "")
            ficha = test[22].find_all(text=True)[1].replace(" ", "").replace(".", "")
            contrato = test[23].find_all(text=True)[1].replace(" ", "")[0]
            data = [nombre, edad, semana, nacionalidad, altura, peso, posicion, clausula, ficha, contrato, media]
            data.append(clas)
            for x in range(0, 13):
                cols = rows[x].find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols[1])  # Get rid of empty values
            return data
        else:
            nombre = test[5].find_all(text=True)[1].strip().replace("\n", "").replace("\t", "")
            edad = test[6].find_all(text=True)[1].strip()
            semana = test[6].find_all(text=True)[3].replace(" ", "")
            nacionalidad = test[7].find_all(text=True)[1].replace(" ", "")
            altura = test[8].find_all(text=True)[1].replace(" ", "")[0:-3]
            peso = test[9].find_all(text=True)[1].replace(" ", "")[0:-2]
            posicion = test[10].find_all(text=True)[1].replace(" ", "")
            clausula = test[20].find_all(text=True)[1].replace(" ", "").replace(".", "")
            ficha = test[21].find_all(text=True)[1].replace(" ", "").replace(".", "")
            contrato = test[22].find_all(text=True)[1].replace(" ", "")[0]
            data = [nombre, edad, semana, nacionalidad, altura, peso, posicion, clausula, ficha, contrato, media]
            # nombre, edad, semana,
            data.append(clas)
            for x in range(0, 13):
                cols = rows[x].find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append(cols[1])  # Get rid of empty values
            return data

    def updatePlayersDB(self, user):
        mysql = MySQLConnect()
        ids = mysql.selectIdPlayers()
        players = []
        for id in ids:
            players.append(self.getPlayerDetails(id, user))

    def getTeamStats(self, id_team, team, user):
        url2 = 'http://www.basketpc.com/index.php?mod=plantilla&id=' + id_team
        req = urllib2.Request(url2)
        # create a request object
        handle = urllib2.urlopen(req)
        data_players = handle.read()
        parser = BeautifulSoup(data_players)
        table_players = parser('tbody', limit=5)
        # print table_players
        print team
        equipo_stats = []
        for row2 in table_players:

            attribs = row2.find_all('a')
            # for ele in attribs:
            #     print 'va:' + str(ele['name'])
            id_array = []
            for ele in attribs:
                id_array.append(ele['name'])
            for id in id_array:
                if team != user:
                    stats = self.getPlayerDetails(id, False)
                else:
                    stats = self.getPlayerDetails(id, True)
                stats.append(team)
                stats.append(id)
                equipo_stats.append(stats)
        return equipo_stats

    def getMatches(self):
        mysql = MySQLConnect()
        countries = ['SUDAFRICA', 'ALEMANIA', 'ARGENTINA', 'AUSTRALIA', 'BELGICA', 'BRASIL', 'CANADA', 'CHILE', 'CHINA', 'COREA', 'CROACIA', 'EGIPTO', 'ESLOVENIA', 'ESPA\xF1A', 'FRANCIA', 'GRECIA', 'HOLANDA', 'INGLATERRA', 'ISRAEL', 'ITALIA', 'JAPON', 'LITUANIA', 'MEXICO', 'PORTUGAL', 'PUERTO RICO', 'RUSIA', 'SENEGAL', 'SERBIA', 'SUECIA', 'TURQUIA', 'USA', 'VENEZUELA']
        # paises = ['ESPA\xF1A', 'SUDAFRICA', 'ALEMANIA', 'ARGENTINA', 'AUSTRALIA', 'BELGICA', 'BRASIL', 'CANADA', 'CHILE', 'CHINA', 'COREA', 'CROACIA', 'EGIPTO', 'ESLOVENIA', 'FRANCIA', 'GRECIA', 'HOLANDA', 'INGLATERRA', 'ISRAEL', 'ITALIA', 'JAPON', 'LITUANIA', 'MEXICO', 'PORTUGAL', 'PUERTO RICO', 'RUSIA', 'SENEGAL', 'SERBIA', 'SUECIA', 'TURQUIA', 'USA', 'VENEZUELA']
        # divisiones = ['1As', '2As', '2Bs', '3As', '3Bs', '3Cs', '3Ds']
        # divisions = ['1As', '2As', '2Bs', '3As', '3Bs', '3Cs', '3Ds', '4As', '4Bs', '4Cs', '4Ds', '4Es', '4Fs', '4Gs', '4Hs']
        divisions = ['1As', '2As', '2Bs']
        # for division in divisions:
        #     print division + '\n'
        #     for country in countries:
        #         teams = []
        #         print country + '\n'
        values = {'pais_equipo': countries[0],
                          'division_categoria': divisions[0]}
        url2 = 'http://www.basketpc.com/index.php?mod=listado_resultados'
        req = urllib2.Request(url2)
        txdata = urllib.urlencode(values)
        # create a request object
        Request = urllib2.Request
        req = Request(url2, txdata)
        handle = urllib2.urlopen(req)
        data_ranking = handle.read()
        parser = BeautifulSoup(data_ranking)
        data = []
        table_teams = parser.find('table', attrs={'class': 'col-75'})
        table_body = table_teams.find('tbody')
        rows = table_body.find_all('a')
