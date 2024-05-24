from flask import request,jsonify,redirect
# from cryptoServer import *
from random import randint
class User():
    def __init__(self):
        '''
        :param _USERINFO: 用户账号列表
        '''
        self._USERINFO = {
            'qwerty1':{
                'password':'password1'
            },
            'qwerty2': {
                'password': 'password2'
            },
            'admin': {
                'password': 'password'
            }

        }

        #生成公钥和私钥
        self._CRYPTO= {
            'qwerty2': {
                'public_key': '',
                'private_key': ''
            }
        }

        #self._private_key,self._public_key = generate_key()
    def check_user_creation(self, username, password):
        print("The input user credentials are: %s" % username, password)
        if username in self._USERINFO:
            if self._USERINFO[username][password] == password:
                print(0)
                return 0
            else:
                print(1)
                return 1
        else:
            print(-1)
            return -1
    # def bool_find_user(self,username):
    #     return username in self._USERINFO
    #
    # def bool_veritify_user(self,username,password):
    #     if self.bool_find_user(username):
    #         if self._USERINFO[username] == password:
    #             return True
    #         else:
    #             return jsonify({'status': 'user undefine'})
    #     else:
    #         return jsonify({'status': 'invalid user'})
    #
    #
    #
    # def login_no_veritify_code(self):
    #     response_object = {'status': 'success'}
    #     print(request.data)
    #     if request.method == 'POST':
    #         post_data = request.get_json()
    #         username = post_data.get('username')
    #         phone = post_data.get('phone')
    #         password = post_data.get('password')
    #         if self.bool_find_user(username):
    #             self._USERINFO[username]['password']==password
    #             print("登录成功，你好%s"%username)
    #             response_object = {'status': 'success'}
    #             #response_object['user'] = self._USERINFO
    #             return  redirect('/books')
    #         else:
    #             return jsonify({'status': '登录失败'})
    #
    # def login_rsa_decrypt_no_veritify_code(self):
    #     response_object = {'status': 'success'}
    #     print(request.data)
    #
    #     if request.method == 'POST':
    #
    #         post_data = request.get_json()
    #         username = post_data.get('username')
    #         state_type = post_data.get('state_type')
    #
    #         if state_type == 'beforelogin':
    #             if self.bool_find_user(username):
    #                 #找到用户并生成公钥和私钥
    #                 private_key,public_key = generate_key()
    #                 self._CRYPTO[username] = {'private_key':private_key,'public_key':public_key}
    #                 public_key = self._CRYPTO[username]['public_key']
    #                 print('====public_key=====')
    #                 print(type(public_key))
    #                 #print(str(public_key))
    #
    #                 return public_key
    #
    #             else:
    #                 return jsonify({'status': 'invalid user'})
    #         elif state_type=='logging':
    #             ##TODO:加密logging，需要修改前端的数据包格式
    #             print("====logging====")
    #             print("username: %s"%(username))
    #             logindata = post_data.get('logindata')
    #             print("=======logindata========")
    #             print(logindata)
    #             result_decrypy = rsa_decrypy(self._CRYPTO[username]['private_key'],logindata)
    #             print("======result_decrypy=========")
    #             print(str(result_decrypy).split("\"")[1])
    #             if self._USERINFO[username]['password']==str(result_decrypy).split("\"")[1]:
    #                 return jsonify({'status': 'success'})
    #             else:
    #                 return jsonify({'status': 'invalid pwd'})
    #
    #
    # def login_rsa_decrypt_with_veritify_code(self):
    #     response_object = {'status': 'success'}
    #     print(request.data)
    #
    #     if request.method == 'POST':
    #
    #         post_data = request.get_json()
    #         username = post_data.get('username')
    #         state_type = post_data.get('state_type')
    #
    #         if state_type == 'beforelogin':
    #             if self.bool_find_user(username):
    #                 #找到用户并生成公钥和私钥
    #                 private_key,public_key = generate_key()
    #                 self._CRYPTO[username] = {'private_key':private_key,'public_key':public_key}
    #                 public_key = self._CRYPTO[username]['public_key']
    #                 print('====public_key=====')
    #                 print(type(public_key))
    #                 #print(str(public_key))
    #
    #                 #此时生成验证码
    #                 phone = self._USERINFO[username]['phone']
    #                 self._PHONE[phone] = str(randint(100000,999999))
    #                 print('====生成登录验证码=====')
    #                 print(self._PHONE[phone])
    #
    #                 return public_key
    #
    #             else:
    #                 return jsonify({'status': 'invalid user'})
    #         elif state_type=='logging':
    #             ##TODO:加密logging，需要修改前端的数据包格式
    #             print("====logging====")
    #             print("username: %s"%(username))
    #             logindata = post_data.get('logindata')
    #             print("=======logindata========")
    #             print(logindata)
    #             result_decrypy = rsa_decrypy(self._CRYPTO[username]['private_key'],logindata)
    #             result_decrypy = str(result_decrypy).split("\"")[1]
    #             password = result_decrypy.split("||||")[0]
    #             veritify_code = result_decrypy.split("||||")[1]
    #             print("======logging:result_decrypy=========")
    #             phone = self._USERINFO[username]['phone']
    #             print(username,password,phone,veritify_code)
    #             print("======_PHONE[phone]==========")
    #             print(self._PHONE)
    #             if self._USERINFO[username]['password']==password:
    #                 if self._PHONE[phone] ==veritify_code:
    #                     return jsonify({'status': 'success'})
    #                 else:
    #                     return jsonify({'status': 'invalid code'})
    #             else:
    #                 return jsonify({'status': 'invalid pwd'})
    #
    #
    #
    # def pre_register_get_veritify_code(self,phone):
    #     print(phone)
    #     veritify_code = randint(100000,999999)
    #     self._PHONE[phone] = str(veritify_code)
    #     print(veritify_code)
    #
    # def register_with_sms_code(self):
    #     response_object = {'status': 'success'}
    #     print(request.data)
    #
    #     post_data = request.get_json()
    #     state_type = post_data.get("state_type")
    #     phone = post_data.get('phone_number')
    #     username = post_data.get('username')
    #     password = post_data.get('password')
    #     if state_type =="register sms":
    #         self.pre_register_get_veritify_code(phone)
    #         return jsonify({'status': 'success'})
    #
    #     elif state_type=="before register":
    #         private_key, public_key = generate_key()
    #         self._CRYPTO[username] = {'private_key': private_key, 'public_key': public_key}
    #         public_key = self._CRYPTO[username]['public_key']
    #         print('====before register:public_key=====')
    #         print(type(public_key))
    #         # print(str(public_key))
    #
    #         return public_key
    #
    #     elif state_type=="register info":
    #         print("====register====")
    #         print("username: %s"%(username))
    #         regisiterdata = post_data.get('registerdata')
    #         print("=======registerdata========")
    #         print(regisiterdata)
    #         result_decrypy = rsa_decrypy(self._CRYPTO[username]['private_key'],regisiterdata)
    #         print("======result_decrypy=========")
    #         print(result_decrypy)
    #         result_decrypy = str(result_decrypy).split("\"")[1]
    #         print(result_decrypy.split("||||"))
    #         password = result_decrypy.split("||||")[0]
    #         veritify_code = result_decrypy.split("||||")[1]
    #         print("======phone number=====")
    #         print(phone,veritify_code)
    #         print(self._PHONE)
    #         if self._PHONE[phone] ==veritify_code:
    #             self._USERINFO[username] = {'password':password,'phone':phone,
    #                                         'verification':'656677','state':'unactive'}
    #             return response_object
    #         else:
    #             return jsonify({'status':'注册失败'})
    #
    #     '''
    #     elif state_type=="register info":
    #         veritify_code = post_data.get('veritify_code')
    #         print("========veritify_code==========")
    #         print(self._PHONE)
    #         print(phone)
    #         print(veritify_code)
    #         print(username)
    #         #TODO:代码有问题：检查self._PHONE[phone] 或者self._USERINFO[username]
    #         if self._PHONE[phone] == str(veritify_code):
    #             self._USERINFO[username] = {'password': password, 'phone': phone,
    #                                         'verification': 'null', 'state': 'unactive'}
    #         print(self._USERINFO)
    #         return jsonify({'status': 'success'})
    #     '''