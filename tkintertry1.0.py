'''
Grade 12 CS Project
17-01-2021
'''

from tkinter import *
import time
import csv
import pickle

#-------------------------------Global_Functions-------------------------------#

def destroyer():
    widget_list = all_children(root)
    for item in widget_list:
        item.destroy()
    
    menubar = Menu(root)

    #Misc.
    misc = Menu(menubar, tearoff = 0)
    misc.add_command(label="Home", command = HomePage)
    misc.add_command(label = "How to Use", command = instructions) 
    misc.add_command(label = "Read A File", command = readfile)
    misc.add_command(label = 'Analytics', command = analytics)
    misc.add_command(label="Quit", command=root.quit)


    menubar.add_cascade(label = "Project", menu = misc)

    #Compression
    compression = Menu(menubar, tearoff = 0)
    compression.add_command(label="compress", command = compressfunct)
    compression.add_command(label = "decompress", command = decompressfunct) 

    menubar.add_cascade(label = "Compression", menu = compression)

    #>>text manipulation
    textmenu = Menu(menubar, tearoff=0)
    textmenu.add_command(label = "Punctuator", command = punctfunct)
    textmenu.add_separator()
    textmenu.add_command(label = "Shorthand", command = shorthand)
    textmenu.add_command(label = "Word Replace", command = replacer)

    menubar.add_cascade(label = "Text Manipulation", menu = textmenu)

    #>>History
    history = Menu(menubar, tearoff=0)
    history.add_command(label = "View Logs", command = logviewer) 
    history.add_command(label = "Delete Logs", command = logdeleter) 


    menubar.add_cascade(label = "History", menu = history)


    root.config(menu = menubar)



