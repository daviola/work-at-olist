
# module to write the sample authors
def write_authors(qty_times_5, filename):
    my_file= open(filename, 'w')
    names = ["Osvaldo Santana Neto","David Beazley","Chetan Giridhar","Brian K. Jones","J.K Rowling"]
    cont = 0
    to_write = 'name\n'
    while cont < qty_times_5:
        for name in names:
            to_write +=name+"\n"
        cont +=1
    my_file.write(to_write)
