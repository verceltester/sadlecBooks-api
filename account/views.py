from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  ProfilePicUpdateSerializer, SendPasswordResetEmailSerializer, SaveBookmarkSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import Bookmarks, Profile, User
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      # 'refresh': str(refresh),
      'access token': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
  
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # token = get_tokens_for_user(user)
    return Response({'msg':'Your Registration is Successful!'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      profileid = Profile.objects.get(user=user).id
      return Response({'token':token, 'msg':'Login Successfull!', 'user':user.name, 'profileId':profileid},  status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':["Email or Password is not Valid!"]}}, status=status.HTTP_404_NOT_FOUND)



#age calculator
def ageCal(birthday):
  now = datetime.now()
  bd = datetime.strptime(str(birthday), "%Y-%m-%d")
  difference = now - bd
  age_in_years = difference.days // 365

  if age_in_years in range(1, 15):
    comment = "Jai Sri Ma"
    # print(comment)
    return comment
  elif age_in_years in range(16, 25):
    comment = "Jai Sri Ma"
    # print(comment)
    return comment
  elif age_in_years in range(26, 35):
    comment = "Jai Sri Ma!"
    # print(comment)
    return comment
  elif age_in_years > 35:
    comment = "Jai Sri Ma"
    # print(comment)
    return comment
    

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    # bdd = User.objects.filter(id=request.user.id).values_list('birthday')
    birthday = User.objects.values_list('birthday').get(id=request.user.id)[0] 
    # print(ageCal(birthday)) 
    serializer = UserProfileSerializer(request.user, context = {"welcomeMsg": ageCal(birthday)})
    return Response(serializer.data, status=status.HTTP_200_OK)

class SaveBookmark(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    profileid  = request.data.get("profile")
    # urlFrontend = request.data.get("bookmarks").get("url")
    bookmarkContent = request.data.get("bookmarks").get("content")
    userid = request.user.id  
    if userid == int(profileid):
      # bk = Bookmarks.objects.filter(profile__id=profileid).values("bookmarks").filter(bookmarks__contains={"url": urlFrontend}).exists()
      bk = Bookmarks.objects.filter(profile__id=profileid).values("bookmarks").filter(bookmarks__contains={"content": bookmarkContent}).exists()
      if bk:
        return Response({'msg':"Bookmark already Saved No need to add again"}, status=status.HTTP_401_UNAUTHORIZED)        
      else:
        serializer = SaveBookmarkSerializer(data=request.data)    
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':"Bookmark Saved Successfully!"}, status=status.HTTP_201_CREATED)
    else:
      return Response({'msg':"Not allowed for you nigga."}, status=status.HTTP_401_UNAUTHORIZED)
    
    
  def delete(self, request, format=None):
    profileId  = request.data.get("profileId")     
    userid = request.user.id
    bookmarkId  = int(request.data.get("bookmarkId"))
    if userid == int(profileId):
      bk = Bookmarks.objects.filter(profile__id=profileId).values("id")
      mylist = []
      for x in bk:
        mylist.append(x.get('id'))
      # print(mylist)
      if bookmarkId in mylist:      
        bookmarkToDel = Bookmarks.objects.get(id=bookmarkId)
        bookmarkToDel.delete()   
        return Response({'msg':"Bookmark deleted Successfully!"}, status=status.HTTP_200_OK)
      else:
        return Response({'msg':"Not allowed for you!"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'msg':"Not allowed for you!"}, status=status.HTTP_401_UNAUTHORIZED)


class ProfilePicUpdate(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def put(self, request, format=None): 
    profileid  = request.data.get("profileid")     
    userid = request.user.id
    # print(type(userid))
    # print(type(profileid))
    
    if userid == int(profileid):
      profieToUpdate = get_object_or_404(Profile, id=profileid)
      # profieToUpdate = Profile.objects.get(id=profileid)         
      serializer = ProfilePicUpdateSerializer(profieToUpdate, data=request.data,  partial=True, context={'user':request.user})
      serializer.is_valid(raise_exception=True)    
      serializer.save()
      return Response({'msg':"profile pic Saved Successfully!"}, status=status.HTTP_200_OK)
    else:
      return Response({'msg':"Not allowed for you!"}, status=status.HTTP_401_UNAUTHORIZED)
      


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user.id})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':"Password Changed Successfully!"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'},  status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
