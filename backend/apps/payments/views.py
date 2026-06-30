from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.basket.models import BasketItem
from apps.orders.models import Order


class PaymentView(APIView):
    def post(self, request, id):
        # 1. Проверяем авторизацию
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_403_FORBIDDEN)

        # 2. Находим заказ текущего пользователя
        order = get_object_or_404(Order, pk=id, customer__user=request.user)

        data = request.data
        card_number = data.get('number', '')

        # 3. Базовая валидация «банка» (например, номер карты должен заканчиваться не на 0)
        if not card_number or card_number.endswith('0'):
            return Response(
                {"detail": "Неверный номер карты или недостаточно средств (тестовая ошибка)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in order.items.all():
            product = item.product
            if product:
                # Еще раз на всякий случай проверяем остаток перед списанием
                if product.stock >= item.count:
                    product.stock -= item.count
                    product.save()
                else:
                    return Response(
                        {"detail": f"Пока вы оплачивали, товар '{product.title}' закончился."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # 4. Меням статус заказа на «Оплачено»
        order.status = 'paid'  # или 'accepted' в зависимости от вашей бизнес-логики статусов
        order.save()
        # 6. Очищаем корзину (удаляем все её элементы, саму корзину не трогаем)
        BasketItem.objects.filter(basket__user=request.user).delete()
        return Response(status=status.HTTP_200_OK)