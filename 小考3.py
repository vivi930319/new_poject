def input_dic(children):
    for_in range(5):
        name=input("Enter the children's name: ")
        age=input("Enter the children's age: ")
        children[name]=age

def print_dic(children):
    for name,age in children.items():
        print(f"Name: {name},Age: {age}")

def if_John(children):
    if 'John' in children:
        print('yes')
    else:
        print('no')

def main():
    children={}
    input_dic(children)
    print_dic(children)
    if_John(children)

main()
