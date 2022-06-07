import random
import pandas as pd
from matplotlib.pyplot import close

#파이썬으로 SPN 구조를 활용한 암호 구현

RoundKey = []           #각 라운드 키가 담길 리스트

###암호화###
def Encryption(Text):           #암호화 함수
    global RoundKey

    UserKey = int(input('암호화를 위해 라운드 키의 초기값을 입력하세요(0~255)>> '))

    EncrypText = []         #암호문이 담길 리스트

    ToByte = bytes(Text, 'utf-8')               #평문을 바이트 형태로 변환
    
    RandomKey = random.randint(0,255)                   #난수 키 초기값
    RoundKey.append(RandomKey)
    FirstKey = RoundXOR(UserKey, RandomKey)             #사용자 입력 키와 난수 키 초기값의 XOR 


    #난수로 라운드 키 생성
    for i in range(4):
        RanRoundKey = random.randint(0,255)            
        RoundKey.append(RanRoundKey)
    

    for j in range(len(ToByte)):
        XORtoByte = RoundXOR(ToByte[j], FirstKey)       #평문 블록과 라운드 키 초기값으로 XOR 연산

        #1라운드
        SText_1 = SBox(XORtoByte, 'en')                 #S-Box에 치환
        PText_1 = PBox_left(SText_1, 1)                 # <<< 1 연산
        ResultXOR_1 = RoundXOR(PText_1, RoundKey[1])

        #2라운드
        SText_2 = SBox(ResultXOR_1, 'en')
        PText_2 = PBox_left(SText_2, 1)
        ResultXOR_2 = RoundXOR(PText_2, RoundKey[2])

        #3라운드
        SText_3 = SBox(PText_2, 'en')
        PText_3 = PBox_left(SText_3, 1)
        ResultXOR_3 = RoundXOR(PText_3, RoundKey[3])

        #4라운드
        ResultXOR_4 = SBox(ResultXOR_3, 'en')
        LastResult = RoundXOR(ResultXOR_4, RoundKey[4])

        EncrypText.append(chr(ResultXOR_4))     #결과값을 암호문 리스트에 추가

    ChiperText = ''.join(EncrypText)
    print(ChiperText)

    f = open("암호문.txt", 'w', encoding='utf-8')   #txt 파일 생성
    f.write(ChiperText)                             #결과값을 txt 파일에 저장
    f.close()
    print('[system] 암호화가 완료되었습니다.\n')

'''

def DivisionBlock(message, size=16):        #블록 분할 함수
    return [message[i:i + size] for i in range(0, len(message), size)]
'''


def RoundXOR(text, key):     #XOR 연산 함수
    return text^key          #두 개의 매개변수의 XOR 연산값을 반환


def SBox(message, way):         #S-Box 함수
    sbox = pd.read_csv('S-BOX.csv',names= ['of','after'],header=None)
    if way == 'en':
        return int(sbox.iloc[message,1])
    if way == 'dec':
        h = sbox[sbox['after'] == message]
        return int(h.iloc[0,0])


def PBox_left(message,num):#왼쪽 시프트일때 비트가 왼쪽으로 오버하여 값손상시 -255처리 
    for i in range(num) : 
        message <<= 1
        if message >= 255 :
            message -= 255 
    return message

            
def PBox_right(message,num): #오른쪽 비트 시프트 첫 자리 1인지 판단하여 1일 경우 True값
                             #True일 경우 오른쪽으로 시프트하여 값이 손실될때마다 or연산으로 순환구현
    for i in range(num) :
        if message & 0b00000001 == 1:    state = True 
        else : state = False
        message >>= 1
        if state == True :
            message |= 0b10000000
    return message



###복호화###
def Decryption():           #복호화 함수
    CipherFile = open('암호문.txt', 'r')        #암호문 읽어오기
    CipherText = CipherFile.read()

    UserKey = int(input('복호화를 위해 라운드 키의 초기값을 입력하세요(0~255)>> '))
    PassKey = RoundXOR(UserKey, RoundKey[0])

    DecrypText = bytearray()

    for i in range(len(CipherText)):
        XORtoByte = RoundXOR(ord(CipherText[i]), RoundKey[3])

        #1라운드
        SText_Inv_1 = SBox(XORtoByte, 'dec')
        ResultXOR_1 = RoundXOR(SText_Inv_1, RoundKey[2])

        #2라운드
        PText_Inv_2 = PBox_right(ResultXOR_1, 1)
        SText_Inv_2 = SBox(PText_Inv_2, 'dec')
        ResultXOR_2 = RoundXOR(SText_Inv_2, RoundKey[1])

        #3라운드
        PText_Inv_3 = PBox_right(ResultXOR_2, 1)
        SText_Inv_3 = SBox(PText_Inv_3, 'dec')
        ResultXOR_3 = RoundXOR(SText_Inv_3, RoundKey[0])

        #4라운드
        PText_Inv_4 = PBox_right(ResultXOR_3, 1)
        SText_Inv_4 = SBox(PText_Inv_4, 'dec')
        LastResult = RoundXOR(SText_Inv_4, PassKey)

        PlainText = (LastResult).to_bytes(1, byteorder="little")
        DecrypText.extend(PlainText)

    ResultText = DecrypText.decode('utf-8')
    print(ResultText) 


SchoolSong = "하늘을 한 가슴에 푸르게 안고 산맥을 다스리며 꿈길 여는 곳 새 역사 문을 여는 학문의 요람 크나큰 우리보람 겨레의 자랑 영원속에 진리의 뿌리 내리고 진리 정의 창의를 피속에 키워 동의대학교 그 품에다 영광 다진다"

while(True):
    print('[>>> Python으로 SPN 암호 알고리즘 구현하기 <<<]')
    print('1. 암호화')
    print('2. 복호화')
    print('3. 동의대 교가 암호화')
    print('4. 교가 원문 출력')
    print('5. 프로그램 종료')

    choice = input('\n원하는 메뉴를 선택하세요(숫자 입력)>> ')

    if choice == '1':
        PlainText = input('암호화할 평문을 입력하세요>> ')     #원문 저장 변수
        Encryption(PlainText)
    elif choice == '2':
        Decryption()
    elif choice == '3':
        Encryption(SchoolSong)
    elif choice == '4':
        print(SchoolSong)
    else:
        print('[system] 프로그램이 종료됩니다.')
        break
