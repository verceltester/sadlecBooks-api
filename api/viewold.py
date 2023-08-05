from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView


def chap(bookid, chapid):
    ch = Chapter.objects.filter(Books__id=bookid).values("id")
    mylist3 = []
    for x in ch:
        mylist3.append(x.get('id'))
    print(mylist3)
    pos_of_current_chap = mylist3.index(chapid)
    pos_last_id_in_chap_list =  mylist3.index(mylist3[-1])
    difference =  pos_last_id_in_chap_list - pos_of_current_chap
    if difference != 0:
        valueofnextchapid = mylist3[pos_of_current_chap+1]
        print("nestid: ", valueofnextchapid)
        url = str(bookid) + "/" + str(valueofnextchapid)
        return url
    else:
        url = "end of book"
        return url
    





@api_view(['GET'])
def book(request):
    books = Books.objects.all()
    myserializer = BooklistSerializer(books, many=True, context={'request': request})
    return Response(myserializer.data)

# class book(ListAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BooklistSerializer


@api_view(['GET'])
def booktoc(request, bookid):
    books = Books.objects.get(id=bookid)
    myserializer = BookSerializer(books, context={'request': request})
    return Response(myserializer.data)


@api_view(['GET'])
def ChapterText(request, bookid, chapid):
    # books = Books.objects.get(id=bookid)
    mychapter = Chapter.objects.get(id=chapid)

    
    nextsub1 = Subhead1.objects.filter(Chapter__id=chapid)
    print(nextsub1)
    if nextsub1.exists():
        nextid = nextsub1.values('id').first().get('id')
                         
        print(nextid)        
        url = str(bookid) + "/" + str(chapid) + "/" + str(nextid) 
        print(url)
    else:
        chap(bookid, chapid) 



    myserializer = ChapterTextSerializer(
                        mychapter, context={
                         'request': request,
                         "nexturl": url,})
    return Response(myserializer.data)


@api_view(['GET'])
def Subhead1Text(request, bookid, chapid, sub1id):
    bookname = Books.objects.get(id=bookid).bookTitle
    # mychapter = Chapter.objects.get(id=chapid)
    mysub1 = Subhead1.objects.get(id=sub1id)


    nextsub2 = Subhead2.objects.filter(Subhead1__id=sub1id)
   
    if nextsub2.exists():
        nextid = nextsub2.values('id').first().get('id')        
        url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(nextid)
        print(url)
    else:
        s1 = Subhead1.objects.filter(Chapter__id=chapid).values("id")        
        mylist2 = []
        for x in s1:
            mylist2.append(x.get('id'))
        print(mylist2)
        pos_of_current_sub1 = mylist2.index(sub1id)
        pos_last_id_in_sub1_list =  mylist2.index(mylist2[-1])
        difference =  pos_last_id_in_sub1_list - pos_of_current_sub1
        
        if difference != 0:
            valueofnexts1id = mylist2[pos_of_current_sub1+1]
            print("nestid: ", valueofnexts1id)
            url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)
        else:
            chap(bookid, chapid)
  
    myserializer = Subhead1TextSerializer(
        mysub1, context={"currentbook": bookname, 
                         'request': request,
                         "nexturl": url,})
    
    return Response(myserializer.data)





@api_view(['GET'])
def Subhead2Text(request, bookid, chapid, sub1id, sub2id):
    bookname = Books.objects.get(id=bookid).bookTitle
    mychapter = Chapter.objects.get(id=chapid).chapTitle
    # mysub1 = Subhead1.objects.get(id=sub1id)
    mysub2 = Subhead2.objects.get(id=sub2id)

    p = Subhead2.objects.filter(Subhead1__id=sub1id).values("id")
    
    no_of_ids = p.filter().values("id")    
    mylist = []

    for x in no_of_ids:
        mylist.append(x.get('id'))

    print(sub2id)
    print(mylist)  

    pos_of_current_sub2 = mylist.index(sub2id)
    pos_last_id_in_list =  mylist.index(mylist[-1])
    print('position of current id: ', pos_of_current_sub2)
    print('position of last id: ', pos_last_id_in_list)
    difference = pos_last_id_in_list-pos_of_current_sub2
    print("differene is: ", difference)

    if difference != 0:
        valueofnextid = mylist[pos_of_current_sub2+1]
        print("nestid: ", valueofnextid)
        url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(valueofnextid)
    
    elif difference==0:
        s1 = Subhead1.objects.filter(Chapter__id=chapid).values("id")        
        mylist2 = []
        for x in s1:
            mylist2.append(x.get('id'))
        print(mylist2)
        pos_of_current_sub1 = mylist2.index(sub1id)
        pos_last_id_in_sub1_list =  mylist2.index(mylist2[-1])
        difference =  pos_last_id_in_sub1_list - pos_of_current_sub1
        
        if difference != 0:
            valueofnexts1id = mylist2[pos_of_current_sub1+1]
            print("nestid: ", valueofnexts1id)
            url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)
        else:
            # url = "next Chapter starting here:url coming soon" 
            chap(bookid, chapid) 
   
    myserializer = Subhead2TextSerializer(mysub2, context={"currentbook": bookname,
                                                           'request': request,
                                                           "currentchapter": mychapter,
                                                           "nexturl": url,
                                                           })
    return Response(myserializer.data)




