from rest_framework.response import Response
from rest_framework import serializers
from  rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
from .models import User
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserPasswordResetSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request ,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # return Response({'msg': 'Register successfully'},status=status.HTTP_201_CREATED)
        token=get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration successfully'},status=status.HTTP_201_CREATED)




class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request ,format=None):
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            # return Response({'msg':'Login Successfully'},status=status.HTTP_200_OK)
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Login successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)





class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,formate=None):
        serializer=UserProfileSerializer(request.user)
        # serializer.is_valid()
        return Response(serializer.data,status=status.HTTP_200_OK)




class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,formate=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,formate=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Link Send . Please Check Your Email'},status=status.HTTP_200_OK)




class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg': 'password Reset successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)



