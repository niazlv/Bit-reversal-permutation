import cv2
import numpy as np

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