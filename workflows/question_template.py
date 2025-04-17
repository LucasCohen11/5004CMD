from tester import compareImplementations as compare
#any other imports

#Must not take any arguments
def q1x_sequential():
    ...

def q1x_Dask():
    ...



if __name__ == "__main__":
    print("Result of comparing question 1x")
    compare(q1x_sequential,q1x_Dask)