import pickle
def getfile():
    file=input('please enter the name of the text file as <name>.txt\nensure the file is in the same folder as the code\n')
    return file
def read(file):
    f=open(file, 'r')
    content=f.read()
    return content
def sort(letter_f):
    for i in range(len(letter_f)):
        for j in range(len(letter_f)-1):
            if letter_f[j][1]>letter_f[j+1][1]:
                letter_f[j],letter_f[j+1]=letter_f[j+1],letter_f[j]
def create_char_and_frequency_list(content):
    letters=[]
    letters_f=[]
    for letter in content:
        if letter not in letters:
            letters.append(letter)
            letters_f.append([letter,1])
        else:
            for i in range(len(letters_f)):
                if letters_f[i][0]==letter:
                    letters_f[i][1]+=1
                    break
    return letters_f,letters
def build_base_level(letter_f):
    sort(letter_f)
    tree=[]
    tree.append(letter_f)
    return tree,letter_f

def build_tree(letter_f):
    new_lvl=[]
    if len(letter_f)>1:
        sort(letter_f)
        letter_f[0].append('0')
        letter_f[1].append('1')
        combined_char=letter_f[0][0]+letter_f[1][0]
        combined_freq=letter_f[0][1]+letter_f[1][1]
        new_lvl.append([combined_char,combined_freq])
        new_lvl=new_lvl+letter_f[2:]
        letter_f=new_lvl
        tree.append(letter_f)
        build_tree(letter_f)
    return tree

def get_binary(tree, letters):
    binary_code=[]
    for i in letters:
        code=''
        repeat=''
        for j in range(len(tree)-2,-1,-1):
            for k in range(len(tree[j])):
                if i in tree[j][k][0] and tree[j][k][0]!=repeat:
                    repeat=tree[j][k][0]
                    code+=tree[j][k][2]
        binary_code.append([i,code])
    return binary_code

def build_new_file(content,binary_code):
    content=list(content)
    for i in range(len(binary_code)):
        for j in range(len(binary_code)-2):
            if binary_code[j][1]<binary_code[j+1][1]:
                binary_code[j],binary_code[j+1]=binary_code[j+1],binary_code[j]
    new_content=''
    for i in content:
        for j in binary_code:
            if i==j[0]:
                new_content=new_content+j[1]
                break
    return new_content

def decompress():
    name1=input('please enter the complete name of the file containing the content that was compressed\n')
    name2=input('please enter the complete name of the file containing the binary key\n')
    f=open(name1,'rb')
    content_=pickle.load(f)
    f.close()
    f=open(name2,'rb')
    binary_code=pickle.load(f)
    f.close()
    #reobtaining the 1s and 0s as a string
    content="{0:b}".format(content_)
    content=str(content)
    temp = ''
    new_content = ''
    for i in content:
        temp = temp + i
        for j in binary_code:
            if j[1] == temp:
                temp = ''
                new_content += j[0]
                break
    name=name1[:3]+'_decompressed.txt'
    f=open(name,'w')
    f.write(new_content)


def make_compressed_file(file,c_content,b_key):
    name=file.split('.')
    name=name[0]
    name1=name+'_compressed.dat'
    name2=name+'_key.dat'
    content=int(c_content,2)
    f=open(name1,'wb')
    pickle.dump(content,f)
    f.close()
    fl=open(name2,'wb')
    pickle.dump(b_key,fl)
    fl.close()
    print('compressed files created')


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


