def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def log(filename, action):
    result = time.localtime()
    a=str(result.tm_mday)
    b=str(result.tm_mon)
    c=str(result.tm_year)
    d=str(result.tm_hour)
    e=str(result.tm_min)
    f=str(result.tm_sec)
    L=[a,b,c,d,e,f]
    for i in range(len(L)):
        if int(L[i])<10:
            L[i]='0'+L[i]
    date = L[0]+ '-' + L[1] + '-' + L[2]
    tyme = L[3] + ':' + L[4] + ':' + L[5]
    try:
        with open('logs.csv', 'a') as logs:
            writer = csv.writer(logs)
            writer.writerow([date, tyme, filename, action])
    except:
        with open('logs.csv', 'w') as logs:
            writer = csv.writer(logs)
            writer.writerow(['Date', 'Time', 'Filename', 'Action'])
        with open('logs.csv', 'a') as logs:
            writer = csv.writer(logs)
            writer.writerow([date, tyme, filename, action])
        

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def read(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        lab = Label(root, text = 'File does not exist')
        lab.pack()
        return False
   
def writefile(filename, s):
    ft = open(filename, 'w')
    ft.write(s)
    ft.close()

def filecheck():
    s = []
    filelist = []
    with open('logs.csv', 'r') as logs:
        reader = csv.reader(logs)
        for row in reader:
            s.append(row)
    for i in s:
        temp = i[2].split('.')
        if 'txt' in temp:
            filelist.append(i[2])
            break
    if len(filelist) !=0:
        return True
    else:
        return False
   
def uselast():
    st = []
    filelist = []
    with open('logs.csv', 'r') as logs:
        reader = csv.reader(logs)
        for row in reader:
            st.append(row)
    for i in st:
        temp = i[2].split('.')
        if 'txt' in temp:
            filelist.append(i[2])
    g = Label(root, text = 'file in use: ' + filelist[len(filelist)-1]).pack()
    return filelist[len(filelist)-1]


#------------------------------Compression_Functions------------------------------#

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


    
def make_compressed_file(file, c_content, b_key):
    name = file.split('.')
    name = name[0]
    name1 = name + '_compressed.dat'
    name2 = name + '_key.dat'
    #################################?????????????????!!!!!!!!!!!!!!!!?!?!?!?!?!?!?!?!?!?!?!?!?ISHAAAAAANNNNN LOOK HERE
    #new_size= len(c_content)
    #print('there are now '+new_size+' bits in the compressed file')
    content = int(c_content, 2)
    f = open(name1, 'wb')
    pickle.dump(content, f)
    f.close()
    fl = open(name2, 'wb')
    pickle.dump(b_key, fl)
    fl.close()
    #print('compressed files created')

    
#--------------------------------Menu_Functions--------------------------------#


def compressfunct():
   destroyer()
   lab = Label(root, text = 'File Compression - Huffman Encoding\nadd more info')
   lab.pack()
   e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e.pack()
   e.insert(0,"filename.txt")
   overrider = False
   def clicker():
      
      global tree
      if overrider ==False:
          file = e.get()
      else:
          file = uselast() 
      
      content = read(file)
      if content != False:
          lf, l = create_char_and_frequency_list(content)
          tree, lf = build_base_level(lf)
          tree = build_tree(lf)
          b = get_binary(tree, l)
          newc = build_new_file(content, b)
          make_compressed_file(file, newc, b)
          log(file, 'compression')
          t = 'compressed files created\n Original file size: '# + str(orglen) +' bytes\nFinal file sixe: ' + str(finlen) + ' bytes'
          l1 =Label(root, text=t)
          l1.pack()
   def clicker1():
        nonlocal overrider
        overrider = False
        clicker()
   def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
   button = Button(root, text = 'Enter filename', command = clicker1)
   button.pack()
   if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()
   
   
def decompressfunct():
   destroyer()
   lab = Label(root, text = 'File Decompression - Huffman Encoding\nadd more info')
   lab.pack()
   e1 = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e1.pack()
   e1.insert(0,"filename_compressed.dat")
   e2 = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e2.pack()
   e2.insert(0,"filename_key.dat")
   
   def clicker():
      name1 = e1.get()
      name2 = e2.get()
      try:
         f = open(name1, 'rb')
         content_ = pickle.load(f)
         f.close()
      except:
         g = Label(root, text = 'unexpected error, please ensure file exists').pack()
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
      log(name1, 'decompression')
      try:
         f = open(name, 'w')
         f.write(new_content)
         f.close()
      except:
          print('error, unable to write data in file')
      t = 'decompressed file created'#\n Original file size: '# + str(orglen) +' bytes\nFinal file sixe: ' + str(finlen) + ' bytes'
      l1 =Label(root, text=t)
      l1.pack()

   button = Button(root, text = 'Submit', command = clicker)
   button.pack()
   

           
   
def shorthand():
   destroyer()
   lab = Label(root, text = 'Shorthand Text Converter\nadd more info')
   lab.pack()

   e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e.pack()
   e.insert(0,"filename.txt")
   overrider = False
   def clicker():
      print(overrider)
      if overrider ==False:
          f = e.get()
      else:
          f = uselast()
      s = read(f)
      if s != False:
          orglen = len(s)
          s = s.split()
          length = len(s)
          i = 0
          while i < length:

             if s[i] == 'the' or s[i] == 'a' or s[i] == 'an':
                length -= 1
                del s[i]
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
          D = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                'eight': '8', 'nine': '9'}
          for i in range(len(s)):
             if s[i] in D.keys():
                s[i] = D[s[i]]

          s = ' '.join(s)
          finlen = len(s)
          writefile(f, s)
          log(f, 'shorthand')
          t = 'Replacements have been made\n Original file size: ' + str(orglen) +' bytes\nFinal file sixe: ' + str(finlen) + ' bytes'
          l1 =Label(root, text=t)
          l1.pack()
   def clicker1():
        nonlocal overrider
        overrider = False
        clicker()
   def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
   button = Button(root, text = 'Enter filename', command = clicker1)
   button.pack()
   if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()

