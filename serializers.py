from rest_framework import serializers
from .models import Board, Column, Card
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CardSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Card
        fields = ['id', 'column', 'title', 'description', 'position', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    cards_count = serializers.IntegerField(source='cards.count', read_only=True)
    
    class Meta:
        model = Column
        fields = ['id', 'board', 'name', 'position', 'color', 'cards', 'cards_count']


class ColumnListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar columnas sin las tarjetas"""
    cards_count = serializers.IntegerField(source='cards.count', read_only=True)
    
    class Meta:
        model = Column
        fields = ['id', 'board', 'name', 'position', 'color', 'cards_count']


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnListSerializer(many=True, read_only=True)
    total_cards = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'columns', 'total_cards']
        read_only_fields = ['created_at']
    
    def get_total_cards(self, obj):
        return obj.get_total_cards()


class BoardDetailSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    total_cards = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'columns', 'total_cards']
        read_only_fields = ['created_at']
    
    def get_total_cards(self, obj):
        return obj.get_total_cards()


class MoveCardSerializer(serializers.Serializer):
    column_id = serializers.IntegerField()
    position = serializers.IntegerField(min_value=0)
