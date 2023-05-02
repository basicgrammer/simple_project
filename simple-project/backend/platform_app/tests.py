from django.test import TestCase

# Create your tests here.
from jamo import h2j, j2hcj



origin_keyword = "슈크림라떼21"



def create_keyword(origin_keyword:str) -> "keyword" :

    
    Init = []

    origin_name = origin_keyword

    for index in origin_name :

        tmp = h2j(index)
        imf = j2hcj(tmp)
        Init.append(imf[0])

    result = "".join(Init)

    return result


print(create_keyword(origin_keyword))


