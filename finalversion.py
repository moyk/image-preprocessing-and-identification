from scipy import ndimage
import os  
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time
start_time = time.time()

def openfile(filename,folder):
   data= []
   fn =  folder +'/'+ filename
   with open(fn, "r") as outputfile:
       for line in outputfile:
           temp=[]
           for each in line:
               temp.append(each)
           if temp!=[]:
               data.append(temp)

   newdat = []
   for i in range (len(data)):
       temp =[]
       for j in range (len(data[i])):
           if data[i][j] == '0' or data[i][j] == '1':
               temp.append(int(data[i][j]))
       newdat.append(temp)

   return newdat


def convertbackground(matrix):
       print("--- %s seconds ---" % (time.time() - start_time)+ " converting background")
       
       boundary=[]
       #print matrix
       for i in range(len(matrix)): #append the first and last col of matrix to array 
               boundary.append(matrix[i][0])
               boundary.append(matrix[i][len(matrix[i])-1])
       for j in range(len(matrix[0])): #append the first and last row of matrix to array
               boundary.append(matrix[0][j])
               boundary.append(matrix[len(matrix)-1][j])
       freq = 0
       for num in boundary:
               if (num==1):
                       freq = freq + 1
       if (float(freq)/len(boundary)>0.8): #if boundary pixels are >80% black
               for m in range(len(matrix)):
                       for n in range(len(matrix[0])):
                               if (matrix[m][n]==0):
                                       matrix[m][n] = 1
                               elif (matrix[m][n]==1):
                                       matrix[m][n] = 0
       return matrix


def compute(data):
   s = 0
   count = 0
   for row in data:
       for entry in row:
           count+=1
           if entry == 1:
               s +=1
   return (s,count)

def isBig(data):
   print("--- %s seconds ---" % (time.time() - start_time)+ " big or not")
   total = compute(data)
   p = float(total[0])/total[1]
   return (p>=0.5)


def compare(data1, data2):
   sum1 = compute(data1)
   sum2 = compute(data2)
   if sum1>sum2:
       return 100
   if sum2<sum1:
       return -100
   else:
       return 0


def border(matrix):
   print("--- %s seconds ---" % (time.time() - start_time)+ " calculate border")
   
   minrow = len(matrix)
   maxrow = 0
   mincol = len(matrix[0])
   maxcol = 0
   for i in range(len(matrix)): 
       for j in range(len(matrix[0])):
           if (matrix[i][j]==1):
               if (i<minrow):
                   minrow = i
               if (i>maxrow):
                   maxrow = i
               if (j<mincol):
                   mincol = j
               if (j>maxcol):
                    maxcol = j


   rowlength = maxrow-minrow
   collength = maxcol-mincol
   maxlength = max(rowlength,collength) 
       
   newmatrix = []
   for rowind in range(0,maxlength+1):
       temp=[]
       if (minrow+rowind>len(matrix)):
           temp.append(0)
       else:
           for colind in range(0,maxlength+1):
               if (mincol+colind>len(matrix[0])):
                   temp.append(0)
               else:
                   temp.append(matrix[minrow+rowind-1][mincol+colind-1])
           newmatrix.append(temp)
   return newmatrix




def scale(matrix):
       print("--- %s seconds ---" % (time.time() - start_time)+ " scaling")
       rownum = len(matrix)
       colnum = len(matrix[0])
       if (rownum > 50):
               return shrink(matrix) #return a 50*50 matrix
       else:
               return enlarge(matrix) #return a 50*50 matrix


def enlarge(matrix):
   rownum = len(matrix)
   if (50%rownum==0):
       ratio = 50/rownum
   else:
       ratio = 50/rownum+1
               
   bigmatrix=[]
   for i in range(0,rownum*ratio):
       temp=[]
       for j in range(0,rownum*ratio):
           temp.append(matrix[i/ratio][j/ratio])
       bigmatrix.append(temp)


   finalmatrix=[]
   for i in range(0,50):
       secondtemp=[]
       for j in range(0,50):
           secondtemp.append(bigmatrix[i][j])
       finalmatrix.append(secondtemp)
   return finalmatrix


