#HUFFMAN COMPRESSION

#binary to integer functions
def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return(decimal)

def DecimalToBinary(num):
    return bin(num).replace('0b',"")

#accepting the string
print('this program compresses text!')
stri=input('please enter a string \n')
print(f"the string you entered is \n {stri}")
print(f'your data is {len(stri)*8} bits long')

#making a list, finding the frequency
letters,letterlol=[],[]
for letter in stri:
    if letter not in letterlol:
        letters.append(stri.count(letter))
        letters.append(letter)
        letterlol.append(letter)

# making the tree
nodes=[]
while len(letters)>0:
    nodes.append(letters[0:2])
    letters=letters[2:]
nodes.sort()
tree=[]
tree.append(nodes)
#base created
def build(nodes):
    newnode=[]
    if len(nodes)>1:
        nodes.sort()

        nodes[0].append('0')
        nodes[1].append('1')
        combinednode1=(nodes[0][0]+nodes[1][0])
        combinednodes2=(nodes[0][1]+nodes[1][1])
        newnode.append(combinednode1)
        newnode.append(combinednodes2)
        newnodes=[]
        newnodes.append(newnode)
        newnodes=newnodes+nodes[2:]
        nodes=newnodes
        tree.append(nodes)
        build(nodes)
    return tree
newnodes=build(nodes)
#invert the tree for visualisation
tree.sort(reverse=True)
print('this is the tree')

check=[]
for lvl in tree:
    for node in lvl:
        if node in check:
            lvl.remove(node)
        else:
            check.append(node)
count=0
for lvl in tree:
    print(f'level: {count} \t {lvl}')
    count+=1
print()

#build a binary code for each letter and completes code is there is only one dude
letterb=[]
if len(letterlol)==1:
    letter_code=[letterlol[0],'0']
    letterb.append(letter_code*len(stri))
else:
    for letter in letterlol:
        lettercode=''
        for n in check:
            if len(n)>2 and letter in n[1]:
                lettercode+=n[2]
        letter_code=[letter,lettercode]
        letterb.append(letter_code)
#output
print('the binary codes are as follows')
for letter in letterb:
    print(letter[0],letter[1])

#creating the real bitstring
bit=''
for char in stri:
    for i in letterb:
        if char in i:
            bit+=i[1]

#obtaining the integer called binary(because i messed up initially)
'''binary=bin(int(bit))
print(bit)'''
binary=binaryToDecimal(int(bit))
#print(binary)
a= str(binary)
#print(a)

#summary
print(f'''the original file length is-
{len(stri)*8} bits''')
print(f'''and the final length is-
{len(a)*4} bits''')
print(f'the compression ratio is \n {(len(stri)*2)/len(a)}')
print(f'your binary message is \n {binary}')

#decompression
bitstring=DecimalToBinary(binary)
uncompressed_string=''
code=''
for digit in bitstring:
    code+=digit
    pos=0
    for letter in letterb:
        if code==letter[1]:
            uncompressed_string+=letterb[pos][0]
            code=''
        pos+=1
print(f'uncompressed data is: \n{uncompressed_string}')
''''''






































