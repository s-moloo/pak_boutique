from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Cart, CartItem, Women, Men, Kids, Accessory, Favorite
from .forms import WomenForm, MenForm, KidsForm, AccessoryForm, RegisterForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View 
from django.views.generic import ListView


# ── Public ─────────────────────────────────────────────────────────────────

class LandingView(TemplateView):
    template_name = 'boutique/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Changed [:4] to [:3] so it perfectly fills exactly one 3-column row!
        context['women'] = Women.objects.all().order_by('-id')[:3]
        context['men'] = Men.objects.all().order_by('-id')[:3]
        context['kids'] = Kids.objects.all().order_by('-id')[:3]
        context['accessories'] = Accessory.objects.all().order_by('-id')[:3]
        return context
    
# ── Auth ───────────────────────────────────────────────────────────────────
# LoginView and LogoutView are Django built-ins wired directly in urls.py.
# We only need RegisterView here.

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'boutique/auth/register.html'
    success_url = reverse_lazy('landing')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful. You are now logged in.')
        return response
    
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # This acts as a bouncer: Only return True if the user is an admin/staff
        return self.request.user.is_staff
    
# ── Women ──────────────────────────────────────────────────────────────────

class WomenListView(ListView):
    model = Women
    template_name = 'boutique/women_list.html'
    context_object_name = 'women'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(color__icontains=query) |
                Q(category__icontains=query)
            )
        return queryset
    
class WomenDetailView(DetailView):
    model = Women
    template_name = 'boutique/women_detail.html'
    context_object_name = 'woman' 

class WomenCreateView(AdminRequiredMixin, CreateView):
    model = Women
    form_class = WomenForm
    template_name = 'boutique/women_form.html'
    success_url = reverse_lazy('women_list')

class WomenUpdateView(AdminRequiredMixin, UpdateView):
    model = Women
    form_class = WomenForm
    template_name = 'boutique/women_form.html'
    success_url = reverse_lazy('women_list')

class WomenDeleteView(AdminRequiredMixin, DeleteView):
    model = Women
    template_name = 'boutique/women_confirm_delete.html'
    success_url = reverse_lazy('women_list') 

class WomenSearchView(LoginRequiredMixin, ListView):
     model               = Women
     template_name       = 'boutique/partials/women_table.html'
     context_object_name = 'womens'

class WomenInlineDeleteView(LoginRequiredMixin, DeleteView):
    """
    HTMX inline delete — returns an empty 200 response so HTMX removes the row.

    We override delete() instead of form_valid() because DeleteView calls
    get_success_url() before form_valid() runs, and with no success_url set
    it raises ImproperlyConfigured before we ever get a chance to return.
    """
    model = Women

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = str(self.object)      # capture before deletion
        self.object.delete()
        messages.error(request, f'{name} has been deleted.')
        return HttpResponse('')      # HTMX swaps this (empty) into the row


# ── Men ──────────────────────────────────────────────────────────────────
class MenListView(ListView):
    model = Men
    template_name = 'boutique/men_list.html'
    context_object_name = 'men'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(color__icontains=query) |
                Q(category__icontains=query)
            )
        return queryset
    
class MenDetailView(DetailView):
    model = Men
    template_name = 'boutique/men_detail.html'
    context_object_name = 'man'

class MenCreateView(AdminRequiredMixin, CreateView):
    model = Men
    form_class = MenForm
    template_name = 'boutique/men_form.html'
    success_url = reverse_lazy('men_list')

class MenUpdateView(AdminRequiredMixin, UpdateView):
    model = Men
    form_class = MenForm
    template_name = 'boutique/men_form.html'
    success_url = reverse_lazy('men_list')

class MenDeleteView(AdminRequiredMixin, DeleteView):
    model = Men
    template_name = 'boutique/men_confirm_delete.html'
    success_url = reverse_lazy('men_list')

class MenSearchView(LoginRequiredMixin, ListView):
     model               = Men
     template_name       = 'boutique/partials/men_table.html'
     context_object_name = 'mens'

class MenInlineDeleteView(LoginRequiredMixin, DeleteView):
    """
    HTMX inline delete — returns an empty 200 response so HTMX removes the row.

    We override delete() instead of form_valid() because DeleteView calls
    get_success_url() before form_valid() runs, and with no success_url set
    it raises ImproperlyConfigured before we ever get a chance to return.
    """
    model = Men

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = str(self.object)      # capture before deletion
        self.object.delete()
        messages.error(request, f'{name} has been deleted.')
        return HttpResponse('')      # HTMX swaps this (empty) into the row

