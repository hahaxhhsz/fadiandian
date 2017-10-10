

# Create your views here.
from users.models import Users
from users.serializers import UsersSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

# 获取所有用户信息
class getAllUsers(APIView):

    def get(self, request):
        myResponse = {}
        data = {}
        data["userList"] = ""
        try:
            users = Users.objects.all()
            serializer = UsersSerializer(users, many=True)
            data["userList"] = serializer.data
            myResponse["state"] = 1
        except:
            myResponse["state"] = 0
        finally:
            myResponse["data"] = data
            return Response(myResponse)


# 注册
class registered(APIView):

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        myResponse = {}
        if serializer.is_valid():
            serializer.save()
            myResponse["state"] = 1
            myResponse["msg"] = "Successfully registered"
        else:
            myResponse["state"] = 0
            myResponse["msg"] = smart_str(serializer.errors)

        return Response(myResponse)



# 登陆，若已登陆的账号无法实现再次登陆
class login(APIView):

    def post(self, request):
        myResponse = {}
        data = {}
        try:
            theUserName = request.data["userName"]
            user = Users.objects.get(userName=theUserName)
            serializer = UsersSerializer(user)
            state = serializer.data["state"]
            thePassword = serializer.data["userPassword"]
            password = request.data["userPassword"]
            if password == thePassword and state == 0 :
                mydata =  serializer.data["id"]
                data["userId"] = mydata
                myResponse["state"] = 1
                user.state = 1
                user.save()
            elif state == 1 :
                myResponse["state"] = 0
                data["msg"] = "This account has been logged in"
            else:
                myResponse["state"] = 0
                data["msg"] = "The account or password is incorrect"
        except:
            myResponse["state"] = 0
            data["msg"] = "The account or password is incorrect"
        finally:
            myResponse["data"] = data
            return Response(myResponse)


# 登出
class logout(APIView):

    def post(self, request):
        myResponse = {}
        data = {}
        try:
            theId = int(request.data["id"])
            user = Users.objects.get(pk=theId)
            serializer = UsersSerializer(user)
            state = serializer.data["state"]
            if state == 1 :
                user.state = 0
                user.save()
                myResponse["state"] = 1
                data["msg"] = "Logout successfully"
            else:
                myResponse["state"] = 0
                data["msg"] = "This account is not logged in"
        except:
            myResponse["state"] = 0
            data["msg"] = "id error"
        finally:
            myResponse["data"] = data
            return Response(myResponse)


# 获取单个用户信息
class getUserInfo(APIView):

    def post(self, request):
        myResponse = {}
        data = {}
        try:
            theId = int(request.data["id"])
            user = Users.objects.get(pk=theId)
            serializer = UsersSerializer(user)
            data["userInfo"] = serializer.data
            myResponse["state"] = 1
        except:
            data["msg"] = "id error"
            myResponse["state"] = 0
        finally:
            myResponse["data"] = data
            return Response(myResponse)