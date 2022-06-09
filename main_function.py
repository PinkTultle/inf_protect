import pandas as pd

def GOXOR(message, key):     #XOR 연산 함수
    return message^key          #두 개의 매개변수의 XOR 연산값을 반환

def SBOX(message,way): #message는 1바이트값 범위는 1~255, way가 'en'이면 암호화 'dec'면 복호화
    sbox = pd.read_csv('S-BOX.csv',names= ['of','after'],header=None) #csv파일을 데이터프레임에 삽입
    if way == 'en': #암호화
        return int(sbox.iloc[message,1])
    if way == 'dec': #복호화
        h = sbox[sbox['after'] == message]
        return int(h.iloc[0,0])
        
def PBOX_left(message,num):#왼쪽 시프트일때 비트가 왼쪽으로 오버하여 값손상시 -255처리 
    for i in range(num) : 
        message <<= 1
        if message > 255 : #왼쪽 시프트시 1이 시프트 되면 앞에 1비트가 늘어난다 이때 맨앞의 비트는 256
            message -= 255  #즉 255를 빼주면 남은 1비트는 1자리에 붙게 된다.
    return message

def PBOX_right(message,num): #오른쪽 비트 시프트 첫 자리 1인지 판단하여 1일 경우 True값
                             #True일 경우 오른쪽으로 시프트하여 값이 손실될때마다 or연산으로 순환구현
    for i in range(num) :
        if message & 0b00000001 == 1:    state = True 
        else : state = False  #AND연산으로 맨뒤의 값dl 1이면 
        message >>= 1
        if state == True :
            message |= 0b10000000
    return message