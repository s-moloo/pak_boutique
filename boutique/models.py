from django.db import models
from django.contrib.auth.models import User

# ── Inventory Models ───────────────────────────────────────────────────

class Women(models.Model):
    CATEGORY_CHOICES = [
        ('shalwarkameez', 'Shalwar Kameez'),
        ('sarees', 'Sarees'),
        ('lehengas', 'Lehengas'),
    ]

    description  = models.CharField(max_length=60)
    color        = models.CharField(max_length=60)
    size = models.CharField(max_length=100, blank=True, null=True)             # CharField
    price        = models.DecimalField(                        # DecimalField
                       max_digits=10, decimal_places=2
                   )
    category     = models.CharField(
                       max_length=20, # Increased to 20 for safety
                       choices=CATEGORY_CHOICES,
                       default='shalwarkameez',
                   )
    
    details = models.TextField(blank=True, null=True, 
                        help_text="Enter material, design, pattern, and care instructions."
                )
    
    image        = models.ImageField(upload_to='images/')  # ImageField

    def __str__(self):
        return self.description
    
    @property
    def size_list(self):
        # Splits "S, M, L" into an actual Python list: ['S', 'M', 'L']
        if self.size:
            return [s.strip() for s in self.size.split(',') if s.strip()]
        return []
    
class Men(models.Model):
    CATEGORY_CHOICES = [
        ('kurta', 'Kurta'),
        ('sherwani', 'Sherwani'),
        ('waistcoat', 'Waistcoat'),
    ]

    description  = models.CharField(max_length=60)
    color        = models.CharField(max_length=60)
    size = models.CharField(max_length=100, blank=True, null=True)             # CharField
    price        = models.DecimalField(                        # DecimalField
                       max_digits=10, decimal_places=2
                   )
    category     = models.CharField(
                       max_length=20, # Increased to 20 for safety
                       choices=CATEGORY_CHOICES,
                       default='kurta',
                   )
    
    details = models.TextField(blank=True, null=True, 
                        help_text="Enter material, design, pattern, and care instructions."
                )
    image        = models.ImageField(upload_to='images/')  # ImageField

    def __str__(self):
        return self.description
    
    @property
    def size_list(self):
        # Splits "S, M, L" into an actual Python list: ['S', 'M', 'L']
        if self.size:
            return [s.strip() for s in self.size.split(',') if s.strip()]
        return []
    
class Kids(models.Model):
    CATEGORY_CHOICES = [
        ('kidswear', 'Kids Wear'),
        ('toys', 'Toys'),
        ('footwear', 'Footwear'),
    ]

    description  = models.CharField(max_length=60)
    color        = models.CharField(max_length=60)
    size = models.CharField(max_length=100, blank=True, null=True)             # CharField
    price        = models.DecimalField(                        # DecimalField
                       max_digits=10, decimal_places=2
                   )
    category     = models.CharField(
                       max_length=20, # Increased to 20 for safety
                       choices=CATEGORY_CHOICES,
                       default='kidswear',
                   )
    details = models.TextField(blank=True, null=True, 
                        help_text="Enter material, design, pattern, and care instructions."
                   )
    image        = models.ImageField(upload_to='images/')  # ImageField

    def __str__(self):
        return self.description
    
    @property
    def size_list(self):
        # Splits "S, M, L" into an actual Python list: ['S', 'M', 'L']
        if self.size:
            return [s.strip() for s in self.size.split(',') if s.strip()]
        return []
    
class Accessory(models.Model):
    CATEGORY_CHOICES = [
        ('jewelry', 'Jewelry'),
        ('handbags', 'Handbags'),
        ('scarves', 'Scarves'),
    ]

    description  = models.CharField(max_length=60)
    color        = models.CharField(max_length=60)
    size = models.CharField(max_length=100, blank=True, null=True)             # CharField
    price        = models.DecimalField(                        # DecimalField
                       max_digits=10, decimal_places=2
                   )
    category     = models.CharField(
                       max_length=20, # Increased to 20 for safety
                       choices=CATEGORY_CHOICES,
                       default='jewelry',
                   )
    details = models.TextField(blank=True, null=True, 
                        help_text="Enter material, design, pattern, and care instructions."
                   )
    image        = models.ImageField(upload_to='images/')  # ImageField

    def __str__(self):
        return self.description
    
    @property
    def size_list(self):
        # Splits "S, M, L" into an actual Python list: ['S', 'M', 'L']
        if self.size:
            return [s.strip() for s in self.size.split(',') if s.strip()]
        return []
    

# ── Cart Models ────────────────────────────────────────────────────────

# 1. Cart MUST be defined before CartItem
class Cart(models.Model):
    # OneToOne ensures every user only has ONE active shopping cart
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        """Sum of all item subtotals in the cart."""
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"

# 2. CartItem uses the Cart defined above
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    elected_size = models.CharField(max_length=50, blank=True, null=True)

    # Because we have 4 different product tables, we make a ForeignKey for each, 
    # but set them to null=True so only one is filled out at a time!
    woman_item = models.ForeignKey(Women, on_delete=models.CASCADE, null=True, blank=True)
    man_item = models.ForeignKey(Men, on_delete=models.CASCADE, null=True, blank=True)
    kid_item = models.ForeignKey(Kids, on_delete=models.CASCADE, null=True, blank=True)
    accessory_item = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item(self):
        """Helper to quickly get whichever product is attached to this row."""
        return self.woman_item or self.man_item or self.kid_item or self.accessory_item

    @property
    def subtotal(self):
        """Calculates total price based on the attached item."""
        if self.item:
            return self.quantity * self.item.price
        return 0

# ── Favorite (Wishlist) Model ──────────────────────────────────────────

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    
    woman_item = models.ForeignKey(Women, on_delete=models.CASCADE, null=True, blank=True)
    man_item = models.ForeignKey(Men, on_delete=models.CASCADE, null=True, blank=True)
    kid_item = models.ForeignKey(Kids, on_delete=models.CASCADE, null=True, blank=True)
    accessory_item = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def item(self):
        """Returns the actual product object."""
        return self.woman_item or self.man_item or self.kid_item or self.accessory_item

    @property
    def item_type(self):
        """Returns the category string needed for our URLs."""
        if self.woman_item: return 'women'
        if self.man_item: return 'men'
        if self.kid_item: return 'kids'
        if self.accessory_item: return 'accessory'

    def __str__(self):
        return f"Favorite by {self.user.username}"