def shrink(matrix):
       rownum = len(matrix)
       if (rownum%50==0):
               ratio = rownum/50
       else:
               ratio = rownum/50+1


       newmatrix = []
       for i in range(0,50):
               temp = []
               for j in range(0,50):
                       entry = majority(matrix,ratio,i,j)
                       temp.append(entry)
               newmatrix.append(temp)
       return newmatrix


def majority(matrix,ratio,rowind,colind):
       msum = 0
       total =0
       for i in range(rowind*ratio, rowind*ratio+ratio):
           if i<= len(matrix)-1:
               for j in range(colind*ratio, colind*ratio+ratio):
                   if j<=len(matrix[0])-1:
                       total +=1
                       if matrix[i][j] == 1:
                           msum += 1
       if msum >= total/2.0 and total!=0:
               return 1
       else:
               return 0


def denoise(matrix):
       print("--- %s seconds ---" % (time.time() - start_time)+ " denoising")
       flag = 0
       for i in range(len(matrix)):
               for j in range(len(matrix[0])):
                       if (matrix[i][j]==1):
                           flag = traverse(matrix,i,j)
                           if (flag==0):
                               matrix[i][j] = 0
       return matrix


def traverse(matrix,i,j):#traverse neighbors of matrix[i][j]
       flag = 0
       for a in range(-1,2):
               if (a!=0 and i+a>=0 and i+a<len(matrix)):
                       if (matrix[i+a][j]==1):
                               flag = 1
       for b in range(-1,2):
               if (b!=0 and j+b>=0 and j+b<len(matrix[0])):
                       if (matrix[i][j+b]==1):
                               flag = 1
       return flag #flag=1 means it's not noise, flag=0 means it is noise


def center(matrix):
        print("--- %s seconds ---" % (time.time() - start_time)+ " centering")
        xvals = 0
        yvals = 0
        count = 0
        newmatrix = [[0 for i in range(len(matrix[0]))]for j in range(len(matrix))]
        for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                        if (matrix[i][j]==1):
                                count = count + 1
                                xvals += i
                                yvals += j
        xavgind = round(float(xvals)/count) #x val of center of the image
        yavgind = round(float(yvals)/count) #y val of center of the image
        xcenter = len(matrix)/2 #x val of center of the matrix
        ycenter = len(matrix[0])/2 #y val of center of the matrix
        xdiff =  xcenter-int(xavgind)
        ydiff =  ycenter-int(yavgind)
        for m in range(len(matrix)):
                for n in range(len(matrix[0])):
                        if (matrix[m][n]==1):
                                if (m>=0 and n>=0 and m+xdiff>=0 and n+ydiff>=0 and m+xdiff<len(matrix) and n+ydiff<len(matrix[0])):
                                        newmatrix[m+xdiff][n+ydiff] = 1
        return newmatrix


def findm(data):
   xlist = []
   ylist = []
   for i in range(len(data)):
       for j in range(len(data[i])):
           if data[i][j] == 1:
               xlist.append(i)
               ylist.append(len(data)-j)
   temp1 = ylist[-1]- ylist[0]
   temp2 = xlist[-1]- xlist[0]
   a = float(temp1)/temp2
   return a


def rotate(data):
   print("--- %s seconds ---" % (time.time() - start_time)+ " rotating")
   a = findm(data)
   slope =  math.degrees(math.atan(a))
   degree = 0
   if a > 0:
       degree = 270+slope
   else:
       degree = slope - 90
   data = ndimage.interpolation.rotate(data, degree, axes=(1, 0), reshape=True, output=None, order=3, mode='constant', cval=0.0, prefilter=True)
   return data


def distance(matrix1, matrix2):
       diffsum = 0
       diffsqr = 0
       for i in range(len(matrix1)):
               for j in range(len(matrix1[0])):
                       diffsqr = (matrix1[i][j]-matrix2[i][j])**2
                       diffsum += diffsqr
       return diffsum


