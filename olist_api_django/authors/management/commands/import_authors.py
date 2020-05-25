from django.core.management.base import BaseCommand, CommandError
from authors.models import Author
import os.path

class Command(BaseCommand):
    help = 'import authors from csv file'

    def add_arguments(self, parser):
        parser.add_argument('authors', nargs='+', type=str)

    def handle(self, *args, **options):
        if options['authors'][0]:
            fpath = options['authors'][0]            
            if not os.path.exists(fpath):
                raise CommandError("file doesn't exist")
            with open(fpath, 'r') as fp:
                line = fp.readline()
                if line.strip()=="name":
                    line = fp.readline()
                else:
                    raise CommandError("Wrong format file")
                cont = 0
                contp = 0
                authors_list = []
                self.stdout.write("Import started. This can take a while...")
                # Read every line in the file and bulk create on every 10000 registers        
                while line:                    
                    author = Author(name=line.strip())
                    authors_list.append(author)                    
                    cont+=1
                    contp+=1
                    if contp == 10000:
                        contp= 0
                        Author.objects.bulk_create(authors_list)
                        authors_list = []
                        self.stdout.write("Imported "+str(cont)+" authors. Still running....")
                    line = fp.readline()
                if authors_list:
                    Author.objects.bulk_create(authors_list)
                self.stdout.write("Imported "+str(cont)+" authors from "+str(fpath))
                
        else:
            self.stdout.write("Fail")        