import ast

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Operation
from core.serializers import OperationSerializer


class OperationList(APIView):
    @staticmethod
    def is_valid_python(code):
        try:
            ast.parse(code)
        except SyntaxError:
            return False
        return True

    def get(self, request):
        operations = Operation.objects.all()
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not self.is_valid_python(request.data.get('operation_code')):
            return Response({'error': 'Please check the submitted code'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationDetail(APIView):
    """
    Retrieve, update or delete a operation instance.
    """

    @staticmethod
    def get_object(pk):
        try:
            return Operation.objects.get(pk=pk)
        except Operation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        operation = self.get_object(pk)
        serializer = OperationSerializer(operation)
        return Response(serializer.data)

    def put(self, request, pk):
        operation = self.get_object(pk)
        serializer = OperationSerializer(operation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = self.get_object(pk)
        operation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExecuteOperation(APIView):
    def post(self, request):
        print(request.data)
        operation_id = request.data.get('id')
        args = request.data.get('args', None)

        if operation_id is None:
            return Response({'error': 'Missing Operation ID!'}, status=status.HTTP_400_BAD_REQUEST)
        if args is None:
            return Response({'error': 'Missing Arguments!'}, status=status.HTTP_400_BAD_REQUEST)

        print(args)
        operation = Operation.objects.get(id=operation_id)
        # code = 'def factorial(args):\n\tprint(args[0], "Working")\n\treturn args[0]\nprint(args[0])\nresult=100'
        # code = 'def par():\n\tdef op(n):\n\t\treturn 1 if (n==1 or n==0) else n * op(n - 1)\n\treturn op(4)'
        # code = 'def op(args):\n\treturn args[0] + args[1]'
        loc = {}
        exec(operation.operation_code, {}, loc)
        print(operation.operation_code)
        print(loc)
        op = loc['op']

        return Response({'result': op(args)})
