from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # ── Public / Landing ───────────────────────────────────────────────────
    path('', views.LandingView.as_view(), name='landing'),

    # ── Auth ───────────────────────────────────────────────────────────────
    path('login/', LoginView.as_view(template_name='boutique/auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # ── Women ──────────────────────────────────────────────────────────────
    path('women/', views.WomenListView.as_view(), name='women_list'),
    path('women/<int:pk>/', views.WomenDetailView.as_view(), name='women_detail'),
    path('women/add/', views.WomenCreateView.as_view(), name='women_create'),
    path('women/<int:pk>/edit/', views.WomenUpdateView.as_view(), name='women_update'),
    path('women/<int:pk>/delete/', views.WomenDeleteView.as_view(), name='women_delete'),

    # ── Men ────────────────────────────────────────────────────────────────
    path('men/', views.MenListView.as_view(), name='men_list'),
    path('men/<int:pk>/', views.MenDetailView.as_view(), name='men_detail'),
    path('men/add/', views.MenCreateView.as_view(), name='men_create'),
    path('men/<int:pk>/edit/', views.MenUpdateView.as_view(), name='men_update'),
    path('men/<int:pk>/delete/', views.MenDeleteView.as_view(), name='men_delete'),

    # ── Kids ───────────────────────────────────────────────────────────────
    path('kids/', views.KidsListView.as_view(), name='kids_list'),
    path('kids/<int:pk>/', views.KidsDetailView.as_view(), name='kids_detail'),
    path('kids/add/', views.KidsCreateView.as_view(), name='kids_create'),
    path('kids/<int:pk>/edit/', views.KidsUpdateView.as_view(), name='kids_update'),
    path('kids/<int:pk>/delete/', views.KidsDeleteView.as_view(), name='kids_delete'),

    # ── Accessories ────────────────────────────────────────────────────────
    path('accessories/', views.AccessoryListView.as_view(), name='accessory_list'),
    path('accessories/<int:pk>/', views.AccessoryDetailView.as_view(), name='accessory_detail'),
    path('accessories/add/', views.AccessoryCreateView.as_view(), name='accessory_create'),
    path('accessories/<int:pk>/edit/', views.AccessoryUpdateView.as_view(), name='accessory_update'),
    path('accessories/<int:pk>/delete/', views.AccessoryDeleteView.as_view(), name='accessory_delete'),

    path('cart/add/<str:category>/<int:item_id>/', views.AddToCartView.as_view(), name='add_to_cart'),

    # ── Cart & Favorites ───────────────────────────────────────────────────
    path('cart/', views.CustomerCartView.as_view(), name='customer_cart'),
    path('manage/carts/', views.AdminCartListView.as_view(), name='admin_carts'),
    path('cart/add/<str:category>/<int:item_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    
    # Add these two lines under your other cart paths:
    path('cart/item/<int:item_id>/update/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.RemoveCartItemView.as_view(), name='remove_cart_item'),
    
    # MAKE SURE THIS EXACT LINE EXISTS:
    path('favorite/toggle/<str:category>/<int:item_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    
    # Add this line:
    path('favorites/', views.FavoriteListView.as_view(), name='favorites_list'),

    # Add this line right next to your toggle_favorite path:
    path('favorite/move-to-cart/<int:favorite_id>/', views.MoveFavoriteToCartView.as_view(), name='move_favorite_to_cart'),
]