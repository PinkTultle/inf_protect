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

RoundKey_origin = []           #각 라운드 난수가 담길 리스트1




def init():

    while True :
        clear = lambda: os.system('cls')
        clear()

        print('-'*100)
        print('')
        print('1. 암호화')
        print('2. 복호화')
        print('3. 암호문 확인')
        print('4. 동의대 교가 입력')
        print('5. 프로그램 종료')
        print('')
        print('-'*100)
        st = int(input('>> '))

        if st == 1 :
            let_cich = input('암호화할 평문을 입력허시오.\n>>')
            encryption(let_cich) #암호화 함수
        elif st == 2 : 
            decryption() #복호화 함수
        elif st == 3 :
            Confirm() #암호문 확인
        elif st == 4 :
            school_price() #교가 입력
        elif st == 5 :
            return #프로그램 종료
        else : 
            print('올바른 기능 번호를 선택하여 주십시오')
        
        print()
        a = input('계속 하시려면 아무키나 눌러주십시오!')

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


def encryption(let_cich): #암호화 함수
    plain_text = let_cich  #평문 입력
    encoded_text = bytes(plain_text,'utf-8') #utf-8로 인코딩하며 바이트형 전환

    while True :
        try :
            first_round_key = int(input('라운드 키 생성을 위한 정수를 입력하시오(범위 0~255)\n>>'))
            #랜덤 모듈과 xor연산할 비밀번호 입력
        except :
            print('올바른 값을 입력해주세요')
        else :
            if first_round_key in range(256) :
                break
            else :
                print('지정 범위내의 수를 입력해주세요') 

    RoundKey = []

    for i in range(6) :  #라운드 키 생성 함수 여기서 6라운드까지의 난수 미리 생성 
        RandomKey = random.randint(0,255)
        RoundKey_origin.append(RandomKey)
        RoundKey.append(GOXOR(first_round_key,RoundKey_origin[i]))
        #암호화때 쓰는 라운드키 XOR 연산후 리스트에 추가
        

    

    for k in range(6) : #6라운드를 위한 반복문
        cipher = [] #매라운드마다 암호값을 저장할 리스트
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

    print('암호문 생성 완료!!')

    return cipher_text

def decryption(): #복호화 함수

    f = open("암호.txt", 'r', encoding= 'utf-8') #암호.txt에 저장된 암호문을 불러온다
    cipher_text = f.read()
    f.close()

    first_round_key = int(input('암호문을 복호화하기 위한 비밀번호를 입력하시오(범위 0~255)\n>>'))

    decryption_Key = []

    for i in range(6) :  #복호화 키 생성 함수 여기서 6라운드까지 복호화 키 XOR  
        decryption_Key.append(GOXOR(first_round_key, RoundKey_origin[i]))

    #plain_text = bytearray() 
    plain = []

    for i in range(6):
        
        plain_d = []

        if i == 0 :
            for k in range(len(cipher_text)) :
                Decryption_Initial = SBOX(ord(cipher_text[k]), 'dec')
                plain.append(GOXOR(Decryption_Initial,decryption_Key[-1]))
        
        else :
            
            for k in range(len(plain)) :
                passPbox = PBOX_right(plain[k], 2)
                passSbox = SBOX(passPbox, 'dec')
                end_decryption = GOXOR(passSbox,decryption_Key[-(i+1)])
                plain_d.append(end_decryption)
                if k is range(len(plain))[-1] :
                    plain = plain_d

        if i == range(6)[-1] :
            plain_text = bytes(plain)
    try :
        Decryption_text = plain_text.decode()
        print(Decryption_text)
    except :
        print('비밀번호가 일치하지 않습니다.')
        return

    return Decryption_text



def Confirm(): #암호문 확인
    f = open("암호.txt", 'r', encoding= 'utf-8') #암호.txt에 저장된 암호문을 불러온다
    cipher_text = f.read()
    print('암호문 : ', end='')
    print(cipher_text)
    f.close()    


def school_price(): #학교 교가 입력
    school_song = '하늘을 한 가슴에 푸르게 안고 산맥을 다스리며 꿈길 여는 곳 새 역사 문을 여는 학문의 요람 크나큰 우리보람 겨레의 자랑 영원속에 진리의 뿌리 내리고 진리 정의 창의를 피속에 키워 동의대학교 그 품에다 영광 다진다'
    encryption(school_song)

    print('교가 암호화를 완료했습니다')

init()




    

