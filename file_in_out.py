#파일 입출력 함수 연습 예정

def make_binary_file(Contents,Title) :  #바이너리 파일 생성
    txtfile = open('암호문/'+Title+'.bin', 'wb')
    txtfile.write(Contents)
    txtfile.close()

def read_binary_file(Title) : #바이너리 파일 읽기
    binaryfile = open('암호문/'+Title+'.bin', 'rb')
    cryptogram = binaryfile.read()
    binaryfile.close()
    return cryptogram

def make_txt_file(Contents,Title) :    #텍스트 파일 생성
    txtfile = open('평문/'+Title+'.txt', 'w', encoding='utf-8')
    txtfile.write(Contents)
    txtfile.close()

def read_txt_file(Title) : #텍스트 파일 읽기
    txtfile = open('평문/'+Title+'.txt', 'w', encoding='utf-8')
    plain_text = txtfile.read()
    txtfile.close()
    return plain_text


