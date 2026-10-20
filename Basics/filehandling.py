
# file handling - creating , reading , updating & deleting files


file = open("create.txt","a")

file.write("hello\n")

file.write("working")

content = file.read()
print(content)

file.close()
