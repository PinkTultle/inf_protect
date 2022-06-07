'''
파이썬 기말프로젝트

기본 화면 구성 실행시 버튼 배치 
1. 암호화 2. 복호화 3. 동의대 교가 암호화 4. 평문 보기 5. 프로그램 종료

암호화시 >> 새창 실행 - 내부 텍스트 필드와 입력 버튼 - 버튼 클릭 메세지 박스 출력 '암호화 되었습니다.'
복호화시 >> 새창 실행 - 비밀번호 입력 입력 

'''

import random
import pandas as pd
from matplotlib.pyplot import close
import os

#파이썬으로 SPN 구조를 활용한 암호 구현

RoundKey = []           #각 라운드 키가 담길 리스트




def init():

    clear = lambda: os.system('cls')
    clear()

    print('-'*100)
    print('')
    print('1. 암호화')
    print('2. 복호화')
    print('3. 암호문 확인')
    print('4. 평문 확인')
    print('5. 동의대 교가 입력')
    print('6. 프로그램 종료')
    print('')
    print('-'*100)
    st = input('>> ')

    if st == 1 :
        encryption() #암호화 함수
    elif st == 2 : 
        decryption() #복호화 함수
    elif st == 3 :
        Confirm() #암호문 확인
    elif st == 4 :
        check() # 평문 확인
    elif st == 5 :
        school_price() #교가 입력
    elif st == 6 :
        return #프로그램 종료


# 위는 메인 화면 함수
# 이 밑은 S-BOX, P-BOX 및 XOR함수 
#

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
        if message >= 255 : #왼쪽 시프트시 1이 시프트 되면 앞에 1비트가 늘어난다 이때 맨앞의 비트는 256
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


def encryption(): #암호화 함수
    plain_text = input('암호화할 평문을 입력허시오.\n>>') #평문 입력
    encoded_text = bytes(plain_text,'utf-8') #utf-8로 인코딩하며 바이트형 전환

    first_round_key = int(input('라운드 키 생성을 위한 정수를 입력하시오(범위 0~255)\n>>'))
    #랜덤 모듈과 xor연산할 비밀번호 입력 


    for i in range(7) :  #라운드 키 생성 함수 여기서 6라운드까지 라운드키 미리생성   
        RandomKey = random.randint(0,255)
        RoundKey.append(GOXOR(first_round_key, RandomKey))
    

    for k in range(0,6) : #6라운드를 위한 반복문
        cipher = [] #매라운드마다 암호값을 저장할 리스트
        print('라운드 -', k+1)
        if k is range(0,6)[-1] : #마지막 라운드는 XOR연산과 S-BOX만 사용
            for i in range(len(encoded_text)) :
                Encrypting = GOXOR(encoded_text[i],RoundKey[k])
                passSbox = SBOX(Encrypting,'en')
                cipher.extend(chr(passSbox)) #암호화된 각 문자를 문자열로 리스트에 저장
            break

        for i in range(len(encoded_text)) : #1~5라운드
            Encrypting = GOXOR(encoded_text[i],RoundKey[k]) #라운드의 첫번째 XOR
            passSbox = SBOX(Encrypting,'en') #S-BOX통과
            passPbox = PBOX_left(passSbox,2) #P-BOX통과 >>두번쨰 매게 변수는 시프트 횟수
            cipher.extend((passPbox).to_bytes(1, byteorder="little"))
            #S-BOX와 P-BOX를 통과하며 정수로 바뀐 값을 다시 바이트형의 변환
            #동시에 extend를 통해 리스트에 추가
            if i is range(len(encoded_text))[-1] :
                encoded_text = bytes(cipher)
            #다음 라운드를 시작하기위해 이번 라운드에서 암호화 된 암호문을 할당

    cipher_text = ''.join(cipher) #완성된 암호문은 리스트기에 join을 통해 문자열로 변환
    

    #암호문을 '암호.txt'에 저장
    f = open("암호.txt", 'w', encoding= 'utf-8')
    f.write(cipher_text)
    f.close()

    return cipher_text







    
    
'''
def fdecryption(): #복호화 함수

def Confirm(): #암호문 확인

def check(): #암호문 확인

def school_price(): #암호문 확인
'''