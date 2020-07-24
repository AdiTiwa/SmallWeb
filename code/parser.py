file = 'main.txt'

parserTrue = False
f = open(file, 'r')
if (f.read(1) == '<!TKC>'):
    parser = True
else:
    parser = False

def line(msg):
    print(msg)
def img(src, *args, **kwargs):
    pass

line = 1
while parserTrue:
    if(f.read(line) == ' '):
        continue
    elif(f.read(line) == '<TKC!>'):
        break
    elif(f.read(line)[0] == '/' and f.read(line)[1] == '/'):
        continue
    else:
        exec(f.read(line))
        line += 1