from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Category display order")

    def __str__(self):
        return self.name or 'Unnamed Category'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order']  # This ensures categories are ordered by this field

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    view_link = models.URLField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    account_details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Add this field

    def __str__(self):
        return f"{self.name} - {self.price}"

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)  # Allow null values
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='transactions')
    tx_ref = models.CharField(max_length=100, blank=True, null=True)
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('declined', 'declined'),
    )
    transaction_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.amount} - {self.transaction_status}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class BankPaymentDetail(models.Model):
    account_number = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number} - {self.account_holder_name} - {self.active}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        else:
            return f"Cart for session {self.session_key}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.cart and self.cart.user:
            return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
        return f"{self.quantity} of {self.product.name} in an anonymous cart"

    def total_price(self):
        return self.product.price * self.quantity

