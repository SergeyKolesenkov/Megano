from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Basket, BasketItem
from .serializers import BasketItemSerializer
from .serializers import BasketSerializer

class BasketView(APIView):
    def get(self, request):
        basket = Basket.objects.get(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        # Находим конкретную позицию в корзине
        try:
            basket_item = BasketItem.objects.get(id=pk)
        except BasketItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        new_count = request.data.get('count')

        # if new_count is None or int(new_count) < 1:
        #     basket_item.delete()
        #     return Response({'status': 'deleted'}, status=status.HTTP_200_OK)

        basket_item.count = new_count
        basket_item.save()

        # Возвращаем полную корзину
        from .serializers import BasketSerializer
        basket_serializer = BasketSerializer(basket_item.basket)
        return Response(basket_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        # 1. Получаем или создаем корзину пользователя
        basket, created = Basket.objects.get_or_create(user=request.user)

        serializer = BasketItemSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            print(f"Ошибки валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_obj = serializer.validated_data['product']
        product_id = product_obj.id
        count_to_add = serializer.validated_data.get('count', 1)
        available_stock = product_obj.stock

        existing_item = basket.basket_items.filter(product_id=product_obj.id).first()
        current_count_in_basket = existing_item.count if existing_item else 0

        total_requested = current_count_in_basket + count_to_add

        if total_requested > available_stock:
            return Response({
                'error': 'Недостаточно товара на складе!',
                'available': available_stock,
                'current_in_basket': current_count_in_basket,
                'requested_total': total_requested,
                'can_add_more': max(0, available_stock - current_count_in_basket)
            }, status=status.HTTP_400_BAD_REQUEST)
        existing_item = basket.basket_items.filter(product_id=product_id).first()
        if existing_item:
            existing_item.count += count_to_add
            existing_item.save()
            print(f"Дубликат найден! Увеличено количество товара {product_id}. Новый count: {existing_item.count}")

            # Возвращаем данные корзины (как и раньше)
            basket_serializer = BasketSerializer(basket)
            return Response(basket_serializer.data, status=status.HTTP_200_OK)
        else:
            # Если товара НЕТ -> создаем новую позицию
            try:
                basket_item = serializer.save(basket=basket)
                basket_serializer = BasketSerializer(basket)
                return Response(basket_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'detail': 'ID не передан'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(f'мой pk: {pk}')
            item = BasketItem.objects.get(id=pk)
            print(f'item:{item}')
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BasketItem.DoesNotExist:
            return Response({'detail': 'Позиция не найдена'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket = request.user.basket

        product_id = serializer.validated_data['product']['id']
        count_to_add = serializer.validated_data.get('count', 1)
        existing_item = basket.basket_items.filter(product_id=product_id).first()

        if existing_item:
            existing_item.count += count_to_add
            existing_item.save()
            return Response(self.get_serializer(existing_item).data, status=status.HTTP_200_OK)
        else:
            serializer.save(basket=basket)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartView(APIView):
    def get(self, request):
        basket, created = Basket.objects.get_or_create(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)