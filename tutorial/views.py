from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tutorial.models import Snippet
from tutorial.serializers import SnippetSerializer


# Create your views here.
# This decoratpr provides a few bits of functionality such as making sure you receive Request instances in your view,
# and adding context to Response objects so that content negotiation can be performed
# It also provides behaviour such as returning 405 Method Not Allowed responses when appropriate, and handling any
# ParseError exceptions that occur when accessing request.data with malformed input.
@api_view(['GET', 'POST'])
# Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to
# handle URLs
def snippet_list(request, format=None):
    """
        List all code snippets, or create a new snippet.
        """
    # LIST ALL
    if request.method == 'GET':
        # Get the snippets from the Snippets model
        snippets = Snippet.objects.all()
        # Serialize the snippets using many=True to specify multiple snippets
        serializer = SnippetSerializer(snippets, many=True)
        # Return the serialized snippets - the api_view decorator allows us to use Response instead of JsonResponse
        # It automatically retrieves the response in the relevant data format
        return Response(serializer.data)

    # CREATE
    elif request.method == 'POST':
        # Deserialize the request - we don't need to use this when using the @api_view decorator
        # data = JSONParser().parse(request)
        # Restore the native datatype into a fully populated object instance
        serializer = SnippetSerializer(data=request.data)
        # Save the object instance if it's valid
        if serializer.is_valid():
            serializer.save()
            # Instead of specifying the actional status code, we use the REST framework's named status codes
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return an error if it isn't valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # Get the snippet by the pk
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # Return error if it doesn't exist - we don't need to use HttpResponse, as api_view handles it for us
        return Response(status=status.HTTP_404_NOT_FOUND)

    # RETRIEVE
    if request.method == 'GET':
        # Serialize the snippet and return it as a JSON response if we want to retrieve it
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    # UPDATE
    elif request.method == 'PUT':
        # Deserialize the request - again, we don't need to do this, as api_view handles it for us
        # data = JSONParser().parse(request)
        # Restore the native datatype into a fully populated object instance
        serializer = SnippetSerializer(snippet, data=request.data)
        # Save the object instance if it's valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # Return an error if it isn't valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