def isSymmetry(data):
   print("--- %s seconds ---" % (time.time() - start_time)+ " symmetry")
   n = len(data)
   a=0
   count = 0
   for i in range(0,n/2):
       for j in range(0,len(data[0])):
           count+=1
           if data[i][j] == data[n-1-i][j]:
               a += 1
   accuracy1= float(a)/count


   n = len(data[0])
   a=0
   count = 0
   for i in range(0,len(data)):
       for j in range(0,n/2):
           count+=1
           if data[i][j] == data[i][n-1-i]:
               a += 1
   accuracy2 = float(a)/count
   if accuracy1>=0.8 or accuracy2>=0.8:
       return 1
   else:
       return 0

def preprocess(folder):
   data = []
   for fn in os.listdir(folder):
       if fn != '.DS_Store' and fn != 'version1.py':
            if ".swp" in fn:
               fn=fn[1:-4]
            matrix = openfile(fn,folder)
            f = smallpreprocess(matrix)
            group = (f,fn)
            data.append(group)              
   return data

def smallpreprocess(matrix):
   a = convertbackground(matrix)
   b = denoise(a)
   c = rotate(b)
   d = border(c)
   e = scale(d)
   f = center(e)
   return f


def isConvex(data):
   print("--- %s seconds ---" % (time.time() - start_time)+ " convexity")
   array = []  
   temp = []   
   for i in range(len(data)):
       for j in range(len(data[i])):
           if data[i][j] == 1:
               array.append([i,j])
   count = 0
   for k in range(600):
       indexone = random.randint(0, len(array)-1)
       indextwo  = random.randint(0,len(array)-1)
       nodeone = array[indexone]
       nodetwo = array[indextwo] 
       result = sub(nodeone, nodetwo, array)
       count = count + result
   if count > 0:
       return 0  
   else:
       return 1   


def sub(nodeone, nodetwo, array):
   count = 0
   num = 0
   if nodetwo[0] != nodeone[0]:
       k = float(nodetwo[1] - nodeone[1])/(nodetwo[0]-nodeone[0])
       b = nodetwo[1] - k * nodetwo[0]
       if nodeone[0] + 1 > nodetwo[0]:
           temp = nodeone 
           nodeone = nodetwo
           nodetwo = temp

       for m in range(nodeone[0]+1, nodetwo[0]):
           y = k * m + b 
           if y == int(y):
               y = int(y)
               item = [m,y]
               if item not in array:
                   return 1  
   return 0   


def category(data):
   categorylist = []
   for i in range(8):
       categorylist.append([])
   for a in data:
       matrix = a[0]
       cat = precategory(matrix)
       categorylist[cat].append(a)
   return categorylist

def precategory(a):
   symmetry = isSymmetry(a)
   convex = isConvex(a)
   area = isBig(a)
   compare = 100*symmetry + 10*convex + area
   if compare == 0:
       return 0
   if compare == 1:
       return 1
   if compare == 10:
       return 2
   if compare == 11:
       return 3
   if compare == 100:
       return 4
   if compare == 101:
       return 5
   if compare == 110:
       return 6
   if compare == 111:
       return 7 

def run(folder1,folder2,folder3,num):
   print "Parameters are: ", folder1,folder2,folder3,num
   num = int(num)
   predata = preprocess(folder1)
   catdata = category(predata)
   resultlist = []
   count = 0
   for fn in os.listdir(folder2):
           if fn != '.DS_Store' and fn != 'version1.py':
               if ".swp" in fn:
                   fn=fn[1:-4]
               data = openfile(fn,folder2)
               a = smallpreprocess(data)
               cat = precategory(a)   # which category this image belongs, cat is a number
               X = []
               X.append([0,fn])
               for image in catdata[cat]:    # compare every one in this list
                   dist = distance(image[0], a)
                   X.append([dist,image[1]])
               X = sorted(X,key=lambda x:x[0])
               ind = min(num+1,len(X))
               temp = []
               for i in range(0,ind):
                   temp.append(X[i]),
               resultlist.append(temp)
   output(resultlist, folder3)


def output(result,folder):
   name = folder+ ".txt"
   f = open(name,'w')
   for each in result:
       for i in each:
           f.write(i[1] + ' ')
       f.write('\n')
   f.close()
ss