# ── Kids ──────────────────────────────────────────────────────────────────
class KidsListView(ListView):
    model = Kids
    template_name = 'boutique/kids_list.html'
    context_object_name = 'kids'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(color__icontains=query) |
                Q(category__icontains=query)
            )
        return queryset 
    
class KidsDetailView(DetailView):
    model = Kids
    template_name = 'boutique/kids_detail.html'
    context_object_name = 'kid' 

class KidsCreateView(AdminRequiredMixin, CreateView):
    model = Kids
    form_class = KidsForm
    template_name = 'boutique/kids_form.html'
    success_url = reverse_lazy('kids_list')

class KidsUpdateView(AdminRequiredMixin, UpdateView):
    model = Kids
    form_class = KidsForm
    template_name = 'boutique/kids_form.html'
    success_url = reverse_lazy('kids_list')

class KidsDeleteView(AdminRequiredMixin, DeleteView):
    model = Kids
    template_name = 'boutique/kids_confirm_delete.html'
    success_url = reverse_lazy('women_list') 

class KidsSearchView(LoginRequiredMixin, ListView):
     model               = Kids
     template_name       = 'boutique/partials/kids_table.html'
     context_object_name = 'kids'

class KidsInlineDeleteView(LoginRequiredMixin, DeleteView):
    """
    HTMX inline delete — returns an empty 200 response so HTMX removes the row.

    We override delete() instead of form_valid() because DeleteView calls
    get_success_url() before form_valid() runs, and with no success_url set
    it raises ImproperlyConfigured before we ever get a chance to return.
    """
    model = Kids

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = str(self.object)      # capture before deletion
        self.object.delete()
        messages.error(request, f'{name} has been deleted.')
        return HttpResponse('')      # HTMX swaps this (empty) into the row

# ── Accessory ───────────────────────────────────────────────────────────────
class AccessoryListView(ListView):
    model = Accessory
    template_name = 'boutique/accessory_list.html'
    context_object_name = 'accessories'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(color__icontains=query) |
                Q(category__icontains=query)
            )
        return queryset 
    
class AccessoryDetailView(DetailView):
    model = Accessory
    template_name = 'boutique/accessory_detail.html'
    context_object_name = 'accessory' 

class AccessoryCreateView(AdminRequiredMixin, CreateView):
    model = Accessory
    form_class = AccessoryForm
    template_name = 'boutique/accessory_form.html'
    success_url = reverse_lazy('accessory_list')

class AccessoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Accessory
    form_class = AccessoryForm
    template_name = 'boutique/accessory_form.html'
    success_url = reverse_lazy('accessory_list')

class AccessoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Accessory
    template_name = 'boutique/accessory_confirm_delete.html'
    success_url = reverse_lazy('women_list')
class AccessorySearchView(LoginRequiredMixin, ListView):
     model               = Accessory
     template_name       = 'boutique/partials/accessory_table.html'
     context_object_name = 'accessory'

class AccessoryInlineDeleteView(LoginRequiredMixin, DeleteView):
    """
    HTMX inline delete — returns an empty 200 response so HTMX removes the row.

    We override delete() instead of form_valid() because DeleteView calls
    get_success_url() before form_valid() runs, and with no success_url set
    it raises ImproperlyConfigured before we ever get a chance to return.
    """
    model = Accessory

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = str(self.object)      # capture before deletion
        self.object.delete()
        messages.error(request, f'{name} has been deleted.')
        return HttpResponse('')      # HTMX swaps this (empty) into the row

# ── Cart Logic ─────────────────────────────────────────────────────────────

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, category, item_id, *args, **kwargs):
        # 1. Get the current user's cart (or create one if it's their first time)
        cart, created = Cart.objects.get_or_create(user=request.user)

        # 2. Figure out which item they are trying to add based on the URL
        cart_item_kwargs = {'cart': cart}

        if category == 'women':
            item = get_object_or_404(Women, pk=item_id)
            cart_item_kwargs['woman_item'] = item
        elif category == 'men':
            item = get_object_or_404(Men, pk=item_id)
            cart_item_kwargs['man_item'] = item
        elif category == 'kids':
            item = get_object_or_404(Kids, pk=item_id)
            cart_item_kwargs['kid_item'] = item
        elif category == 'accessory':
            item = get_object_or_404(Accessory, pk=item_id)
            cart_item_kwargs['accessory_item'] = item
        else:
            messages.error(request, "Invalid category.")
            return redirect(request.META.get('HTTP_REFERER', 'landing'))

        # 3. Check if this exact item is ALREADY in their cart
        cart_item, created = CartItem.objects.get_or_create(**cart_item_kwargs)

        if not created:
            # If it was already in the cart, just increase the quantity!
            cart_item.quantity += 1
            cart_item.save()

        # 4. Show a success toast message
        messages.success(request, f"Added {item.description} to your cart!")

        # 5. Redirect the user right back to the page they clicked the button on!
        return redirect(request.META.get('HTTP_REFERER', 'landing'))

