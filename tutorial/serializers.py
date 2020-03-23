"""
We need to provide a way of serializing and deserializing the snippet instances into representations such as json.
We can do this by declaring serializers that work very similar to Django's forms.
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer to create representations of the users
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class SnippetSerializer(serializers.ModelSerializer):
    """
    The first part of the serializer class defines the fields that get serialized/deserialized. The create() and
    update() methods define how fully fledged instances are created or modified when calling serializer.save()
    """
    # This would be how we would write the fields if we were using Serializer
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # # Equivalent to using widget=widgets.Textarea on a Django Form class
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # The REST framework has ModelSerializer, which avoids us having to repeat code that is already in the model
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'lineons', 'language', 'style']

    def create(self, validated_data):
        """
        Create and return a new 'Snippet' instance, given the validated data
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return existing 'Snippet' instance, given the validated data
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        # Save the instance and return it
        instance.save()
        return instance
