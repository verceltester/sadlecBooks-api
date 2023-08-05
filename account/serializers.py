from rest_framework import serializers
from account.models import User, Profile, Bookmarks
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  # birthday = fields.DateField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
  class Meta:
    model = User
    fields=['email', 'name', "birthday", 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError(" hey Bitch Ass Nigga, can't u all type right? why u typing difffernt shit in password box?")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)
  

  
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']


class BookmarkSerializer(serializers.ModelSerializer):  
  class Meta:
    model = Bookmarks
    fields = ['id', "bookmarks"]


class ProfileSerializer(serializers.ModelSerializer):  
  mybookmark = BookmarkSerializer(many=True)
  class Meta:
    model = Profile
    fields = ['id','image', "mybookmark"]


class UserProfileSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer()  
  welcomeMsg = serializers.SerializerMethodField()
  



  def get_welcomeMsg(self, obj):
        if "welcomeMsg" in self.context:
            return self.context["welcomeMsg"]        
        return None
  
  class Meta:
    model = User
    fields = ['email', 'name' , 'birthday' , 'welcomeMsg', 'profile']


class SaveBookmarkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bookmarks
    fields = ['bookmarks', 'profile']


# SQL Query (postgress) to make sure id of both profile and user match ==== ALTER SEQUENCE account_profile_id_seq RESTART WITH 1
class ProfilePicUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['image']








class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
  


  


class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']



  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/api/user/reset-password/'+uid+'/'+token+'/'
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs 
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  