def replacer():
   destroyer()
   
   lab = Label(root, text = 'Text Replacement')
   lab.pack()
   
   e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e.pack()
   e.insert(0,"filename.txt")
   
   def clicker():
      if overrider ==False:
          f = e.get()
      else:
          f = uselast() 
      s = read(f)
      #print(s)
      if s!= False:
          s = s.split()
          key = ''
          val = ''
          
          tb1 = Entry(root, width = 30, bg = 'orange', fg = 'white')
          tb1.pack()
          tb1.insert(0, 'enter unique word')
          tb2 = Entry(root, width = 30, bg = 'orange', fg = 'white')
          tb2.pack()
          tb2.insert(0, 'enter replacement')

          def keyvalget():
             global key, val
             
             if overrider ==False:
                  f = e.get()
             else:
                 f = uselast() 
             s = read(f)
             print(s)
             orglen = len(s)
             s = s.split()
             key = tb1.get()
             val = tb2.get()
             for j in range(len(s)):
                if s[j] == key:
                    s[j] = val

             s = ' '.join(s)
             finlen = len(s)
             writefile(f, s)
             log(f, 'replacer')
             t = 'Replacements have been made\n Original file size: ' + str(orglen) +' bytes\nFinal file sixe: ' + str(finlen) + ' bytes'
             l1 =Label(root, text=t)
             l1.pack()
          submitbut=Button(root, text = 'Submit', command = keyvalget)
          submitbut.pack()
   def clicker1():
        nonlocal overrider
        overrider = False
        clicker()  
   button = Button(root, text = 'Enter filename', command = clicker1)
   button.pack()
   overrider = False
   def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
   
   if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()

def punctfunct():
   destroyer()
   
   lab = Label(root, text = 'Punctuator\n add info\nNote: This function does not \
reduce file size. It is for basic grammar correction')
   lab.pack()
   
   e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
   e.pack()
   e.insert(0,"filename.txt")
   overrider = False
   def clicker():
       if overrider ==False:
          f = e.get()
       else:
          f = uselast()  
       s = read(f)
       if s!= False:
           orglen = len(s)
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
           finlen = len(s)
           writefile(f, s)
           log(f, 'punctuator')
           t = 'Replacements have been made\n Original file size: ' + str(orglen) +' bytes\nFinal file sixe: ' + str(finlen) + ' bytes'
           l1 =Label(root, text=t)
           l1.pack()
   def clicker1():
        nonlocal overrider
        overrider = False
        clicker()
   button = Button(root, text = 'Enter filename', command = clicker1)
   button.pack()
   def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
   
   if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()
    
def instructions():
    destroyer()
    lab = Label(root, text = '''Instructions\nadd info''')
    lab.pack()

def logviewer():
    destroyer()
    s = []
    with open('logs.csv', 'r') as logs:
        reader = csv.reader(logs)
        for row in reader:
            s.append(row)
  
    class Table: 
        def __init__(self,root): 
            for i in range(total_rows): 
                for j in range(total_columns): 
                      
                    self.e = Entry(root, width=17) 
                      
                    self.e.grid(row=i, column=j) 
                    
                    self.e.insert(END, s[i][j])
                   
                    
                    
    total_rows = len(s) 
    total_columns = len(s[0])
    t = Table(root) 

def logdeleter():
    destroyer()
       
    lab = Label(root, text = 'Please confirm that you want the file manipulation history to be deleted.')
    lab.pack()

    def clicker():
        try:
            with open('logs.csv', 'w') as logs:
                    writer = csv.writer(logs)
                    writer.writerow(['Date', 'Time', 'Filename', 'Action'])
            log('logs.csv', 'history deleted')
        
            l = Label(root, text = 'Deletion Successful')
            l.pack()
        except:
            l = Label(root, text = 'Deletion Unsuccessful')
            l.pack()
    
    submitbut=Button(root, text = 'Confirm', command = clicker)
    submitbut.pack()

def HomePage():
    destroyer()
    lab1 = Label(root, text = 'Grade 12 CS Project - Text Compressor and Editor')
    lab1.pack()
  
