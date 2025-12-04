from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Board, Column, Card
from .serializers import (
    BoardSerializer, BoardDetailSerializer,
    ColumnSerializer, ColumnListSerializer,
    CardSerializer, MoveCardSerializer
)
from .permissions import IsAdminOrReadOnly


class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar tableros Kanban.
    
    list: Listar todos los tableros (todos los usuarios)
    create: Crear un nuevo tablero (solo admins)
    retrieve: Obtener detalles de un tablero específico (todos los usuarios)
    update: Actualizar un tablero (solo admins)
    partial_update: Actualizar parcialmente un tablero (solo admins)
    destroy: Eliminar un tablero (solo admins)
    """
    queryset = Board.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer
    
    def get_queryset(self):
        return Board.objects.prefetch_related('columns__cards')


class ColumnViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar columnas.
    
    list: Listar todas las columnas (todos los usuarios)
    create: Crear una nueva columna (solo admins)
    retrieve: Obtener detalles de una columna específica (todos los usuarios)
    update: Actualizar una columna (solo admins)
    partial_update: Actualizar parcialmente una columna (solo admins)
    destroy: Eliminar una columna (solo admins)
    """
    queryset = Column.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ColumnSerializer
        return ColumnListSerializer
    
    def get_queryset(self):
        queryset = Column.objects.all()
        board_id = self.request.query_params.get('board', None)
        if board_id is not None:
            queryset = queryset.filter(board_id=board_id)
        return queryset.prefetch_related('cards')


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar tarjetas.
    
    list: Listar todas las tarjetas (todos los usuarios)
    create: Crear una nueva tarjeta (solo admins)
    retrieve: Obtener detalles de una tarjeta específica (todos los usuarios)
    update: Actualizar una tarjeta (solo admins)
    partial_update: Actualizar parcialmente una tarjeta (solo admins)
    destroy: Eliminar una tarjeta (solo admins)
    move: Mover una tarjeta a otra columna/posición (solo admins)
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = Card.objects.select_related('column', 'created_by')
        column_id = self.request.query_params.get('column', None)
        if column_id is not None:
            queryset = queryset.filter(column_id=column_id)
        return queryset
    
    def perform_create(self, serializer):
        # Asignar automáticamente el usuario actual como creador
        serializer.save(created_by=self.request.user)
    
    def perform_destroy(self, instance):
        column = instance.column
        instance.delete()
        
        # Reordenar las tarjetas restantes
        cards = Card.objects.filter(column=column).order_by('position')
        for idx, card in enumerate(cards):
            if card.position != idx:
                card.position = idx
                card.save()
    
    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Mover una tarjeta a otra columna o posición.
        
        POST /api/cards/{id}/move/
        Body: {"column_id": 2, "position": 0}
        """
        card = self.get_object()
        serializer = MoveCardSerializer(data=request.data)
        
        if serializer.is_valid():
            column_id = serializer.validated_data['column_id']
            new_position = serializer.validated_data['position']
            
            new_column = get_object_or_404(Column, id=column_id)
            
            # Actualizar la tarjeta
            card.column = new_column
            card.position = new_position
            card.save()
            
            # Reordenar tarjetas en la nueva columna
            cards = Card.objects.filter(column=new_column).order_by('position')
            for idx, c in enumerate(cards):
                if c.position != idx:
                    c.position = idx
                    c.save()
            
            return Response({
                'status': 'success',
                'message': 'Tarjeta movida correctamente',
                'card': CardSerializer(card).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
