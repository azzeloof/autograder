import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assignment, TestFunction
from django_ratelimit.decorators import ratelimit
from django.conf import settings

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'grader/index.html')

@csrf_exempt
@ratelimit(key='ip', rate=settings.RATE_LIMIT, block=True)
def evaluate(request):
    if request.method == "GET":
        data = {"submit a POST request!"}
        return JsonResponse(data)
    elif request.method == "POST":
        logger.info(f"Received evaluation request from {request.META.get('REMOTE_ADDR')}")
        try:
            if not request.body:
                logger.warning("Empty request body")
                return JsonResponse({'error': 'Empty request body'}, status=400)
            data = json.loads(request.body)
            assignment_post = data.get('assignment', None)
            function_post = data.get('function', None)
            args = data.get('args', None)
            kwargs = data.get('kwargs', None)
            if assignment_post is None or function_post is None:
                logger.warning("Missing assignment or function in request")
                return JsonResponse({'error': 'assignment and function are required'}, status=400)
            if not isinstance(assignment_post, str) or not isinstance(function_post, str):
                logger.warning("Invalid type for assignment or function")
                return JsonResponse({'error': 'assignment and function must be strings'}, status=400)
            if args is not None and not isinstance(args, list):
                logger.warning("Invalid type for args")
                return JsonResponse({'error': 'args must be a list'}, status=400)
            if kwargs is not None and not isinstance(kwargs, dict):
                logger.warning("Invalid type for kwargs")
                return JsonResponse({'error': 'kwargs must be a dict'}, status=400)
            try:
                assignment = Assignment.objects.get(name=assignment_post)
                try:
                    testfunction = TestFunction.objects.get(name=function_post, assignment=assignment)
                    logger.info(f"Evaluating {function_post} for assignment {assignment_post}")
                    result = testfunction.evaluate(args, kwargs)
                    logger.info(f"Evaluation successful for {function_post}")
                    return result
                except TestFunction.MultipleObjectsReturned:
                    logger.error(f"Multiple test functions found for {function_post}")
                    return JsonResponse({'error': 'TestFunction already exists'}, status=400)
                except TestFunction.DoesNotExist:
                    logger.warning(f"Test function not found: {function_post}")
                    return JsonResponse({'error': 'test function not found'}, status=404)
            except Assignment.MultipleObjectsReturned:
                logger.error(f"Multiple assignments found for {assignment_post}")
                return JsonResponse({'error': 'multiple assignments with this name exist'}, status=400)
            except Assignment.DoesNotExist:
                logger.warning(f"Assignment not found: {assignment_post}")
                return JsonResponse({'error': 'assignment not found'}, status=404)
        except json.decoder.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.exception(f"Unhandled exception in evaluate view: {e}")
            return JsonResponse({"unhandled error": str(e)}, status=400)
    return None


