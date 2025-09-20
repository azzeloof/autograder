import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assignment, TestFunction

def index(request):
    return render(request, 'grader/index.html')

@csrf_exempt
def evaluate(request):
    if request.method == "GET":
        data = {"submit a POST request!"}
        return JsonResponse(data)
    elif request.method == "POST":
        try:
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)
            data = json.loads(request.body)
            assignment_post = data.get('assignment', None)
            function_post = data.get('function', None)
            args = data.get('args', None)
            kwargs = data.get('kwargs', None)
            if assignment_post is None or function_post is None:
                return JsonResponse({'error': 'assignment and function are required'}, status=400)
            if not isinstance(assignment_post, str) or not isinstance(function_post, str):
                return JsonResponse({'error': 'assignment and function must be strings'}, status=400)
            if args is not None and not isinstance(args, list):
                return JsonResponse({'error': 'args must be a list'}, status=400)
            if kwargs is not None and not isinstance(kwargs, dict):
                return JsonResponse({'error': 'kwargs must be a dict'}, status=400)
            try:
                assignment = Assignment.objects.get(name=assignment_post)
                try:
                    testfunction = TestFunction.objects.get(name=function_post, assignment=assignment)
                    result = testfunction.evaluate(args, kwargs)
                    return result
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


