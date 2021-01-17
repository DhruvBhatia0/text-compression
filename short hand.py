'''
Grade 12 CS Project
17-01-2021
'''

import pickle
import csv
import time

# Function Definition
# >>File Handling
f = ''


def getfile():
    global f
    f = input(
        'please enter the name of the text file as <name>.txt\nensure the file is in the same folder as the code\n')
    return f


def read(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content


def writefile(filename, s):
    ft = open(filename, 'w')
    ft.write(s)
    ft.close()


def log(filename, action):
    result = time.localtime()
    date = str(result.tm_mday) + '-' + str(result.tm_mon) + '-' + str(result.tm_year)
    tyme = str(result.tm_hour) + ':' + str(result.tm_min) + ':' + str(result.tm_sec)
    with open('logs.csv', 'a') as logs:
        writer = csv.writer(logs)
        writer.writerow([date, tyme, filename, action])

    # print(date)


# >>Compression
def sort(letter_f):
    for i in range(len(letter_f)):
        for j in range(len(letter_f) - 1):
            if letter_f[j][1] > letter_f[j + 1][1]:
                letter_f[j], letter_f[j + 1] = letter_f[j + 1], letter_f[j]


def create_char_and_frequency_list(content):
    letters = []
    letters_f = []
    for letter in content:
        if letter not in letters:
            letters.append(letter)
            letters_f.append([letter, 1])
        else:
            for i in range(len(letters_f)):
                if letters_f[i][0] == letter:
                    letters_f[i][1] += 1
                    break
    return letters_f, letters


def build_base_level(letter_f):
    sort(letter_f)
    tree = []
    tree.append(letter_f)
    return tree, letter_f


def build_tree(letter_f):
    new_lvl = []
    if len(letter_f) > 1:
        sort(letter_f)
        letter_f[0].append('0')
        letter_f[1].append('1')
        combined_char = letter_f[0][0] + letter_f[1][0]
        combined_freq = letter_f[0][1] + letter_f[1][1]
        new_lvl.append([combined_char, combined_freq])
        new_lvl = new_lvl + letter_f[2:]
        letter_f = new_lvl
        tree.append(letter_f)
        build_tree(letter_f)
    return tree


def get_binary(tree, letters):
    binary_code = []
    for i in letters:
        code = ''
        repeat = ''
        for j in range(len(tree) - 2, -1, -1):
            for k in range(len(tree[j])):
                if i in tree[j][k][0] and tree[j][k][0] != repeat:
                    repeat = tree[j][k][0]
                    code += tree[j][k][2]
        binary_code.append([i, code])
    return binary_code


def build_new_file(content, binary_code):
    content = list(content)
    for i in range(len(binary_code)):
        for j in range(len(binary_code) - 2):
            if binary_code[j][1] < binary_code[j + 1][1]:
                binary_code[j], binary_code[j + 1] = binary_code[j + 1], binary_code[j]
    new_content = ''
    for i in content:
        for j in binary_code:
            if i == j[0]:
                new_content = new_content + j[1]
                break
    return new_content


def decompress():
    name1 = input('please enter the complete name of the file containing the content that was compressed\n')
    name2 = input('please enter the complete name of the file containing the binary key\n')
    try:
        f = open(name1, 'rb')
        content_ = pickle.load(f)
        f.close()
    except:
        print('unexpected error, please ensure file exists')
        return
    try:
        f = open(name2, 'rb')
        binary_code = pickle.load(f)
        f.close()
    except:
        print('unexpected error, please ensure file exists')
        return
    # reobtaining the 1s and 0s as a string
    content = "{0:b}".format(content_)
    content = str(content)
    temp = ''
    new_content = ''
    for i in content:
        temp = temp + i
        for j in binary_code:
            if j[1] == temp:
                temp = ''
                new_content += j[0]
                break
    name = name1[:5] + '_decompressed.txt'
    try:
        f = open(name, 'w')
        f.write(new_content)
        f.close()
    except:
        print('error, unable to write data in file')


def make_compressed_file(file, c_content, b_key):
    name = file.split('.')
    name = name[0]
    name1 = name + '_compressed.dat'
    name2 = name + '_key.dat'
    content = int(c_content, 2)
    f = open(name1, 'wb')
    pickle.dump(content, f)
    f.close()
    fl = open(name2, 'wb')
    pickle.dump(b_key, fl)
    fl.close()
    print('compressed files created')


def shorthand():
    s = read(getfile())
    print('''
            processing. . . 
            In shorthand notation, the following words will be omitted -
                 - the
                 - a
                 - an
            Furthermore, word contractions will be made where possible. eg. we are becomes we're''')
    # contractions being made include you're, we're, they're, it's, what's, how's, can't, aren't, weren't, wouldn't, couldn't, etc.
    print('number of characters in original file: ', len(s))
    s = s.split()
    length = len(s)
    i = 0
    while i < length:

        if s[i] == 'the' or s[i] == 'a' or s[i] == 'an':
            length -= 1
            del s[i + 1]
        if i < len(s) - 1:
            if s[i] in ['could', 'would', 'should', 'are', 'were', 'where']:
                if s[i + 1] == 'have':
                    s[i] = s[i] + '\'ve'
                    del s[i + 1]
                    length -= 1
                elif s[i + 1] == 'not':
                    s[i] = s[i] + 'n\'t'
                    length -= 1
                    del s[i + 1]
            elif s[i] in ['it', 'what', 'how', 'where'] and s[i + 1] == 'is':
                length -= 1
                del s[i + 1]
                s[i] = s[i] + '\'s'
            elif s[i] == 'cannot':
                s[i] = 'can\'t'
            elif s[i] == 'can' and s[i + 1] == 'not':
                s[i] = 'can\'t'
                length -= 1
                del s[i + 1]
            elif s[i] in ['you', 'we', 'they', 'how'] and s[i + 1] == 'are':
                length -= 1
                del s[i + 1]
                s[i] = s[i] + '\'re'
        i += 1

    s = ' '.join(s)
    print('number of characters in altered file: ', len(s))
    writefile(f, s)
    log(f, 'shorthand')


def shortform():
    D = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
         'eight': '8', 'nine': '9'}
    s = read(getfile())

    n = int(input('How many unique words do you want to replace with short forms?'))
    for i in range(n):
        key = input('Enter word')
        val = input('Enter abbreviation/short form: ')
        D[key] = val
    print('number of characters in original file: ', len(s))
    s = s.split()
    for i in range(len(s)):
        if s[i] in D.keys():
            s[i] = D[s[i]]

    s = ' '.join(s)
    print('number of characters in altered file: ', len(s))
    writefile(f, s)
    log(f, 'shortform')


