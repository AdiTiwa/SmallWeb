import tkinter as tk
import string

def label(text, *args, **kwargs):
    size = kwargs.get('size', 'h3')
    if size == 'h1':
        size = 50
    elif size == 'h2':
        size = 40
    elif size == 'h3':
        size = 25
    elif size == 'p':
        size = 10
    elif size == 'h4':
        size = 5
    else:
        size = 25
    label = tk.Label(
        master = self.window,
        text = kwargs.get('text', 'New Label'),
        fg = kwargs.get('fg', 'black'),
        bg = kwargs.get('bg', 'white'),
        size = size
    )
    return label

def parse(file):
    file = open(file).read()
    lineCode = ''
    lineCodes = []
    for x:
        lineCode +=
    if lineCode.endswith(';'):
        if lineCode.count(':') > 1:
            lineCode = lineCode.translate(maketrans(':', '('))
            lineCode = lineCode.translate(maketrans(';', ')'))
            exec(linecode.strip('/n'))
    else:
        break


def commit(object):
    object.pack()

def gridCommit(object, *args, **kwargs):
    row = kwargs.get('row', 0)
    column = kwargs.get('column', 0)
    rowSpan = kwargs.get('rowspan', 1)
    columnSpan = kwargs.get('columnspan', 1)
    object.grid(row = row, column = column, rowspan = rowSpan, columnspan = columnSpan)

def relativeCommit(object, *args, **kwargs):
    xVal = kwargs.get('x', 0)
    yVal = kwargs.get('y', 0)
    object.place(x = x, y = y)
