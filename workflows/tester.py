import time
def compareImplementations(sequential=lambda x:x,parallel=lambda x:x,verbose = True)->tuple:
    #Override the definition of the print function to avoid printing to console
    #Printing is a major source of overhead and also clutters up the console output
    def print(*args):
        ...
    sequential_elapsed = -1
    parallel_elapsed = -1
    try:
        start=time.time()
        sequential()
        sequential_elapsed = time.time()-start
    except Exception as e:
        raise e
    try:
        start=time.time()
        parallel()
        parallel_elapsed = time.time()-start
    except Exception as e:
        raise e
    del print
    print_to_console(f"Sequential: {sequential_elapsed}\nParallel:{parallel_elapsed}")
    times =(sequential_elapsed,parallel_elapsed)
    if verbose:
        faster = 'Sequential' if sequential_elapsed<parallel_elapsed else 'Parallel'
        print_to_console(f"{faster} is faster by {(max(times)/(min(times) or float('nan')))*100}%")
    return times


#Since print will be locally redefined in compareImplementations,
#this method conserves the original print definition
def print_to_console(text:str)->None:
    print(text)