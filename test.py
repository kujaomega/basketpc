import sys
from BasketParse import BasketParse


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'update' or sys.argv[1] == 'test':
            if sys.argv[1] == 'update':
                update()
            elif sys.argv[1] == 'test':
                test()
        else:
            print 'The Dataset must be in the same path'
    else:
        print 'Introduce 1 argument'
def test():
    # instantiate the parser and fed it some HTML
    # parser = MyHTMLParser()
    #parser.feed('<html><head><title>Test</title></head>'
    #           '<body><h1>Parse me!</h1></body></html>')
    # parser.feed("http://www.basketpc.com/")
    basketinfo = BasketParse()
    user = '**'
    password = '**'
    equipo = '**'
    basketinfo.getAuthentication(user, password)
    basketinfo.getPlayersByTeams(equipo)

def update():
    print 'update'
    basketinfo = BasketParse()
    user = '**'
    password = '**'
    equipo = '**'
    basketinfo.getAuthentication(user, password)
    basketinfo.updatePlayersDB()
if __name__ == "__main__":
    main()
