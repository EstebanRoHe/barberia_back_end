from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users.models import CustomUser

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(username=username) 
        except CustomUser.DoesNotExist:
            return Response({"detail": "Credenciales inválidas"}, status=401)

        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            response_data = {
                'token': str(token),
                'user_id': user.id,
                'username': user.username,
                'role': user.role, 
            }
            return Response(response_data)
        else:
            return Response({"detail": "Credenciales inválidas"}, status=401)


