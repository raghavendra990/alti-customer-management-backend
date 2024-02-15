from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import jwt
from datetime import datetime, timedelta
from .log import LOGGER, raise_400
from .authentication import IsTokenValid
from .models import UserModel, BlackListedToken, Plan
from .serializers import LoginSerializer, RegisterSerializer, UserDetailsSerializer, PlanSerializer, UpgradeDowngradeSerializer

# Create your views here.

USER_ALREADY_PRESENT = "User Already Exist."
USER_NOT_EXIST = "User Does not Exist."
PLAN_NOT_EXIST = "Plan Does not Exist."


INVALID_LOGIN = "Invalid phonenumber or Password."
class RegisterAPIView(APIView):

    """
    Register API
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user_exist(self, phone_number):
        user = UserModel.objects.filter(phone_number=phone_number)
        if user:
            raise_400(USER_ALREADY_PRESENT)
    
    def _get_plan(self, data):
        try:
            plan_obj = Plan.objects.get(id=data['plan'], status = 'active')
            if not plan_obj:
                raise_400(PLAN_NOT_EXIST)
           

            return plan_obj
        except Exception as e:
            raise_400(PLAN_NOT_EXIST)
    
    def generate_jwt_token(self, data):
        data['created_at'] = str(datetime.utcnow())

        return 'JWT {}'.format(jwt.encode(data,settings.JWT_SECRET_KEY, algorithm='HS256'))

    def post(self, request):
        current_time = datetime.now()

        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = str(serializer.validated_data['email'])

        self._check_user_exist(email)
        plan_obj = self._get_plan(serializer.data)
        validated_data = serializer.data
        validated_data['plan'] = plan_obj
        validated_data['expiry'] = (current_time + timedelta(days=plan_obj.validity)).date()
        validated_data['plan_status'] = 'active'
        user_obj = UserModel.register(data=validated_data)
        token = self.generate_jwt_token({"email": validated_data['email'], "id": str(user_obj.id) }) 
        payload = {"id": user_obj.id, "phone_number": user_obj.phone_number, "name": user_obj.name,
                    "plan": plan_obj.name, 'dob': user_obj.dob, 'expiry': user_obj.expiry, 'plan_status': user_obj.plan_status, "token": token, 'plan_status': user_obj.plan_status}
        return Response(status=200, data=payload)

class PlanView(APIView):  # pylint: disable=abstract-method
    permission_classes = [AllowAny]
    

    def get(self, request):
        serializers = PlanSerializer
        plan_obj = Plan.objects.filter(status = 'active')
        data = serializers(plan_obj, many=True)
        return Response(status=200, data=data.data)
 
class LoginAPIView(APIView):

    """
    Login API
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user(self, email):
        try:
            user = UserModel.objects.get(email=email)
            if not user:
                raise_400(USER_NOT_EXIST)
        except Exception as e:
            raise_400(USER_NOT_EXIST)
        return user
    
    def generate_jwt_token(self, data):
        data['created_at'] = str(datetime.utcnow())

        return 'JWT {}'.format(jwt.encode(data,settings.JWT_SECRET_KEY, algorithm='HS256'))


    def post(self, request):
        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = str(serializer.validated_data['email'])
        password = serializer.validated_data['password']

        user = self._check_user(email)

        verified_check = UserModel.verify_password(user.password, password, email)

        if verified_check:
            token = self.generate_jwt_token({"email": email, "id": str(user.id) })
        else:
            return Response(status=403, data={"message": INVALID_LOGIN})
        return Response(status=200, data={"token":token})

class LogoutAPIView(APIView):

    """
    Logout API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    # serializer_class = LoginSerializer

    # def get_serializer(self, *args, **kwargs):
    #     """Return view serializer class"""
    #     return self.serializer_class(*args, **kwargs)


    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_id = request.user.user_id
        user_obj = UserModel(id=user_id)
        blt_obj = BlackListedToken(token=token, user=user_obj)
        blt_obj.save()
        return Response(status=200, data={"messge": "logout successfully"})

class UserDetailsAPIView(APIView):

    """
    UserDetails API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    
    def get(self, request):
        current_date = datetime.now().date()
        serializers = UserDetailsSerializer
        user_id = request.user.user_id
        user_obj = UserModel.objects.get(id=user_id)
        if (user_obj.expiry< current_date):
            user_obj.plan_status = 'inactive'
            user_obj.save()
        data = serializers(user_obj).data
        data['plan'] = user_obj.plan.name
        return Response(status=200, data=data)


class RenewPlan(APIView):

    """
    Renew Plan API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]

    
    def get(self, request):
        current_time = datetime.now()
        current_date = current_time.date()
        user_id = request.user.user_id
        user_obj = UserModel.objects.get(id=user_id)
        if user_obj.expiry < current_date:
            plan_obj = user_obj.plan
            user_obj.expiry = (current_time + timedelta(days=plan_obj.validity)).date()
            user_obj.plan_status = 'active'
            user_obj.save()
            data = {'plan_renew_status': 'success'}
            return Response(status=200, data=data)
        else:
            data = {'plan_renew_status': 'failed', "message": "plan not expired"}
            return Response(status=400, data=data)

class UpgradeDowngradePlan(APIView):

    """
    Renew Plan API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    
    def _get_plan(self, id):
        try:
            plan_obj = Plan.objects.get(id=id, status = 'active')
            if not plan_obj:
                raise_400(PLAN_NOT_EXIST)
           

            return plan_obj
        except Exception as e:
            raise_400(PLAN_NOT_EXIST)
    
    def post(self, request):
        current_time = datetime.now()
        current_date = current_time.date()

        serializer = UpgradeDowngradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.user_id
        
        plan_id = serializer.validated_data['id']
        plan_obj = self._get_plan(plan_id)

        user_obj = UserModel.objects.get(id=user_id)

        if user_obj.plan.id != plan_obj.id:
            user_obj.plan = plan_obj
            if user_obj.expiry< current_date:
                user_obj.expiry = (datetime.now() + timedelta(days=plan_obj.validity)).date()
                user_obj.plan_status = 'active'
            user_obj.save()
            data = {'Plan_upgrade_downgrade_status': 'success'}
            return Response(status=200, data=data)
        else:
            data = {'Plan_upgrade_downgrade_status': 'failed', "message": "plan id can not same as existing"}
            return Response(status=400, data=data)
