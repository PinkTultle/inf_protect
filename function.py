#기능들 함수로 구현
import pandas as pd

def SBOX(message,way): #message는 1바이트값 범위는 1~255, way가 'en'이면 암호화 'dec'면 복호화
    sbox = pd.read_csv('S-BOX.csv',names= ['of','after'],header=None)
    if way == 'en':
        return int(sbox.iloc[message,1])
    if way == 'dec':
        h = sbox[sbox['after'] == message]
        return int(h.iloc[0,0])


def PBOX_left(message,num):#왼쪽 시프트일때 비트가 왼쪽으로 오버하여 값손상시 -255처리 
    for i in range(num) : 
        message <<= 1
        if message >= 255 :
            message -= 255 
    return message

            
def PBOX_light(message,num): #오른쪽 비트 시프트 첫 자리 1인지 판단하여 1일 경우 True값
                             #True일 경우 오른쪽으로 시프트하여 값이 손실될때마다 or연산으로 순환구현
    for i in range(num) :
        if message & 0b00000001 == 1:    state = True 
        else : state = False
        message >>= 1
        if state == True :
            message |= 0b10000000
    return message


a = input('평문 입력 : ')

bb = bytes(a,'utf-8')

print('인코딩 : ',end = '')
print(bb)

chiper_m = []
hoho = []

for i in range(len(bb)) :
    d = SBOX(bb[i],'en')
    #print('sbox : ', end = '')
    #print(d)
    d = PBOX_left(d,1)
    #print('pbox :',end = '')
    #print(d)
    chiper_m.append(chr(d))

    
chiper_p = ''.join(chiper_m)
print(chiper_p)

#위에 까지하여 암호화
#여기부터 복호화

plain = bytearray()

for i in range(len(chiper_p)) :
    gen = PBOX_light(ord(chiper_p[i]),1)
    #print('pbox :',end = '')
    #print(gen)
    sjd = SBOX(gen,'dec')
    #print('sbox : ', end = '')
    #print(sjd)
    god = (sjd).to_bytes(1, byteorder="little")
    #print(god)
    plain.extend(god)

plain_text = plain.decode('utf-8')

#print(plain)





print(plain_text)