def readfile():
    destroyer()

    lab = Label(root, text = 'Read a File')
    lab.pack()
    e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
    e.pack()
    e.insert(0,"filename.txt")
    overrider = False
    def clicker():
        
        if overrider ==False:
          f = e.get()
        else:
          f = uselast() 
        s = read(f)
        if s!= False:
            filewin = Toplevel(root)

            canvas = Canvas(filewin, width=600, height=400)
            scroll_y = Scrollbar(filewin, orient="vertical", command=canvas.yview)

            frame = Frame(canvas)

            Label(frame, text = s, wraplength = 600).pack()
            canvas.create_window(0, 0, anchor='nw', window=frame)
            # make sure everything is displayed before configuring the scrollregion
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
                             
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
    
    def clicker1():
        nonlocal overrider
        overrider = False
        clicker()
    def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
    button = Button(root, text = 'Enter filename', command = clicker1)
    button.pack()
    if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()

def analytics():
    destroyer()

    lab = Label(root, text = 'Text Analytics')
    lab.pack()
    e = Entry(root, width = 30, bg = 'orange', fg = 'white', borderwidth = 2)
    e.pack()
    e.insert(0,"filename.txt")
    overrider = False
    def clicker1():
        nonlocal overrider
        overrider = False
        clicker()
    def clicker2():
       nonlocal overrider
       overrider = True
       clicker()
    
    def clicker():
        if overrider ==False:
          f = e.get()
        else:
          f = uselast()  
        s = read(f)
        if s!= False:
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
                else:# s[i] not in ['the', 'of', 'and', 'a', 'an', 'to', 'was', 'that', 'it', 'in', 'had', 'which', 'his', 'I', 'by', 'as', 'The', 'not', 'but', 'were', 'be', 'have', 'all','he', 'with', 'from', 'for', 'to', 'at', 'on', 'of', 'or','when']:
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
            al = 'Analytics\n'
            al +='Word count: '+ str(wordcount)
            al +='\nNo. of characters: '+ str(charcount)
            al +='\nNo. of sentences: '+ str(sentcount)
            al +='\nMost common words: \n'
            for word, count in mostcommon.items():
                al+='\t'+ word+ ' : '+ str(count) +'\n'

            alab = Label(root, text = al, justify = LEFT).pack()
            log(f, 'analytics')
            
            
    button = Button(root, text = 'Enter filename', command = clicker1)
    button.pack()
    if filecheck():
           button2 = Button(root, text = 'Use Previous', command = clicker2)
           button2.pack()
    
#------------------------------Main_Window_Elements------------------------------#


root = Tk()
root.geometry('700x400')
lab1 = Label(root, text = 'Grade 12 CS Project - Text Compressor and Editor')
lab1.pack()
menubar = Menu(root)

#Misc.
misc = Menu(menubar, tearoff = 0)
misc.add_command(label="Home", command = HomePage)
misc.add_command(label = "How to Use", command = instructions) 
misc.add_command(label = "Read A File", command = readfile)
misc.add_command(label = 'Analytics', command = analytics)
misc.add_command(label="Quit", command=root.quit)


menubar.add_cascade(label = "Project", menu = misc)

#Compression
compression = Menu(menubar, tearoff = 0)
compression.add_command(label="compress", command = compressfunct)
compression.add_command(label = "decompress", command = decompressfunct) 

menubar.add_cascade(label = "Compression", menu = compression)

#>>text manipulation
textmenu = Menu(menubar, tearoff=0)
textmenu.add_command(label = "Punctuator", command = punctfunct)
textmenu.add_separator()
textmenu.add_command(label = "Shorthand", command = shorthand)
textmenu.add_command(label = "Word Replace", command = replacer)

menubar.add_cascade(label = "Text Manipulation", menu = textmenu)

#>>History
history = Menu(menubar, tearoff=0)
history.add_command(label = "View Logs", command = logviewer) 
history.add_command(label = "Delete Logs", command = logdeleter) 


menubar.add_cascade(label = "History", menu = history)


root.config(menu = menubar)

#-------------------------------------------------------------------------------#
