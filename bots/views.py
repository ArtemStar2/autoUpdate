from rest_framework import status
from rest_framework.response import Response
from rest_framework import status, permissions, generics
import requests
from .serializers import BotsSerializer
from orders.models import Order

class BotsView(generics.ListAPIView):
    serializer_class = BotsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            url = "http://127.0.0.1:8000/upload/all.json"

            headers = {
                "Content-Type": "application/json",
            }

            response = requests.get(url, headers=headers)  # Заменено на requests.get
            response.raise_for_status()
            response_data = response.json()

            return Response(response_data, status=200)
        except requests.exceptions.RequestException as e:
            return Response({"detail": "Сервер не отвечает"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            url = "http://127.0.0.1:8000/upload/pause.json"
            data = request.data
            
            headers = {
                "Content-Type": "application/json",
            }
            
            user = self.request.user
            try:
                order = Order.objects.get(id= request.data["order_id"], user=user)
            except:
                return Response({"detail": "Заказ не найден"}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.data["type"] != "active" and request.data["type"] != "pause" and request.data["type"] != "success" and request.data["type"] != "error":
                return Response({"detail": "Выбирете тип команды"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "order_id": order.id,
                "login_bot": order.login_bot,
                "type" : request.data["type"],
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            print(response_data)
            if response_data["server"]:
                order.status =  response_data["server"]
                order.save()
            else:
                return Response({"detail": "Ошибка при отправке"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(response_data, status=200)
        except requests.exceptions.RequestException as e:
            return Response({"detail": "Сервер не отвечает"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class BotsMessageView(generics.ListAPIView):
    serializer_class = BotsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            url = "http://127.0.0.1:8000/upload/messanger.json"
            data = request.data
            
            headers = {
                "Content-Type": "application/json",
            }
            
            user = self.request.user
            try:
                order = Order.objects.get(id= request.data["order_id"], user=user)
            except:
                return Response({"detail": "Заказ не найден"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not request.data["message"]:
                return Response({"detail": "Ввидите сообщение"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "order_id": order.id,
                "login_bot": order.login_bot,
                "message" : request.data["message"],
            }

            response = requests.post(url, headers=headers, json=data)  # Заменено на requests.get
            response.raise_for_status()
            response_data = response.json()

            return Response(response_data, status=200)
        except requests.exceptions.RequestException as e:
            return Response({"detail": "Сервер не отвечает"}, status=status.HTTP_400_BAD_REQUEST)