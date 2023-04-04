import cv2
import numpy as np

def bit_print(block:int=4)->dict[list]:
    a = (2<<(block-1))
    di = []
    for i in range(0,a):
        di.append(list(format(i, f'0{block}b')))
    return di

def reverseIndexSingle(di:dict)->dict[list[int]]:
    # reverce index dict of list int's
    for i in range(0,len(di)):
        # safe length into new variable for convenience
        ldi = len(di[i])
        # safe list into new variable for convenience
        dij = di[i]
        for j in range(0,ldi//2):
            a = dij[j]
            dij[j] = dij[ldi-j-1]
            dij[ldi-j-1] = a
        # return list to global dict
        di[i] = dij
    return di

def reverseIndex(di:dict[dict[list[int]],dict])->dict[dict[list[int]],dict]:
    if(len(di)<2):
        raise ValueError("di length can't be less than 2!")
    di[0] = reverseIndexSingle(di[0])
    return di


def List2Int(di:dict[list[int]])->dict[int]:
    # init dict to return him
    idi = []
    for i in range(len(di)):
        # convert list[binary] to integer variable
        res = int("".join(str(x) for x in di[i]), 2)
        # and append to return dict 
        idi.append(res)
    return idi

def sortByDict(di:dict[dict[list[int]],dict])->dict[dict[list[int]],dict]:
    if(len(di)<2):
        raise ValueError("di length can't be less than 2!")
    index = di[0]
    data = di[1]
    lin = len(index)
    if(not (lin == len(data))):
        if(((lin & (lin-1) == 0) and lin != 0)):
            raise ValueError("Number is not a degree of two, or the length of the indexes is not equal to the length of the data!!!")
    iindex = List2Int(index)
    # now sort data by index
    for i in range((lin//2)):
        # (re)init local variables
        max = iindex[i]
        min = iindex[i]
        imax = i
        imin = i
        #find min and max
        for j in range(i,lin-i):
            if(min > iindex[j]):
                min = iindex[j]
                imin = j
            if(max < iindex[j]):
                max = iindex[j]
                imax = j
        
        # and replace him
        # min
        #iindex
        buff = iindex[i]
        iindex[i] = iindex[imin]
        iindex[imin] = buff
        #index
        buff = index[i]
        index[i] = index[imin]
        index[imin] = buff
        #data
        buff = data[i]
        data[i] = data[imin]
        data[imin] = buff
        
        # max
        if(not (max == iindex[lin-i-1])):
            #iindex
            buff = iindex[lin-i-1]
            iindex[lin-i-1] = iindex[imax]
            iindex[imax] = buff
            #index
            buff = index[lin-i-1]
            index[lin-i-1] = index[imax]
            index[imax] = buff
            #data
            buff = data[lin-i-1]
            data[lin-i-1] = data[imax]
            data[imax] = buff
    # pack all local variables to dict and return 
    di[0] = index
    di[1] = data
    return di

def printDict(di:dict[dict[list[int]],dict]):
    print("index:",end="")
    print(List2Int(di[0]))
    print("data:",end="")
    if(type(di[1]) == type(list)):
        print(List2Int(di[1]))
    else:
        print(di[1])

def order_in_reversed_bits(data: np.ndarray) -> np.ndarray:
    tobinary = lambda t: np.binary_repr(t, width=len(np.binary_repr(data.shape[0]-1)))[::-1]
    func = np.vectorize(tobinary)
    a = func(np.arange(0,data.shape[0]))
    t = np.zeros(data.shape,dtype='float64')

    for i,k in enumerate(a):
        t[int(k,2)] = data[i]

    return t

def order_in_reversed_bits_python(lst):
    return order_in_reversed_bits(lst)
    return [v for _, v in sorted(enumerate(lst), key=lambda k: bin(k[0])[:1:-1])]

def example1():
    # generate bit dict
    di = []
    #index
    di.append(bit_print(4))
    #data's
    #di.append(bit_print(4)) 
    di.append([])
    sstr = "hello world!"
    for i in range(0,(2<<3)):
        if(len(sstr)<=i):
            di[1].append("*")
            sstr = sstr + "*"
        else:
            di[1].append(sstr[i])

    print("first run block")
    # --------  begin block bit reversal permutation --------
    print("Before any change")
    printDict(di)
    #bit-reversion
    di = reverseIndex(di)
    print("\nAfter reverseIndex change")
    printDict(di)
    # and sort data by reversed index
    di = sortByDict(di)
    print("\nAfter sortByDict change")
    printDict(di)
    # --------  end block bit reversal permutation   --------

    # corypt data

    di[1][3] = "#"
    di[1][4] = "#"
    #di[1][5] = "#"
    #di[1][6] = "#"

    print("second run block")
    # --------  begin block bit reversal permutation --------
    print("Before any change")
    printDict(di)
    #bit-reversion
    di = reverseIndex(di)
    print("\nAfter reverseIndex change")
    printDict(di)
    # and sort data by reversed index
    di = sortByDict(di)
    print("\nAfter sortByDict change")
    printDict(di)
    # --------  end block bit reversal permutation   --------

    print(f"started word: \n\t'{sstr}'")
    print(f"after corrupt and repair by bit reversal: \n\t'{''.join(di[1])}'")
    di[1] = order_in_reversed_bits_python(di[1])
    print("".join(di[1]))
    di[1] = order_in_reversed_bits_python(di[1])
    print("".join(di[1]))

def rever(img:cv2.Mat,size:int=0)->cv2.Mat:
    if(size==0):
        size = img.shape[0]
    print(img.shape)
    print(size)
    print(img.shape[0]//size)
    for i in range(img.shape[0]):
        for j in range(0,img.shape[0]//size): 
            img[i][j*size:j*size+size] = order_in_reversed_bits_python(img[i][j*size:j*size+size])
    return img

def example2(img:cv2.Mat,size:int=0)->cv2.Mat:
    img = rever(img,size)
    # получим массив, с которым будем работатьs
    img = cv2.transpose(img)
    img = rever(img,size)
    return img

if __name__ == "__main__":
    img = cv2.imread('A.png', cv2.IMREAD_COLOR)
    cv2.imshow("before",img)
    cv2.waitKey(0)

    img = example2(img)
    cv2.imwrite("corupt.png",img)
    cv2.imshow("after encode(edit corrupt.png)",img)
    cv2.waitKey(0)
    
    img = cv2.imread('corupt.png', cv2.IMREAD_COLOR)
    cv2.imshow("check corrupted",img)
    cv2.waitKey(0)

    img = example2(img)
    cv2.imshow("result",img)
    cv2.waitKey(0)
    pass