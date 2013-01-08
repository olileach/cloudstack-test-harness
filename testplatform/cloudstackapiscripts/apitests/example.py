class MyClass():
     

    vara = 'Class Variable A'

    def __init__(self):

        self.varb = 'Class instantiation Variable B'

    def a(self):

        varc = 2
        vard = 3 

        print 'def a function variables unchanged', varc, vard

        MyClass.vara = 'Class Variable A now changed by def a'
       
    def b(self):

        print self.varb
        self.varb = 'Class instantiation Variable B now changed by def b'
        print self.varb


if __name__ == "__main__":

    
    print MyClass.vara

    a = MyClass()
    a.a()
    a.b()
    print MyClass.vara
    a.a()

