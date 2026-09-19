def repeat(n=2):
    def decorator(func):
        def wrapped_func(*args, **kargs):
            for _ in range(n):
                res += func(*args, **kargs)
            return res

        return wrapped_func

    return decorator


@repeat(n=10)
def f(a, b):
    return a + b


a = f(7, 5)
print(a)
