import math

class Canvas():
    def __init__(self, width, height, background = " "):
        """Initialisation method for the Canvas class"""
        self.height = height
        self.width = width
        self.canData = []
        self.canH = 2
        self.canW = 2
        self.camPos = [0,0,-10]
        self.canPos = [0,0,-1]
        self.viewDir = [0,0,0] # vector of view direction (normalized)
        self.canParalx = [1,0,0]
        self.canParaly = [0,1,0]
        self.objects = []

        val = 0
        for i in range(len(self.camPos)):
            self.viewDir[i] = self.canPos[i] - self.camPos[i]
            val += abs(self.viewDir[i])

        self.pixelx = [0,0,0]
        self.pixely = [0,0,0]
        for i in range(len(self.canParalx)):
            self.pixelx[i] = (self.canW/(self.width-1))*self.canParalx[i]
            self.pixely[i] = (self.canH/(self.height-1))*self.canParaly[i]
            
        self.endPoint = [1,1,-1.0] 

    
    def render(self, background = " "):
        """
        Rendering method for the raytracer. Renders all objects attached to the canvas.
        Everything is drawn using raycasting. The canvas is positioned at (0.0, 0.0, -1.0) and
        has the endpoints(-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0), (1.0, -1.0, -1.0).

        The camera is positioned at (0.0, 0.0 , -10.0).

        Rays are send from the camera to the sampling points on the canvas.
        """
        
        for i in range(self.width):
            self.canData.append([])
            for j in range(self.height):
                self.canData[i].append([])
                val = 0
                for n in range(len(self.pixelx)):
                    self.canData[i][j].append((self.endPoint[n] - self.pixelx[n]*(i) - self.pixely[n]*(j)) - self.camPos[n])
                    val += abs(self.canData[i][j][n])
                self.canData[i][j][0] = self.canData[i][j][0]/val
                self.canData[i][j][1] = self.canData[i][j][1]/val 
                self.canData[i][j][2] = self.canData[i][j][2]/val
                self.canData[i][j].append(background)
                self.canData[i][j].append(math.inf)
        line = ""
        canvas = ""

        for i in range(len(self.canData[0])):
            for j in range(len(self.canData)):
                for o in self.objects:
                    result = ["+", math.inf, math.inf]
                    result = o.calc_intersection(self.camPos,[self.canData[j][i][0],self.canData[j][i][1],self.canData[j][i][2]])

                    if result[0]:
                        if isinstance(o, Sphere):
                            res = min(result[1],result[2])
                            if res < self.canData[j][i][4]:
                                self.canData[j][i][4] = res
                                self.canData[j][i][3] = o.getColor()
                            elif res < self.canData[j][i][4]:
                                self.canData[j][i][4] = res
                                self.canData[j][i][3] = o.getColor()
                            else:
                                pass

                        elif(isinstance(o,Triangle)):
                            if result[1] < self.canData[j][i][4]:
                                self.canData[j][i][4] = result[1]
                                self.canData[j][i][3] = o.getColor()
                            else:
                                pass
               
                line = self.canData[j][i][3] + " " + line
            canvas = canvas + line + "\n"
            line = ""
        return (canvas)

    def attach(self, toAttach):
        """Method for attaching an object to the scene. Only models attached to the canvas are drawn."""
        self.objects.append(toAttach)

class Sphere():

    def __init__(self, origin, radius, color):
        """
        Initialisation method for Sphere class
        Expects the origin as an arrays in the form of [x, y, z].
        Radius is the radius of the sphere.
        """
        self.color = color
        self.ori = origin
        self.rad = radius
        
    def calc_intersection(self, ray_o, ray_d):
        discriminant = 0
        A = [0,0,0]
        B = [0,0,0] 
        C = [0,0,0] 

        for i in range(len(ray_d)):
            B[i] = ray_d[i] * (ray_o[i] - self.ori[i])
            A[i] = (ray_d[i] * ray_d[i])
            C[i] = (ray_o[i] - self.ori[i]) * (ray_o[i] - self.ori[i])

        discriminant = sum(B)*sum(B)-sum(A)*(sum(C)-pow(self.rad,2))

        if discriminant >= 0 and discriminant >= 0 and discriminant >= 0:
            t1 = 0
            t2 = 0
            t1 = (-sum(B) + math.sqrt(discriminant))/sum(A)
            t2 = (-sum(B) - math.sqrt(discriminant))/sum(A)
            return [True,t1,t2]
        else:
            return [False,math.inf] 

    def getColor (self):
        return self.color


