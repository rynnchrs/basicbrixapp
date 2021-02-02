from rest_framework import generics,viewsets
from rest_framework.response import Response
from .serializer import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from .models import *
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import filters


# Registration API for User Accounts
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        # checking if the user is valid or not
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


# List accounts but for Admin User only
class ListAccountsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


# Logout of Accounts as we put the JWT tokens into blacklist after logout
class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


# List only all products in Store with searching feature and ordering feature
class StoreViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = StoreSerializer
    # we use SearchFilter for search API and OrderingFilter for sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # we can search and order the API based on name and price
    search_fields = ['name','price']


# Create, Update, Retrieve and Delete the products in the store but for Admin User only
class AdminStoreViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdminStoreSerializer
    # we use SearchFilter for search API and OrderingFilter for sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # we can search and order the API based on name and price
    search_fields = ['name','price']
    # setting the permission to Admin only
    permission_classes = (IsAdminUser,)


# Cart API that will show the products in the cart with id, name, price, total etc.
class Cart(generics.ListAPIView):

    def list(self,request,*args,**kwargs):
        # getting the user data based on authentication
        customer = request.user.customer
        # query for the order table to check the products in the transaction
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        y=[]
        z=[]
        # query for the order item table to check the items on the order table
        for q in order.orderitem_set.all():
            y.append({"product_id":q.product.id,"product_name": q.product.name, "quantity": q.quantity, "price_per_piece": q.product.price, "total_price_per_product": q.product.price*q.quantity})
        z.append({"items": y})
        total = order.get_cart_total
        cart_items = order.get_cart_items
        # creation of JSON data for return purpose
        z.append({'order':order.transaction_id, 'total_cart_items':cart_items, 'total_price':total})

        return JsonResponse(z, safe=False)


# Update API for the add and remove item in the cart with automatic recalculation
class UpdateItem(APIView):

    def post(self,request):
        # checking the product id in the request data to specify which item will be added or removed
        product_id = request.data['productId']
        # checking for the action data
        action = request.data['action']
        # checking for the user data
        customer = request.user.customer
        # query for the product table with the product id indicated in request
        product = Product.objects.get(id=product_id)
        # getting the order id for adding and removing
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # getting the items in the order item table
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        # if the action is add we will increment a value in the cart
        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        # if the action is remove we will decrement a value in the cart
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)

        # saving the transaction
        order_item.save()

        # if the item is equal to 0, it will be deleted in the cart
        if order_item.quantity <= 0:
            order_item.delete()

        # redirecting in the Cart API to show the updated cart values
        return redirect("cart")


