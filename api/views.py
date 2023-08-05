from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status



@api_view(['GET'])
def book(request):
    books = Books.objects.all()
    myserializer = BooklistSerializer(
        books, many=True, context={'request': request})
    return Response(myserializer.data)


@api_view(['GET'])
def home(request):    
    return Response("You are on home page, design as per your appetite. If you need some content from database, will send that")

# @api_view(['GET'])
# def home(request):    
#     return render(request, 'api/index.html')

@api_view(['GET'])
def booktoc(request, bookid):
    books = Books.objects.get(id=bookid)
    # books = Books.objects.prefetch_related('chap').get(id=bookid)
    myserializer = BookSerializer(books, context={'request': request})
    return Response(myserializer.data)

@api_view(['GET'])
def bookdetails(request, bookid):
    books = Books.objects.get(id=bookid)
    myserializer = BookdetailSerializer(books, context={'request': request})
    return Response(myserializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @decorators.permission_classes([permissions.IsAuthenticated])
def ChapterText(request, bookid, chapid):
    bookname = Books.objects.get(id=bookid).bookTitle
    mychapter = Chapter.objects.get(id=chapid)


    ch = Chapter.objects.filter(Books__id=bookid).values("id")
    mylist3 = []
    for x in ch:
        mylist3.append(x.get('id'))
    pos_of_current_chap = mylist3.index(chapid)
    pos_last_id_in_chap_list = mylist3.index(mylist3[-1])
    difference = pos_last_id_in_chap_list - pos_of_current_chap
    pos_first_id_in_chap_list = mylist3.index(mylist3[0])
    pre_difference1 = pos_of_current_chap - pos_first_id_in_chap_list



    nextsub1 = Subhead1.objects.filter(Chapter__id=chapid)    
    if nextsub1.exists():
        nextid = nextsub1.values('id').first().get('id')        
        url = str(bookid) + "/" + str(chapid) + "/" + str(nextid)

    else:        
        if difference != 0:
            valueofnextchapid = mylist3[pos_of_current_chap+1]
            url = str(bookid) + "/" + str(valueofnextchapid)
        else:
            url = None


    if pre_difference1 != 0:
        valueofnextchapid = mylist3[pos_of_current_chap-1]
        pre_url = str(bookid) + "/" + str(valueofnextchapid)
    else:
        pre_url = None


    myserializer = ChapterTextSerializer(
        mychapter, context={"currentBook": bookname,
            'request': request,
            "nextUrl": url, 
            "previousUrl": pre_url,             
            })
   

    return Response(myserializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def Subhead1Text(request, bookid, chapid, sub1id):
    bookname = Books.objects.get(id=bookid).bookTitle
    # mychapter = Chapter.objects.get(id=chapid)
    mysub1 = Subhead1.objects.get(id=sub1id)


    s1 = Subhead1.objects.filter(Chapter__id=chapid).values("id")
    mylist2 = []
    for x in s1:
        mylist2.append(x.get('id'))
    try:
        pos_of_current_sub1 = mylist2.index(sub1id)
        pos_last_id_in_sub1_list = mylist2.index(mylist2[-1])
        difference1 = pos_last_id_in_sub1_list - pos_of_current_sub1
        pos_first_id_in_sub1_list = mylist2.index(mylist2[0])
        pre_difference1 = pos_of_current_sub1 - pos_first_id_in_sub1_list
    except:
        print("something went wrong")

    ch = Chapter.objects.filter(Books__id=bookid).values("id")
    mylist3 = []
    for x in ch:
        mylist3.append(x.get('id'))

    try:
        pos_of_current_chap = mylist3.index(chapid)
        pos_last_id_in_chap_list = mylist3.index(mylist3[-1])
        difference2 = pos_last_id_in_chap_list - pos_of_current_chap
    


        nextsub2 = Subhead2.objects.filter(Subhead1__id=sub1id)
        if nextsub2.exists():
            nextid = nextsub2.values('id').first().get('id')
            url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(nextid)

        else: 
            if difference1 != 0:
                valueofnexts1id = mylist2[pos_of_current_sub1+1]
                url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)
            else:            
                if difference2 != 0:
                    valueofnextchapid = mylist3[pos_of_current_chap+1]
                    url = str(bookid) + "/" + str(valueofnextchapid)
                else:
                    url = None
    

    
    
    
        if pre_difference1 != 0:
            valueofnexts1id = mylist2[pos_of_current_sub1-1]
            pre_url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)                    

        elif pre_difference1 == 0:    
            pre_url = str(bookid) + "/" + str(chapid)

    except:
        print("Something went wrong")
        url = None
        pre_url = None 


    myserializer = Subhead1TextSerializer(
        mysub1, context={"currentBook": bookname,
                         'request': request,
                         "nextUrl": url,
                        "previousUrl": pre_url, 
                        })
    
    

    return Response(myserializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def Subhead2Text(request, bookid, chapid, sub1id, sub2id):
    bookname = Books.objects.get(id=bookid).bookTitle
    mychapter = Chapter.objects.get(id=chapid).chapTitle
    # mysub1 = Subhead1.objects.get(id=sub1id)
    mysub2 = Subhead2.objects.get(id=sub2id)

    
    s2 = Subhead2.objects.filter(Subhead1__id=sub1id).values("id")
    no_of_ids = s2.filter().values("id")
    mylist = []
    for x in no_of_ids:
        mylist.append(x.get('id'))

    try:
        pos_of_current_sub2 = mylist.index(sub2id)
        pos_last_id_in_list = mylist.index(mylist[-1])
        pos_first_id_in_list = mylist.index(mylist[0])
        difference1 = pos_last_id_in_list-pos_of_current_sub2    
        pre_difference1 = pos_of_current_sub2 - pos_first_id_in_list 
    except:
        print("s2 went wrong")  


    s1 = Subhead1.objects.filter(Chapter__id=chapid).values("id")
    mylist2 = []
    for x in s1:
        mylist2.append(x.get('id'))

    try:
        pos_of_current_sub1 = mylist2.index(sub1id)
        pos_last_id_in_sub1_list = mylist2.index(mylist2[-1])
        difference2 = pos_last_id_in_sub1_list - pos_of_current_sub1  
    except:
        print("s1 went wrong") 
    

    ch = Chapter.objects.filter(Books__id=bookid).values("id")
    mylist3 = []
    for x in ch:
        mylist3.append(x.get('id'))
    try:
        pos_of_current_chap = mylist3.index(chapid)
        pos_last_id_in_chap_list = mylist3.index(mylist3[-1])    
        difference3 = pos_last_id_in_chap_list - pos_of_current_chap
    

        


        if difference1 != 0:
            valueofnextid = mylist[pos_of_current_sub2+1]
            url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(valueofnextid)

        elif difference1 == 0:    
            if difference2 != 0:
                valueofnexts1id = mylist2[pos_of_current_sub1+1]
                url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)
            else:
                if difference3 != 0:
                    valueofnextchapid = mylist3[pos_of_current_chap+1]
                    url = str(bookid) + "/" + str(valueofnextchapid)
                else:
                    url = None


        if pre_difference1 != 0:
            valueofnextid = mylist[pos_of_current_sub2-1]
            pre_url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(valueofnextid)

        elif pre_difference1 == 0:    
            pre_url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id)      
    except:
        print("last error")
        url = None
        pre_url = None
        
    myserializer = Subhead2TextSerializer(mysub2, context={"currentBook": bookname,
                                                           'request': request,
                                                           "currentChapter": mychapter,
                                                           "nextUrl": url,
                                                            "previousUrl": pre_url,
                                                           })
    return Response(myserializer.data)
