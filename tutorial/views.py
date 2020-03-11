# ------------------------------ CLASS-BASED VIEWS ------------------------------ #
from tutorial.models import Snippet
from tutorial.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # We don't have to declare the type of request (GET, POST). Instead, we specify it in a function and we
    # declare the format as none in the function. This helps us to have more cleary defined request method handlers
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USING MIXINS
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics
#
#
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# GENERIC CLASS BASED VIEW
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import generics
#
#
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    # First we get the snippet object
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            # Raise an erorr if there is no snippet
            raise Http404

    def get(self, request, pk, format=None):
        # Save the relevant snippet in a variable
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# USING MIXINS
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# GENERIC CLASS BASED VIEW
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# ------------------------------ FUNCTION-BASED VIEWS ------------------------------ #
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from tutorial.models import Snippet
# from tutorial.serializers import SnippetSerializer
#
#
# # Create your views here.
# # This decorator provides a few bits of functionality such as making sure you receive Request instances in your view,
# # and adding context to Response objects so that content negotiation can be performed
# # It also provides behaviour such as returning 405 Method Not Allowed responses when appropriate, and handling any
# # ParseError exceptions that occur when accessing request.data with malformed input.
# @api_view(['GET', 'POST'])
# # Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to
# # handle URLs
# def snippet_list(request, format=None):
#     """
#         List all code snippets, or create a new snippet.
#     """
#     # LIST ALL
#     if request.method == 'GET':
#         # Get the snippets from the Snippets model
#         snippets = Snippet.objects.all()
#         # Serialize the snippets using many=True to specify multiple snippets
#         serializer = SnippetSerializer(snippets, many=True)
#         # Return the serialized snippets - the api_view decorator allows us to use Response instead of JsonResponse
#         # It automatically retrieves the response in the relevant data format
#         return Response(serializer.data)
#
#     # CREATE
#     elif request.method == 'POST':
#         # Deserialize the request - we don't need to use this when using the @api_view decorator
#         # data = JSONParser().parse(request)
#         # Restore the native datatype into a fully populated object instance
#         serializer = SnippetSerializer(data=request.data)
#         # Save the object instance if it's valid
#         if serializer.is_valid():
#             serializer.save()
#             # Instead of specifying the actional status code, we use the REST framework's named status codes
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # Return an error if it isn't valid
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         # Get the snippet by the pk
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         # Return error if it doesn't exist - we don't need to use HttpResponse, as api_view handles it for us
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # RETRIEVE
#     if request.method == 'GET':
#         # Serialize the snippet and return it as a JSON response if we want to retrieve it
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     # UPDATE
#     elif request.method == 'PUT':
#         # Deserialize the request - again, we don't need to do this, as api_view handles it for us
#         # data = JSONParser().parse(request)
#         # Restore the native datatype into a fully populated object instance
#         serializer = SnippetSerializer(snippet, data=request.data)
#         # Save the object instance if it's valid
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         # Return an error if it isn't valid
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # DELETE
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
