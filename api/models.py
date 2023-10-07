from django.db import models

#NOTE: if name changes, changes to be made everywhre like admin.py, views.py, serialiers.py 
# to reset id gerneration in postgress sql command ===    SELECT setval('api_books_id_seq', (SELECT MAX(id) FROM api_books)+1);

class Books(models.Model):
    bookTitle = models.CharField(max_length=200, null=True, blank=True)
    bookAuthor = models.CharField(max_length=200, null=True, blank=True)
    bookPrice = models.FloatField(null=True, blank=True)
    image = models.ImageField(default='defaultt.jpg', upload_to='book_pics')
    imagelink = models.CharField(max_length = 300, null=True, blank=True)
    aurokart = models.CharField(max_length = 300, null=True, blank=True)
    otherinfo = models.TextField(max_length=150000, null=True, blank=True)
    searchableFields = ["bookTitle"]
   
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.bookTitle


class Chapter(models.Model):
    chapTitle = models.CharField(max_length=200, null=True, blank=True )
    chapText = models.TextField(max_length=250000, null=True, blank=True)
    Books = models.ForeignKey(Books, related_name='chap', on_delete=models.CASCADE)
    hastext = models.BooleanField(default=True)
    FilterFields = ["Books", "hastext"]
    searchableFields = ["chapTitle"]

    class Meta:
        ordering = ['id']
   

    def __str__(self):
        return self.chapTitle


class Subhead1(models.Model):
    subhead1Titles = models.CharField(max_length=500, null=True, blank=True)
    subhead1Text = models.TextField(max_length=250000, null=True, blank=True)
    Chapter = models.ForeignKey(Chapter, related_name='sub1', on_delete=models.CASCADE)
    hastext = models.BooleanField(default=True)
    searchableFields = ["subhead1Titles"]
    FilterFields = ["hastext"]
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.subhead1Titles


class Subhead2(models.Model):
    subhead2Titles = models.CharField(max_length=500, null=True, blank=True)
    subhead2Text = models.TextField(max_length=250000, null=True, blank=True)
    Subhead1 = models.ForeignKey(Subhead1, related_name='sub2',on_delete=models.CASCADE)
    hastext = models.BooleanField(default=True)
    searchableFields = ["subhead2Titles"]
    FilterFields = ["hastext"]

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.subhead2Titles



class indexword(models.Model):    
    
    alphaTitle  = models.CharField(max_length=1, blank=True)
    word = models.CharField(max_length=100, null=True, blank=True)
    bookID = models.ForeignKey(Books, on_delete=models.CASCADE)
    searchableFields = ["word"]
    FilterFields = ["bookID"]

    def __str__(self):
        return self.word
    

class indexUrl(models.Model):
    word = models.ForeignKey(indexword, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, null=True, blank=True)
    urltext = models.CharField(max_length=100, null=True, blank=True)    
    searchableFields = ["url"]
    
    def __str__(self):
        return  self.url