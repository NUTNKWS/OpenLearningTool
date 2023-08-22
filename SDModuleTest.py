
from gpb import delay
import pomaspackage as pomaspkg


import const

stored_data = ['Today is Thursday.',
                'I am working with the AI-FML Learning Tool.']

if __name__ == '__main__':

    mySD = pomaspkg.SDModule()
    #readfile
    data = mySD.ReadFile('./sd/input/test.py')
    print (data)

    #write and delete file (Note: You can see the executed resule after reset the board)
    mySD.WriteFile('./sd/output/test.txt', stored_data, 'w')
    mySD.DeleteFile('./sd/output/test.py')