class Triangle():
    
    def __init__(self, a, b, c, color):
        """
        Initialisation method for the Triangle class
        Expects points as arrays in the form of [x, y, z]. 
        Color is the string the triangle is drawn in.
        """
        self.color = color
        self.a = a
        self.b = b
        self.c = c
        self.A_1 = [a[0]-b[0],a[1]-b[1],a[2]-b[2]]
        self.A_2 = [a[0]-c[0],a[1]-c[1],a[2]-c[2]]

    def getColor (self):
        return self.color

    def calc_determinant(self, A):
        det_A = A[0][0]*A[1][1]*A[2][2] + A[1][0]*A[2][1]*A[0][2] + A[2][0]*A[0][1]*A[1][2] -\
                A[0][2]*A[1][1]*A[2][0] - A[1][2]*A[2][1]*A[0][0] - A[2][2]*A[0][1]*A[1][0]
        return det_A
    
    def calc_intersection(self, ray_o, ray_d):

        A = [self.A_1,self.A_2,ray_d]
        det_A = self.calc_determinant(A)

        M = A[0][0] * (A[1][1] * A[2][2] - A[2][1] * A[1][2]) + \
            A[0][1] * (A[2][0] * A[1][2] - A[1][0] * A[2][2]) + \
            A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])

        j = self.a[0]-ray_o[0]
        k = self.a[1]-ray_o[1]
        l = self.a[2]-ray_o[2]
        
        b = (j * (A[1][1] * A[2][2] - A[2][1] * A[1][2]) + \
            k * (A[2][0] * A[1][2] - A[1][0] * A[2][2]) + \
            l * (A[1][0] * A[2][1] - A[1][1] * A[2][0])) / M
        
        y = (A[2][2] * (A[0][0] * k - j * A[0][1]) + \
            A[2][1] * (j * A[0][2] - A[0][0] * l) + \
            A[2][0] * (A[0][1] * l - k * A[0][2])) / M
        
        t = -((A[1][2] * (A[0][0] * k - j * A[0][1]) + \
                A[1][1] * (j * A[0][2] - A[0][0] * l) + \
                A[1][0] * (A[0][1] * l - k * A[0][2])) /M)

        if(t < 0):
            return [False,math.inf]
        
        if (y < 0) or (y > 1.0001):
            return [False,math.inf]
        
        elif (b < 0) or (b > 1.0001-y):
            return [False,math.inf]
        
        else:
            return [True,t]
            

"""
Commands are prompted and executed here.
"""
print("Create a canvas.")
canvasX = int(input("Please provide the width of the Canvas: "))
canvasY = int(input("Please provide the heigth of the Canvas: "))
fillingChar = input("With which character should the empty space be filled?: ")
      
C = Canvas(canvasX, canvasY, fillingChar)

while(True):
    print("Choose one of follwing commands:")
    print("Type 's' to create a Sphere.")
    print("Type 't' to create a Triangle.")
    print("Type 'render' to render the space")
    command = input("Command?:")
    if (command == 's'):
        print("Please enter the 3D Point of the center of the sphere")
        print("divide the x,y and z Coordinate by a space")
        print("example entry: '1 2 3'")
        center = list(map(float, 
            input("\nEnter x y z coordinates : ").strip().split()))[:3]
        radius = float(input("Enter the Radius of the sphere: "))
        charSphere = input("Enter the character that should fill the sphere: ")
        S = Sphere(center, radius, charSphere)
        C.attach(S)
    elif (command == 't'):
        print("To draw a Triangle we need three points in space that represent the corners of the triangle")
        print("Please provide the first corner point of the triangle by divide the x,y and z Coordinate with a white space")
        print("example entry: '1 2 3'")
        a = list(map(float, 
            input("\nEnter x y z coordinates: ").strip().split()))[:3]
        print("please provide the second point of the triangle")
        b = list(map(float, 
            input("\nEnter x y z coordinates: ").strip().split()))[:3]
        print("please provide the third point of the triangle")
        c = list(map(float, 
            input("\nEnter x y z coordinates: ").strip().split()))[:3]
        charSphere = input("Enter the character that should fill the triangle: ")
        T2 = Triangle([1,0,-0.5], [0,1,-0.5], [0,0,-0.5], "_")
        C.attach(T2)
    elif (command == 'render'):
        print(C.render(fillingChar))
        break
    else:
        print("Thats not a valid Command \n")

