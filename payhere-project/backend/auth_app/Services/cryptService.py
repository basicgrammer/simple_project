import bcrypt

class CryptService :

    def pw_crypt(pw_check:str) -> str:


        ## 솔트 랜덤 생성 // byte
        # salt 값을 6 ~ 12 숫자가 크면 해독하는 데 오래걸림 
        new_salt = bcrypt.gensalt()

        ## byte 단위의 인코딩 필요
        byte_pw = pw_check.encode('utf-8')
        
        ## 메소드 사용법을 참고하면 인자로 들어가는 데이터는 모두 byte로 처리되어야함
        hashed_pw = bcrypt.hashpw(byte_pw, new_salt)

        ## DB에서 패스워드 저장 필드가 Binary가 아닌 varchar로 구성되었기 때문에, decode 과정을 통해 다시 변환함
        decode_hashed_pw = hashed_pw.decode('utf-8')

        return decode_hashed_pw

