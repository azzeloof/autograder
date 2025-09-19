import json
from django.shortcuts import render
from django.http import request, JsonResponse
from .models import Assignment, TestFunction

def evaluate(request):
    if request.method == "GET":
        data = {"submit a POST request!"}
        return JsonResponse(data)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            assignment_post = data.get('assignment', None)
            function_post = data.get('function', None)
            arguments_post = data.get('arguments', None)
            if assignment_post is None or function_post is None:
                return JsonResponse({'error': 'assignment and function are required'}, status=400)
            try:
                with Assignment.objects.get(name=assignment_post) as assignment:
                    try:
                        with assignment.testfunction_set.get(name=function_post) as testfunction:
                            try:
                                args = arguments_post['args']
                                kwargs = arguments_post['kwargs']
                            except KeyError:
                                return JsonResponse({'error': 'malformed args or kwargs'}, status=400)
                            result = testfunction.evaluate(assignment, args, kwargs)
                    except TestFunction.MultipleObjectsReturned:
                        # This should not be allowed to happen
                        return JsonResponse({'error': 'TestFunction already exists'}, status=400)
                    except TestFunction.DoesNotExist:
                        return JsonResponse({'error': 'test function not found'}, status=404)
            except Assignment.MultipleObjectsReturned:
                # This should not be allowed to happen
                return JsonResponse({'error': 'multiple assignments with this name exist'}, status=400)
            except Assignment.DoesNotExist:
                return JsonResponse({'error': 'assignment not found'}, status=404)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"unhandled error": str(e)}, status=400)
    return None


