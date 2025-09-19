from django.db import models
from django.http import JsonResponse

class Assignment(models.Model):
    name = models.CharField(max_length=100)     # assignment name (i.e "Week 1")

    def __str__(self):
        return self.name


class TestFunction(models.Model):
    name = models.CharField(max_length=100) # the name of the function
    function = models.TextField() # the actual function being evaluated
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) # the parent assignment
    grade = models.BooleanField(default=False, null=True) # whether requests should be graded/recorded, or simply responded to

    def __str__(self):
        return self.name

    def evaluate(self, args, kwargs):
        # note, not *args and **kwargs
        try:
            # oohhhh big scary exec()
            exec(self.function)
            passed_args = ""
            if args is not None:
                for arg in args:
                    passed_args += f"{str(arg)}, "
            if kwargs is not None:
                for key, value in kwargs.items():
                    passed_args += f"{key}={value}, "
            passed_args = passed_args.strip()
            passed_args = passed_args.strip(",")
            try:
                return eval(f"{self.name}({passed_args})")
            except Exception as e:
                return JsonResponse({'error': e}, status=400)
        except Exception as e:
            return JsonResponse({'error': e}, status=400)