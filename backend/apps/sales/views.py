import math
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Sale
from .serializers import SaleSerializer
from ..catalog.models import ProductImage

def sales_page(request):
    return render(request, 'frontend/sales.html')

class SalesView(APIView):
    def get(self, request):
        now = timezone.now()
        sales = Sale.objects.filter(
            is_active=True,
            date_from__lte=now,
            date_to__gte=now
        ).select_related('product')

        items = []
        for sale in sales:
            image_obj = ProductImage.objects.filter(product=sale.product).first()
            images = []
            if image_obj and image_obj.src:
                images.append({
                    'src': image_obj.src.url,
                    'alt': image_obj.alt or sale.product.title or 'Товар'
                })

            serialized = SaleSerializer(sale).data

            items.append({
                'id': str(sale.id),
                'price': serialized['price'],
                'salePrice': serialized['salePrice'],
                'title': serialized['title'],
                'dateFrom': sale.date_from.strftime("%m-%d"),
                'dateTo': sale.date_to.strftime("%m-%d"),
                'images': images
            })

        # Пагинация
        try:
            current_page = int(request.GET.get('currentPage', 1))
        except ValueError:
            current_page = 1

        page_size = 10
        total_items = len(items)
        last_page = max(1, math.ceil(total_items / page_size) if total_items else 1)

        start = (current_page - 1) * page_size
        end = start + page_size
        paginated_items = items[start:end]

        return Response({
            'items': paginated_items,
            'currentPage': current_page,
            'lastPage': last_page
        })