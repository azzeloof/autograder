import signal
import logging
from django.db import models
from django.http import JsonResponse
from django.conf import settings
from importlib import import_module
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence

logger = logging.getLogger(__name__)

class TimeoutError(Exception):
    pass

def handler(signum, frame):
    raise TimeoutError("Function execution timed out")

signal.signal(signal.SIGALRM, handler)


class Assignment(models.Model):
    name = models.CharField(max_length=100, unique=True)     # assignment name (i.e "Week 1")

    def __str__(self):
        return self.name


class TestFunction(models.Model):
    name = models.CharField(max_length=100) # the name of the function
    function = models.TextField() # the actual function being evaluated
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) # the parent assignment
    grade = models.BooleanField(default=False, null=True) # whether requests should be graded/recorded, or simply responded to
    allowed_libraries = models.TextField(blank=True) # csv of library names, e.g "math, json, gravity"

    class Meta:
        unique_together = ('name', 'assignment')

    def __str__(self):
        return self.name

    def evaluate(self, args, kwargs):
        logger.info(f"Evaluating function {self.name} for assignment {self.assignment.name}")
        # note, not *args and **kwargs
        allowed_globals = safe_globals.copy()
        allowed_globals['_getiter_'] = default_guarded_getiter
        allowed_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        for library in self.allowed_libraries.split(','):
            logger.debug(f"Importing library: {library}")
            allowed_globals[library] = import_module(library)
        safe_locals = {}
        signal.alarm(settings.TIMEOUT_SECONDS) # Set a 5-second timeout
        try:
            logger.debug("Compiling restricted code")
            byte_code = compile_restricted(
                self.function,
                filename='<inline code>',
                mode='exec'
            )
            logger.debug("Executing restricted code")
            exec(byte_code, allowed_globals, safe_locals)
            args = args or []
            kwargs = kwargs or {}
            func_to_call = safe_locals.get(self.name)
            if not func_to_call:
                logger.warning(f"Function not found after execution: {self.name}")
                return JsonResponse({'No such function': self.name}, status=400)
            if not callable(func_to_call):
                logger.warning(f"Function not callable after execution: {self.name}")
                return JsonResponse({'Not a callable function': self.name}, status=400)
            logger.debug(f"Calling function {self.name} with args: {args} and kwargs: {kwargs}")
            result = func_to_call(*args, **kwargs)
            logger.info(f"Function {self.name} executed successfully with result: {result}")
            return JsonResponse({'Result': result}, status=200)
        except TimeoutError as e:
            logger.error(f"Function {self.name} timed out after {settings.TIMEOUT_SECONDS} seconds")
            return JsonResponse({'Error': str(e)}, status=400)
        except SyntaxError as e:
            logger.error(f"Syntax error in function {self.name}: {e}")
            return JsonResponse({'Syntax error': str(e)}, status=400)
        except ImportError as e:
            logger.error(f"Import error in function {self.name}: {e}")
            return JsonResponse({'ImportError': str(e)}, status=400)
        except Exception as e:
            logger.exception(f"Unhandled exception in function {self.name}")
            return JsonResponse({'Unhandled error': str(e)}, status=400)
        finally:
            signal.alarm(0) # Disable the alarm