def analytics():
    # word count, character count, no. of sentences, 10 most common words
    s = read(getfile())
    print('''
    processing. . . ''')
    charcount = len(s)
    sentcount = len(s.split('.'))
    s = s.split()
    wordcount = len(s)
    D = {}
    for i in range(len(s)):
        for j in ('.', '!', ',', '?', ')', '('):
            if j in s[i]:
                tr = list(s[i])
                o = 0
                re = len(tr)
                while o < re:
                    if tr[o] in ('.', '!', ',', '?', ')', '('):
                        del tr[o]
                        o -= 1
                        re -= 1
                    o += 1
                s[i] = ''.join(tr)
        if s[i] in D.keys():
            pass
        else:
            D[s[i]] = s.count(s[i])
    wc = list(D.values())
    wc.sort(reverse=True)
    mostcommon = {}
    if len(wc) < 10:
        num = len(wc)
    else:
        num = 10
        if wc[9] == wc[10]:
            num += 1
    for i in range(num):
        for word, count in D.items():
            if count == wc[i]:
                mostcommon[word] = count
    print('Word count: ', wordcount)
    print('No. of characters: ', charcount)
    print('No. of sentences: ', sentcount)
    print('Most common words: ')
    for word, count in mostcommon.items():
        print('\t', word, ' : ', count)
    log(f, 'analytics')
    print()


def replacer():
    D = {}
    Dr = {}
    s = read(getfile())
    s = s.split()
    n = int(input('How many unique words do you want to replace?'))
    for i in range(n):
        key = input('Enter unique word')
        val = input('Enter replacement: ')
        rep = input('''Replace (a/b)
    a) First occurence
    b) All occurences''')
        for j in range(len(s)):
            if s[j] == key:
                s[j] = val
                if rep == 'a':
                    break

    s = ' '.join(s)
    writefile(f, s)
    log(f, 'replacer')
    print('replacements have been made')


