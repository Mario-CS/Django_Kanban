from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import json
from .models import Board, Column, Card
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class BoardListView(LoginRequiredMixin, ListView):
    login_url = 'kanban:login'
    model = Board
    template_name = 'kanban/board_list.html'
    context_object_name = 'boards'


class BoardDetailView(LoginRequiredMixin, DetailView):
    login_url = 'kanban:login'
    model = Board
    template_name = 'kanban/kanban_board.html'
    context_object_name = 'board'

    def get_queryset(self):
        return Board.objects.prefetch_related('columns__cards')


@require_http_methods(["POST"])
@login_required
def create_card(request, board_id):
    try:
        data = json.loads(request.body)
        column = get_object_or_404(Column, id=data['column_id'], board_id=board_id)
        
        # Get highest position
        max_pos = Card.objects.filter(column=column).count()
        
        card = Card.objects.create(
            column=column,
            title=data.get('title', 'New Task'),
            description=data.get('description', ''),
            position=max_pos,
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'card': {
                'id': card.id,
                'title': card.title,
                'description': card.description,
                'position': card.position,
                'created_by': request.user.username
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["PUT"])
@login_required
def update_card(request, card_id):
    try:
        card = get_object_or_404(Card, id=card_id)
        data = json.loads(request.body)
        
        if 'title' in data:
            card.title = data['title']
        if 'description' in data:
            card.description = data['description']
        
        card.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
@login_required
def move_card(request, card_id):
    try:
        card = get_object_or_404(Card, id=card_id)
        data = json.loads(request.body)
        
        new_column = get_object_or_404(Column, id=data['column_id'])
        new_position = data.get('position', 0)
        
        # Update column and position
        card.column = new_column
        card.position = new_position
        card.save()
        
        # Reorder cards in the new column
        cards = Card.objects.filter(column=new_column).order_by('position')
        for idx, c in enumerate(cards):
            if c.position != idx:
                c.position = idx
                c.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
@login_required
def delete_card(request, card_id):
    try:
        card = get_object_or_404(Card, id=card_id)
        column = card.column
        card.delete()
        
        # Reorder remaining cards
        cards = Card.objects.filter(column=column).order_by('position')
        for idx, c in enumerate(cards):
            c.position = idx
            c.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('kanban:board_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # El mensaje de bienvenida se muestra en board_list, no aquí
                return redirect('kanban:board_list')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'kanban/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('kanban:board_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # El mensaje se muestra en board_list
            return redirect('kanban:board_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'kanban/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('kanban:login')
