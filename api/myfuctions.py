

# from .models import *



# def Subhead2Text(request, bookid, chapid, sub1id, sub2id):
#     bookname = Books.objects.get(id=bookid).bookTitle
#     mychapter = Chapter.objects.get(id=chapid).chapTitle
#     # mysub1 = Subhead1.objects.get(id=sub1id)
#     mysub2 = Subhead2.objects.get(id=sub2id)






#     p = Subhead2.objects.filter(Subhead1__id=sub1id).values("id")
#     no_of_ids = p.filter().values("id")
#     mylist = []
#     for x in no_of_ids:
#         mylist.append(x.get('id'))
#     pos_of_current_sub2 = mylist.index(sub2id)
#     pos_last_id_in_list = mylist.index(mylist[-1])
#     difference1 = pos_last_id_in_list-pos_of_current_sub2


#     s1 = Subhead1.objects.filter(Chapter__id=chapid).values("id")
#     mylist2 = []
#     for x in s1:
#         mylist2.append(x.get('id'))
#     pos_of_current_sub1 = mylist2.index(sub1id)
#     pos_last_id_in_sub1_list = mylist2.index(mylist2[-1])
#     difference2 = pos_last_id_in_sub1_list - pos_of_current_sub1


#     ch = Chapter.objects.filter(Books__id=bookid).values("id")
#     mylist3 = []
#     for x in ch:
#         mylist3.append(x.get('id'))
#     pos_of_current_chap = mylist3.index(chapid)
#     pos_last_id_in_chap_list = mylist3.index(mylist3[-1])
#     difference3 = pos_last_id_in_chap_list - pos_of_current_chap



    

#     if difference1 != 0:
#         valueofnextid = mylist[pos_of_current_sub2+1]
#         url = str(bookid) + "/" + str(chapid) + "/" + str(sub1id) + "/" + str(valueofnextid)

#     elif difference1 == 0:    
#         if difference2 != 0:
#             valueofnexts1id = mylist2[pos_of_current_sub1+1]
#             url = str(bookid) + "/" + str(chapid) + "/" + str(valueofnexts1id)
#         else:
#             if difference3 != 0:
#                 valueofnextchapid = mylist3[pos_of_current_chap+1]
#                 url = str(bookid) + "/" + str(valueofnextchapid)
#             else:
#                 url = "end of book"