import string

palabra = 'gabserra#!!!'

for i in palabra:
    if (i in string.punctuation):
        print(i)
        print('Lol asi no compa')
        break
    print(i)
