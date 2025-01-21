import logging
import traceback
import concurrent.futures
from typing import Callable, Iterable


def get_trace(e: Exception, n: int = 5):
    """Get the last n lines of the traceback for an exception"""
    return "".join(traceback.format_exception(e)[-n:])

def run_parallel_exec(exec_func: Callable, iterable: Iterable, *func_args, **kwargs):
    """
    Runs the `exec_func` function in parallel for each element in the `iterable` using a thread pool executor.
    
    Parameters:
        exec_func (Callable): The function to be executed for each element in the `iterable`.
        iterable (Iterable): The collection of elements for which the `exec_func` function will be executed.
        *func_args: Additional positional arguments to be passed to the `exec_func` function.
        **kwargs: Additional keyword arguments to customize the behavior of the function.
            - max_workers (int): The maximum number of worker threads in the thread pool executor. Default is 100.
            - quiet (bool): If True, suppresses the traceback logging for exceptions. Default is False.
    
    Returns:
        list[tuple]: A list of tuples where each tuple contains the element from the `iterable` and the result of executing the `exec_func` function on that element.

    Example:
        >>> from app.utils.helpers import run_parallel_exec
        >>> run_parallel_exec(lambda x: str(x), [1, 2, 3])
        [(1, '1'), (2, '2'), (3, '3')]
    """
    func_name = f"{exec_func.__name__} | parallel_exec | " if hasattr(exec_func, "__name__") else "unknown | parallel_exec | "
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=kwargs.pop("max_workers", 100), thread_name_prefix=func_name
    ) as executor:
        # Start the load operations and mark each future with each element
        future_element_map = {
            executor.submit(exec_func, element, *func_args): element
            for element in iterable
        }
        result: list[tuple] = []
        for future in concurrent.futures.as_completed(future_element_map):
            element = future_element_map[future]
            try:
                result.append((element, future.result()))
            except Exception as exc:
                log_trace = exc if kwargs.pop("quiet", False) else get_trace(exc, 3)
                logging.error(f"Got error while running parallel_exec: {element}: \n{log_trace}")
                result.append((element, exc))
        return result

def run_parallel_exec_but_return_in_order(exec_func: Callable, iterable: Iterable, *func_args, **kwargs):
    """
    Runs the `exec_func` function in parallel for each element in the `iterable` using a thread pool executor.
    Returns the result in the same order as the `iterable`.
    """
    # note this is usable only when iterable has types that are hashable
    result = run_parallel_exec(exec_func, iterable:=list(iterable), *func_args, **kwargs)

    # sort the result in the same order as the iterable
    result.sort(key=lambda x: iterable.index(x[0]))

    return [x[-1] for x in result]
