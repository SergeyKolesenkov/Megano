import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Profile
from .models import Order, OrderItem
from .serializers import OrderSerializer
from django.views.generic import TemplateView

from ..basket.models import Basket


class OrderHistoryPageView(TemplateView):
    template_name = 'frontend/history-order.html'

class OrderListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=403)

        # Находим все заказы текущего пользователя
        orders = Order.objects.filter(customer__user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(orders, many=True)  # many=True обязателен для списка
        return Response(serializer.data)

class OrderView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=403)

        orders = Order.objects.filter(customer__user=request.user).prefetch_related('items__product')
        serializer = OrderSerializer(orders, many=True)  # many=True обязателен для списка
        return Response(serializer.data)
    def post(self, request):
        # 1. Проверяем авторизацию
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_403_FORBIDDEN)

        try:
            customer_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"detail": "Профиль пользователя не найден"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Получаем корзину текущего пользователя через связь OneToOne
        try:
            basket = request.user.basket
            # Извлекаем все товары из этой корзины
            basket_items = basket.basket_items.select_related('product').all()
        except Basket.DoesNotExist:
            return Response({"detail": "Корзина не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if not basket_items.exists():
            return Response({"detail": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Генерируем уникальный номер заказа для вашей модели
        order_number = f"ORD-{random.randint(100000, 999999)}"
        while Order.objects.filter(order_number=order_number).exists():
            order_number = f"ORD-{random.randint(100000, 999999)}"

        # 4. Считываем camelCase данные формы от фронтенда
        data = request.data

        # Создаем пустой заказ с мета-данными покупателя
        order = Order.objects.create(
            customer=customer_profile,
            order_number=order_number,
            city=data.get('city', ''),
            address=data.get('address', ''),
            delivery_type=data.get('deliveryType', 'standard'),
            payment_type=data.get('paymentType', 'online'),
            total_cost=0,
            status='new'
        )

        total_price = 0

        # 5. Переносим товары из BasketItem в OrderItem [3]
        for item in basket_items:
            product = item.product
            count = item.count  # Берем count из вашей модели BasketItem [3]
            if product.stock < count:
                # Если товара не хватает, удаляем уже созданный черновик заказа и возвращаем ошибку
                order.delete()
                return Response(
                    {"detail": f"Недостаточно товара '{product.title}' на складе. Доступно: {product.stock} шт."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item_total = product.price * count
            total_price += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                count=count,
            )

        # Фиксируем итоговую стоимость и сохраняем заказ
        order.total_cost = total_price
        order.save()



        # Возвращаем ID заказа в обоих форматах для надежности фронтенда
        return Response({"id": order.id, "orderId": order.id}, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    def get(self, request, id):
        try:
            order = Order.objects.select_related(
                'customer',
            ).prefetch_related(
                'items',
                'items__product',
                'items__product__images',
                'items__product__tags'
            ).get(pk=id)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=404)

        serializer = OrderSerializer(order)
        return Response(serializer.data)