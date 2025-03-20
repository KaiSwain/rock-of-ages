from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rockapi.models import Rock
from rockapi.models import Type
from django.contrib.auth.models import User

class RockView(ViewSet):
    """Rock view set"""


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        chosen_type = Type.objects.get(pk=request.data['typeId'])
        rock = Rock()
        rock.user = request.auth.user
        rock.weight = request.data['weight']
        rock.name = request.data['name']
        rock.type = chosen_type
        rock.save()

        serialized = RockSerializer(rock, many = False)

        # You will implement this feature in a future chapter
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            rocks = Rock.objects.all()
            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RockOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name')

class RockTypeSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Type
        fields = ( 'label', )

class RockSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    type = RockTypeSerializer(many=False)
    user = RockOwnerSerializer(many = False)

    class Meta:
        model = Rock
        fields = ( 'id', 'name', 'weight', 'user', 'type' )
