from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from tutorial.models import Snippet
from tutorial.serializers import SnippetSerializer


# Create your views here.
@csrf_exempt
def snippet_list(request):
    """
        List all code snippets, or create a new snippet.
        """
    # LIST ALL
    if request.method == 'GET':
        # Get the snippets from the Snippets model
        snippets = Snippet.objects.all()
        # Serialize the snippets using many=True to specify multiple snippets
        serializer = SnippetSerializer(snippets, many=True)
        # Return them as a JSON response
        return JsonResponse(serializer.data, safe=False)

    # CREATE
    elif request.method == 'POST':
        # Deserialize the request
        data = JSONParser().parse(request)
        # Restore the native datatype into a fully populated object instance
        serializer = SnippetSerializer(data=data)
        # Save the object instance if it's valid
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # Return an error if it isn't valid
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # Get the snippet by the pk
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # Return error if it doesn't exist
        return HttpResponse(status=404)

    # RETRIEVE
    if request.method == 'GET':
        # Serialize the snippet and return it as a JSON response if we want to retrieve it
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    # UPDATE
    elif request.method == 'PUT':
        # Deserialize the request
        data = JSONParser().parse(request)
        # Restore the native datatype into a fully populated object instance
        serializer = SnippetSerializer(snippet, data=data)
        # Save the object instance if it's valid
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # Return an error if it isn't valid
        return JsonResponse(serializer.errors, status=400)

    # DELETE
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
