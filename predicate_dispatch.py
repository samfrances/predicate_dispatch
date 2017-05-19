from functools import wraps, update_wrapper

class MultiMethod(object):

    def __init__(self, default):
        self.default = default
        self.methods = []

        @wraps(self.default)
        def wrapper(*args):
            return self(*args)

        def when(*predicates):
            return When(multi=self, predicates=predicates, decorator_returns=wrapper)

        wrapper.when = when

        self.wrapper = wrapper

    def when(self, *predicates):
        return When(mutli=self, predicates=predicates, decorator_returns=self)

    def __call__(self, *args):
        for predicates, func in self.methods:
            if all(predicate(arg) for predicate, arg in zip(predicates, args)):
                return func(*args)
        return self.default(*args)

class When(object):

    def __init__(self, multi, predicates, decorator_returns):
        self.multi = multi
        self.predicates = predicates
        self.decorator_returns = decorator_returns

    def __call__(self, func_or_val):

        if not callable(func_or_val):
            func = lambda *args: func_or_val
        else:
            func = func_or_val

        self.multi.methods.append(
            (self.predicates, func)
        )
        return self.decorator_returns

    def then(self, func_or_val):
        return self(func_or_val)

def multi(func):
    return MultiMethod(func).wrapper

def when(multimethod, *predicates):
    return multimethod.when(*predicates)

if __name__ == "__main__":

    @multi
    def kitkat(n):
        """Kitkat function"""
        return str(n)

    @kitkat.when(lambda x: x % 3 == 0 and x % 5 == 0)
    def kitkat(n):
        return "kitkat"

    kitkat.when(lambda x: x % 3 == 0).then("kit")

    when(kitkat, lambda x: x % 5 == 0)("kat")