# ── Customer Views (Only sees their own stuff) ─────────────────────────

class CustomerCartView(LoginRequiredMixin, ListView):
    template_name = 'boutique/cart_customer.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # 1. Get or create the cart for THIS specific user
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        # 2. Return only the items in this cart
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the cart itself to the template so we can show the Total
        context['cart'], _ = Cart.objects.get_or_create(user=self.request.user)
        return context
    
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, category, item_id, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item_kwargs = {'cart': cart}
        
        if category == 'women':
            cart_item_kwargs['woman_item_id'] = item_id
        elif category == 'men':
            cart_item_kwargs['man_item_id'] = item_id
        elif category == 'kids':
            cart_item_kwargs['kid_item_id'] = item_id
        elif category == 'accessory':
            cart_item_kwargs['accessory_item_id'] = item_id
        else:
            return HttpResponse("Invalid category", status=400)
            
        # Get the item if it's already in the cart, otherwise create it
        cart_item, item_created = CartItem.objects.get_or_create(**cart_item_kwargs)
        
        if not item_created:
            # If it was already in the cart, just increase the quantity
            cart_item.quantity += 1
            cart_item.save()
            
        messages.success(request, "Item added to your basket!")
        # Redirect the user right back to the page they clicked the button on
        return redirect(request.META.get('HTTP_REFERER', 'landing'))
    
# Make sure you have this import at the top if you don't already:
# from django.shortcuts import get_object_or_404, redirect

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        # Find the specific item in THIS user's cart
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        # Get the new quantity from the form input
        new_quantity = request.POST.get('quantity')
        
        if new_quantity and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Quantity must be at least 1.")
            
        return redirect('customer_cart')

class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        # Find the specific item in THIS user's cart
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        # Delete it from the database
        cart_item.delete()
        messages.info(request, "Item removed from your cart.")
        
        return redirect('customer_cart')
    
from django.views.generic import ListView

class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = 'boutique/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        # Fetch only the favorites belonging to this specific user
        return Favorite.objects.filter(user=self.request.user)
    
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, category, item_id, *args, **kwargs):
        fav_kwargs = {'user': request.user}

        if category == 'women':
            fav_kwargs['woman_item_id'] = item_id
        elif category == 'men':
            fav_kwargs['man_item_id'] = item_id
        elif category == 'kids':
            fav_kwargs['kid_item_id'] = item_id
        elif category == 'accessory':
            fav_kwargs['accessory_item_id'] = item_id
        else:
            return HttpResponse("Invalid category", status=400)

        # Check if the user already favorited this item
        existing_favorite = Favorite.objects.filter(**fav_kwargs).first()

        if existing_favorite:
            existing_favorite.delete()
            messages.info(request, "Removed from your wishlist.")
        else:
            Favorite.objects.create(**fav_kwargs)
            messages.success(request, "Added to your wishlist!")

        return redirect(request.META.get('HTTP_REFERER', 'landing'))
    
class MoveFavoriteToCartView(LoginRequiredMixin, View):
    def post(self, request, favorite_id, *args, **kwargs):
        # 1. Grab the specific favorite record (Ensure it belongs to this user!)
        favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
        
        # 2. Get or create the user's shopping cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # 3. Figure out which item was in the favorite to add to the cart
        cart_item_kwargs = {'cart': cart}
        if favorite.woman_item:
            cart_item_kwargs['woman_item'] = favorite.woman_item
        elif favorite.man_item:
            cart_item_kwargs['man_item'] = favorite.man_item
        elif favorite.kid_item:
            cart_item_kwargs['kid_item'] = favorite.kid_item
        elif favorite.accessory_item:
            cart_item_kwargs['accessory_item'] = favorite.accessory_item
            
        # 4. Add it to the cart (or increase quantity if already there)
        cart_item, item_created = CartItem.objects.get_or_create(**cart_item_kwargs)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
        # 5. Delete it from the Favorites list
        item_name = favorite.item.description
        favorite.delete()
        
        messages.success(request, f"Moved {item_name} to your basket!")
        return redirect('favorites_list')

# ── Admin Views (Sees everything) ──────────────────────────────────────

class AdminCartListView(LoginRequiredMixin, ListView):
    # LoginRequiredMixin ensures normal users get blocked!
    model = Cart
    template_name = 'boutique/cart_admin.html'
    context_object_name = 'carts'
    # By default, ListView does Cart.objects.all(), so it fetches everyone's carts!

