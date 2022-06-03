#기능들 함수로 구현
import numpy as np
import pandas as pd

def SBOX(message,way): #message는 1바이트값 범위는 1~255, way가 'en'이면 암호화 'dec'면 복호화
    sbox = pd.read_csv('S-BOX.csv',names= ['of','after'],header=None)
    if way == 'en':
        return (sbox.iloc[message,1])
    if way == 'dec':
        h = sbox[sbox['after'] == message]
        return (h.iloc[0,0])


def PBOX_left(message,num):#왼쪽 시프트일때 비트가 왼쪽으로 오버하여 값손상시 -255처리 
    for i in range(num) : 
        message <<= 1
        if message >= 255 :
            message -= 255 
    return message

            
def PBOX_light(message,num): #오른쪽 비트 시프트 첫 자리 1인지 판단하여 1일 경우 True값
                             #True일 경우 
    for i in range(num) :
        if message & 0b00000001 == 1:    state = True 
        else : state = False
        message >>= 1
        if state == True :
            message |= 0b10000000
    return message




'''
def split(message, size=8):
    return [message[i:i + size] for i in range(0, len(message), size)]

'''

print("섹시한 현서")

a = input('평문 입력 : ')

bb = bytes(a,'utf-8')


print(bb)

for i in range(len(bb)) :
    d = SBOX(bb[i],'en')
    print(d)


#print(int())

'''
a = SBOX(a,'en')
print(a)
print(bin(a))

a = PBOX_light(a,4)

print(a)
print(bin(a))'''