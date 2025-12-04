from django.urls import path
from .views import (
    BoardListView, BoardDetailView,
    create_card, update_card, move_card, delete_card,
    login_view, register_view, logout_view
)

app_name = 'kanban'

urlpatterns = [
    # Authentication
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Boards
    path('', BoardListView.as_view(), name='board_list'),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    
    # API endpoints
    path('api/board/<int:board_id>/card/create/', create_card, name='create_card'),
    path('api/card/<int:card_id>/update/', update_card, name='update_card'),
    path('api/card/<int:card_id>/move/', move_card, name='move_card'),
    path('api/card/<int:card_id>/delete/', delete_card, name='delete_card'),
]
