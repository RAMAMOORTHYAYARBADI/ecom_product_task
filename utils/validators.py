

def ProductFeedback_Validators(data):
    json_keys =['product_id','title','review','rating']
    for val in json_keys:
        if  val not in dict.keys(data):
            return False
    return True


def Signup_Validators(data):
    json_keys =['email','paasword','username','confirm_password']
    for val in json_keys:
        if  val not in dict.keys(data):
            return False
    return True