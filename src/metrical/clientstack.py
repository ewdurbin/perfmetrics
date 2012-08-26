
import threading


class ClientStack(threading.local):
    """Thread local stack of statsd clients.

    Applications and tests can either set the global statsd client using
    set_statsd_client() or set a statsd client for each thread
    using statsd_client_stack.push()/.pop().

    This is like pyramid.threadlocal but it handles the default differently.
    """

    default = None

    def __init__(self):
        self.stack = stack = []

        # Optimization: this closure is faster than a method. ;-)
        def get():
            return stack[-1] if stack else self.default

        self.get = get

    def push(self, obj):
        self.stack.append(obj)

    def pop(self):
        stack = self.stack
        if stack:
            return stack.pop()

    def clear(self):
        del self.stack[:]


client_stack = ClientStack()