from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserUpdateSerializer, CustomUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
import json
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
import random
from response_utils import success_response, not_found_response, bad_request_response, forbidden_response, unauthorized_response, server_error_response

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateUser(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(decoded_token)

        if user.is_user_active == False:
            return bad_request_response(msg="You cant update details until you verify your email address!")

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serialized_data = {key: value for key, value in body.items()}  # Convert to dictionary
        queryset = CustomUser.objects.filter(id=user.id).update(**serialized_data) 
        return success_response(msg="User Updated Successfully.")
    except Exception as e:
        return server_error_response(apiMsg="Error while updating user!", error=str(e))
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request):
    try:
        user = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email,
            'country': user.country,
        }

        # serializer = CustomUserSerializer(user) ==> serializer.data

        return success_response(msg="User Details Fetched Successfully", data=user_data)
    except Exception as e:
        return server_error_response(apiMsg="Error while fetching user details!", error=str(e))


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send_otp(request):
    try:
        user = request.user
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        body = f"""
            <!DOCTYPE html>
            <html>
              <head>
                <title>Hello World!</title>
                <link rel="stylesheet" href="styles.css" />
              </head>
              <body> 
                <table align="center" border="0" cellpadding="0" cellspacing="0"
                       width="550" bgcolor="white" style="border:2px solid black"> 
                    <tbody> 
                        <tr> 
                            <td align="center"> 
                                <table align="center" border="0" cellpadding="0" 
                                       cellspacing="0" class="col-550" width="550"> 
                                    <tbody> 
                                        <tr> 
                                            <td align="center" style="background-color: #173D7A; 
                                                       height: 50px;"> 
  
                                                <a href="https://www.dolphinfurnishingindia.com" style="text-decoration: none;  padding-horizontal: 5px"> 
                                                    <p style="color:white; font-size: 25px;
                                                              font-weight:bold;"> 
                                                        Welcome To My User Api
                                                    </p> 
                                                </a> 
                                            </td> 
                                        </tr> 
                                    </tbody> 
                                </table> 
                            </td> 
                        </tr> 
                        <tr style="height: 200px;"> 
                            <td align="center" style="border: none; 
                                       border-bottom: 2px solid #79635D;  
                                       padding-right: 20px;padding-left:20px"> 
  
                                <p style="font-weight: bolder;font-size: 25px; 
                                          letter-spacing: 0.025em; 
                                          color:black;"> 
                                         Hello, {user.first_name}
                                    <br> Email Verification
                                </p> 
                            </td> 
                        </tr> 
  
                        <tr style="display: inline-block;"> 
                            <td style="height: 150px; 
                                       padding: 20px; 
                                       border: none;  
                                       border-bottom: 2px solid #79635D; 
                                       background-color: white;"> 
                                
                                <h2 style="text-align: left; 
                                           align-items: center;"> 
                                    Your OTP for email verification is: {otp}
                                </h2> 

                                 <p style="text-align: left; 
                                           align-items: center;">
                              Your username is {user.username}
                                </p>

                                <p class="data" 
                                   style="text-align: justify-all; 
                                          align-items: center;  
                                          font-size: 15px; 
                                          padding-bottom: 12px;"> 
                                   Thank you for choosing us.
                                </p> 
                                <p> 
                                </p> 
                            </td> 
                        </tr> 
                    </tbody> 
                </table> 
            </body> 
            </html>
        """

        email = EmailMessage('Email Verification', body, 'sansakhraliy@gmail.com', [user.email])
        email.content_subtype = 'html'
        email.send()

        queryset = CustomUser.objects.filter(id=user.id).update(otp=otp)
        return success_response(msg="OTP has been sent to your registered email address")
    except Exception as e:
        return server_error_response(apiMsg="Error while sending OTP!", error=str(e))
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def verify_otp(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        decoded_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(decoded_token)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        userQueryset = CustomUser.objects.get(id=user.id)

        if body['otp'] is None:
            return bad_request_response(msg="OTP is required")

        elif body['otp'] == userQueryset.otp:
            queryset = CustomUser.objects.filter(id=user.id).update(otp=None, is_user_active=True)
            return bad_request_response(msg="Your account has been activated. Now you can update your details")
        
        else:
            return bad_request_response(msg="OTP is invalid. Try again...")
    except Exception as e:
        return server_error_response(apiMsg="Error while verifying OTP!", error=str(e))