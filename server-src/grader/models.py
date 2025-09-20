from django.db import models
from django.http import JsonResponse
from importlib import import_module
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import guarded_iter_unpack_sequence

class Assignment(models.Model):
    name = models.CharField(max_length=100)     # assignment name (i.e "Week 1")

    def __str__(self):
        return self.name


class TestFunction(models.Model):
    name = models.CharField(max_length=100) # the name of the function
    function = models.TextField() # the actual function being evaluated
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) # the parent assignment
    grade = models.BooleanField(default=False, null=True) # whether requests should be graded/recorded, or simply responded to
    allowed_libraries = models.TextField(blank=True) # csv of library names, e.g "math, json, gravity"

    def __str__(self):
        return self.name

    def evaluate(self, args, kwargs):
        # note, not *args and **kwargs
        allowed_globals = safe_globals.copy()
        allowed_globals['_getiter_'] = default_guarded_getiter
        allowed_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
        for library in self.allowed_libraries.split(','):
            allowed_globals[library] = import_module(library)
        safe_locals = {}
        try:
            byte_code = compile_restricted(
                self.function,
                filename='<inline code>',
                mode='exec'
            )
        except SyntaxError as e:
            return JsonResponse({'Syntax error': str(e)}, status=400)
        except ImportError as e:
            return JsonResponse({'ImportError': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'Unhandled error': str(e)}, status=400)
        try:
            exec(byte_code, allowed_globals, safe_locals)
        except Exception as e:
            return JsonResponse({'Error defining function': str(e)}, status=400)
        try:
            args = args or []
            kwargs = kwargs or {}
            func_to_call = safe_locals.get(self.name)
            if not func_to_call:
                return JsonResponse({'No such function': self.name}, status=400)
            result = func_to_call(*args, **kwargs)
            print(result)
            return JsonResponse({'Result': result}, status=200)
        except Exception as e:
            return JsonResponse({'Error': e}, status=400)