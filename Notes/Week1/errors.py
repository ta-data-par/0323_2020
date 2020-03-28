# Error Handling

# Import error
from random import something

# Name Error
def func(s):
    return something

func(11)

# Raise an Error
def test_for_positiveness(number):
    if number<0:
        print('ERROR! I am stuck in infinity')
        raise ValueError('We accept only positive numbers')
    else:
        print('alles gut!')
        
test_for_positiveness(11)

test_for_positiveness(-11)


# try except statement
try:
    test_for_positiveness(-11)
except NameError:
    print('please follow the instructions')
else:
    print('there is an error in your code but I dont know where')
    
