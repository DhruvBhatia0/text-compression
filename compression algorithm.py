#HUFFMAN COMPRESSION
#accepting the string
print('this program compresses text!')
str=input('please enter a string \n')
print(f"the string you entered is \n {str}")
print(f'your data is {len(str)*8} bits long')

#making a list, finding the frequency
letters,letterlol=[],[]
for letter in str:
    if letter not in letterlol:
        letters.append(str.count(letter))
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
    letterb.append(letter_code*len(str))
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
for char in str:
    for i in letterb:
        if char in i:
            bit+=i[1]
#obtaining the binary digit
binary=bin(int(bit))
print(bit)

#summary
print(f'''the original file length is-
{len(str)*8} bits''')
print(f'''and the final length is-
{len(binary)} bits''')
print(f'the compression ratio is \n {(len(str)*8)/len(binary)}')
print(f'your binary message is \n {binary}')

#decompression
bitstring=bit
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






