def punctuator():
    # full stop & comma spacing, capitalizing letters, last full stop
    # bracket space
    s = read(getfile())
    s = s.split()
    s[0] = s[0].capitalize()
    i = 0
    k = len(s)
    while i < k:
        if '.' in s[i]:
            temp = s[i].split('.')
            l = len(temp)
            k += l - 1
            s[i] = temp[0] + '.'
            for j in range(1, l):
                if len(temp[j]) > 0:
                    temp[j] = temp[j].capitalize()
                s.insert(i + 1, temp[j])
                if j == l - 1:
                    pass
                else:
                    s[i + j] += '.'

            i += l - 1
        i += 1
    g = len(s) - 1

    if len(s[g]) > 0 and s[g][len(s[g]) - 1] != '.':
        s[g] += '.'
    k = len(s)
    i = 0
    while i < k:
        if ',' in s[i]:
            temp = s[i].split(',')
            l = len(temp)
            k += l - 1
            s[i] = temp[0] + ','
            for j in range(1, l):
                s.insert(i + 1, temp[j])
                if j == l - 1:
                    pass
                else:
                    s[i + j] += ','
            i += l - 1
        i += 1

    k = len(s)
    i = 0
    while i < k:
        if ')' in s[i] and s[i][-2] + s[i][-1] != ').':
            temp = s[i].split(')')
            l = len(temp)
            k += l - 1
            s[i] = temp[0] + ')'
            for j in range(1, l):
                s.insert(i + 1, temp[j])
                if j == l - 1:
                    pass
                else:
                    s[i + j] += ')'
            i += l - 1
        i += 1

    k = len(s)
    i = 0
    while i < k:
        if '(' in s[i]:
            temp = s[i].split('(')
            l = len(temp)
            k += l - 1
            temp[1] = '(' + temp[1]
            s[i] = temp[0]
            s.insert(i + 1, temp[1])
            i += l - 1
        i += 1

    i = 0
    k = len(s)
    while i < k:
        if '!' in s[i]:
            temp = s[i].split('!')
            l = len(temp)
            k += l - 1
            s[i] = temp[0] + '!'
            for j in range(1, l):
                if len(temp[j]) > 0:
                    temp[j] = temp[j].capitalize()
                s.insert(i + 1, temp[j])
                if j == l - 1:
                    pass
                else:
                    s[i + j] += '!'

            i += l - 1
        i += 1

    i = 0
    k = len(s)
    while i < k:
        if '?' in s[i]:
            temp = s[i].split('?')
            l = len(temp)
            k += l - 1
            s[i] = temp[0] + '?'
            for j in range(1, l):
                if len(temp[j]) > 0:
                    temp[j] = temp[j].capitalize()
                s.insert(i + 1, temp[j])
                if j == l - 1:
                    pass
                else:
                    s[i + j] += '?'

            i += l - 1
        i += 1

    s = ' '.join(s)
    writefile(f, s)
    log(f, 'punctuator')


def history():
    tval2 = True
    while tval2:
        s = input(print('''Choose Action (a, b, c) -
    a) View History
    b) Delete History (note: this will be logged)
    c) Back to Main Menu'''))
        if s == 'a':
            with open('logs.csv', 'r') as logs:
                reader = csv.reader(logs)
                for row in reader:
                    if row[0] == 'date':
                        print(row[0] + '\t', row[1] + '\t', row[2], row[3], sep='\t')
                    else:
                        print('\t'.join(row))
        if s == 'b':
            with open('logs.csv', 'w') as logs:
                writer = csv.writer(logs)
                writer.writerow(['date', 'time', 'filename', 'action'])
            log('logs.csv', 'history deleted')
        if s == 'c':
            tval2 = False
        else:
            print('Please enter valid input (a, b, c)')


# menu
tval = True

while tval:
    n = int(input('''What do you want to do? (1, 2, 3. . .)
1) File Compression
2) File Decompression
3) Shorthand Text Notation
4) Abbreviation Replacement
5) Text Analytics
6) Replace word
7) Punctuator
8) View History
9) Quit
'''))

    if n == 1:
        file = getfile()
        content = read(file)
        lf, l = create_char_and_frequency_list(content)
        tree, lf = build_base_level(lf)
        tree = build_tree(lf)
        b = get_binary(tree, l)
        newc = build_new_file(content, b)
        make_compressed_file(file, newc, b)
    elif n == 2:
        decompress()
    elif n == 3:
        shorthand()
    elif n == 4:
        shortform()
    elif n == 5:
        analytics()
    elif n == 6:
        replacer()
    elif n == 7:
        punctuator()
    elif n == 8:
        history()
    elif n == 9:
        print('exiting. . .')
        break
    else:
        print('Please input valid value (1, 2, 3. . .)')

'''  
#run test
file=getfile()
content=read(file)
lf,l=create_char_and_frequency_list(content)
tree,lf=build_base_level(lf)
tree=build_tree(lf)
b=get_binary(tree,l)
newc=build_new_file(content, b)
make_compressed_file(file,newc,b)
decompress()
'''