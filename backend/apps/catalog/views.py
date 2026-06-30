from rest_framework import request, status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Product, Tag, ProductImage
from .serializers import ProductSerializer, TagSerializer, ProductImageSerializer
from ..reviews.models import Review
from ..reviews.serializers import ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from ..specifications.serializers import SpecificationSerializer


class ProductView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Фильтрация
        name = request.query_params.get('filter[name]', '')
        if name:
            queryset = queryset.filter(title__icontains=name)

        min_price = request.query_params.get('filter[minPrice]')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = request.query_params.get('filter[maxPrice]')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        freeDelivery = request.query_params.get('filter[freeDelivery]')
        if freeDelivery in ['true', 'True']:
            queryset = queryset.filter(freeDelivery=True)
        elif freeDelivery and freeDelivery.lower() == 'false':
            queryset = queryset.filter(freeDelivery=False)

        # queryset = queryset.filter(count__gt=0)
        available = request.query_params.get('filter[available]')
        if available in ['true']:
            queryset = queryset.filter(stock__gt=0)

        category_id = request.query_params.get('category')
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(category_id=category_id)
            except ValueError:
                pass

        subcategory_id = request.query_params.get('subcategory')
        if subcategory_id:
            try:
                subcategory_id = int(subcategory_id)
                queryset = queryset.filter(subcategory_id=subcategory_id)
            except ValueError:
                pass

        # Сортировка
        sort = request.query_params.get('sort', 'price')
        sort_type = request.query_params.get('sortType', 'inc')
        if sort_type == 'inc':
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by(f'-{sort}')

        # Пагинация
        current_page = int(request.query_params.get('currentPage', 1))
        limit = int(request.query_params.get('limit', 20))
        start = (current_page - 1) * limit
        end = start + limit
        paginated_products = queryset[start:end]

        serializer = ProductSerializer(paginated_products, many=True)
        return Response({
            'items': serializer.data,
            'currentPage': current_page,
            'lastPage': (Product.objects.count() + limit - 1) // limit  # простая формула для lastPage
        })

class ProductDetailsView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Изображения
        images = ProductImage.objects.filter(product=product)
        images_data = ProductImageSerializer(images, many=True, context={'request': request}).data

        # Теги
        tags = product.tags.all()
        tags_data = TagSerializer(tags, many=True).data

        # Отзывы
        reviews = Review.objects.filter(product=product)
        reviews_data = ReviewSerializer(reviews, many=True).data

        # Характеристики
        specifications = product.specifications.all()
        specifications_data = SpecificationSerializer(specifications, many=True).data

        response_data = {
            'id': product.id,
            'category': product.category.id,
            'subcategory': product.subcategory.id if product.subcategory else None,
            'price': str(product.price),
            'count': product.stock,
            'date': product.date.isoformat(),
            'title': product.title,
            'description': product.description,
            'fullDescription': product.fullDescription,
            'freeDelivery': product.freeDelivery,
            'images': images_data,
            'tags': [tag["name"] for tag in tags_data],
            'reviews': reviews_data,
            'specifications': specifications_data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PopularProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by(
            'sort_index', '-sales_count'
        ).distinct()[:3]

class LimitedProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(stock__lte=4)
