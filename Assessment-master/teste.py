from tabulate import tabulate

dicionario = [('alexandre', '456123789'), ('anderson', '1245698456'),
                ('antonio','123456456'), ('carlos', '91257581'),
                ('cesar','987458'), ('rosemary','789456125') ]

headers = ["Nr." ,  " Usuário "   ,    "Espaço utilizado "  ,"  % do uso"]
print(tabulate(dicionario, headers))