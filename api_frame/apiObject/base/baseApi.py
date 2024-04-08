import os
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from api_frame.config import ApiConfig
from ui_frame.config import UiConfig
from api_frame.utils.rsa_util import RsaUtil
from api_frame.conftest import get_user_account_conftest
from api_frame.utils.TimeoutHTTPAdapter import TimeoutHTTPAdapter


DEFAULT_TIMEOUT = ApiConfig.timeout

source_dir = os.getcwd()
if source_dir.find("ui_frame") > -1:
    base_url = UiConfig.base_url.split("//")[-1]
    filename = UiConfig.filename
    testdata_dir = UiConfig.testdata_dir
else:
    base_url = ApiConfig.baseurl
    filename = ApiConfig.filename
    testdata_dir = os.path.join(ApiConfig.API_FRAME_PATH, "testData")


class BaseApi():

    account_data = get_user_account_conftest()
    name = account_data[0][0]
    username = account_data[1][0]
    password = account_data[2][0]

    def baseurl(self):
        return base_url

    @classmethod
    def http_timeout(cls, timeout=DEFAULT_TIMEOUT):
        timeout = timeout or DEFAULT_TIMEOUT
        http = requests.Session()
        # 把配置复制给http和https请求
        adapter = TimeoutHTTPAdapter(timeout=timeout)
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    @classmethod
    def get_PHPSESSID(cls):
        PHPSESSID = cls.login_api(username=cls.username, password=cls.password)
        return PHPSESSID

    @classmethod
    def login_api(self, username='13800138006', password='123456', verify_code='aaaa', **kwargs):
        """
        testingedu登录
        :param username:
        :param password:
        :param verify_code:
        :param kwargs:
        :return:
        """
        domain = base_url if not kwargs.get('domain') else kwargs.get('domain')
        url = f'http://{domain}/index.php?m=Home&c=User&a=do_login&t=0.010459923089728207'
        if kwargs.get('is_https') == False:
            url = url.replace('https', 'http')
        headers = {
            'Content-Type': 'text/html; charset=UTF-8'
        }
        payload = {
            'username': username,
            'password': password,
            'verify_code': verify_code
        }
        response = requests.request("POST", url, headers=headers, params=payload)
        assert response.status_code == 200, f"testingedu登录失败，resp:{response.text}"
        return response.json()['result']['token']

    def get_user_account(self, file_name=filename):
        '''获取人员帐号信息'''
        user_file_path = os.path.join(testdata_dir, file_name)
        user_file = open(user_file_path, 'r', encoding="UTF-8")
        users = user_file.readlines()
        name = []
        username = []
        password = []
        remark = []
        teams = []
        for u in users:
            name.append(u.split(',')[0].strip())
            username.append(u.split(',')[1].strip())
            password.append(u.split(',')[2].strip())
            remark.append(u.split(',')[3].strip())
            teams.append(u.split(',')[4].strip())
        return name, username, password, remark, teams

    def get_value(self, data, list_key=["data", "data"], **kwargs):
        """
        从数据中获取值，如果不存在抛出断言错误
        :param data: 取值对象，可以是字典或列表
        :param list_key: 取值列表，可以从字典取key,也可以列表取下标，可传递非列表会转成列表
        :param kwargs: msg=异常提示信息，不传默认提示："数据{}不存在取值'{}'！"
        :return:
        """
        key=""
        data_msg = ""
        if not isinstance(list_key, list):
            list_key = [list_key]
        try:
            if len(list_key) > 1:
                data_msg = f"原始数据:{data};"
            for key in list_key:
                data = data[key]
            return data
        except:
            msg = "数据{}不存在取值'{}'！{}".format(data, key, data_msg)
            if kwargs.get("msg"):
                msg = "{}:{}".format(kwargs.get("msg"), msg)
            assert False, msg

    def get_json_dict(self, data, key, value):
        """
        获取满足key=value的json中的字典
        :param data:
        :param key:
        :param value:
        :return:
        """
        matches = []
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key and v == value:
                    matches.append(data)
                else:
                    ret = self.get_json_dict(v, key, value)
                    if ret is not None:
                        matches.extend(ret)
        elif isinstance(data, list):
            for item in data:
                ret = self.get_json_dict(item, key, value)
                if ret is not None:
                    matches.extend(ret)
        return matches if matches else None

    def sha1_encrypt(self, text):
        """使用sha1加密"""
        # 创建SHA-1对象
        sha = hashlib.sha1()
        # 将文本转换为字节类型并更新到SHA-1对象中
        sha.update(text.encode('utf-8'))
        # 获取加密后的结果（十六进制表示）
        encrypted_text = sha.hexdigest()
        return encrypted_text

    def md5_encrypt(self, text):
        """使用md5加密"""
        # 创建一个MD5对象
        md5 = hashlib.md5()
        # 将文本转换为字节类型并进行编码
        text = text.encode('utf-8')
        # 更新MD5对象的内容
        md5.update(text)
        # 获取16进制表示的结果（默认大写）
        result = md5.hexdigest().lower()
        return result

    def encrypt_aes_ecb(self, plain_text, key):
        """AES-ECB加密"""
        key = key.encode()
        plain_text = plain_text.encode()
        cipher = AES.new(key, AES.MODE_ECB)
        padded_data = pad(plain_text, AES.block_size)
        ct_bytes = cipher.encrypt(padded_data)
        ct_base64 = base64.b64encode(ct_bytes).decode('utf-8')
        return ct_base64

    def decrypt_aes_ecb(self, ciphertext, key):
        """aes-ecb解码"""
        # ciphertext如果是requests请求拿到的数据，需要使用response.content获取body内容，不能和response信息一起传递过来
        key = key.encode()
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(base64.b64decode(ciphertext))
        return plaintext.decode('utf-8')

    def encrypt_aes_cbc(self, plain_text, key, iv):
        """aes-cbc加密"""
        # plain_text需要转换的文本内容，key是加密密钥，iv是偏移量
        # 创建AES对象
        key = key.encode()
        plain_text = plain_text.encode()
        iv = iv.encode()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 对明文进行填充
        block_size = 16
        padding_length = block_size - len(plain_text) % block_size
        padded_plain_text = plain_text + bytes([padding_length] * padding_length)
        # 加密数据
        cipher_text = cipher.encrypt(padded_plain_text)
        # # 将密文和初始化向量进行Base64编码
        cipher_text_b64 = base64.b64encode(cipher_text).decode('utf-8')
        # iv_b64 = b64encode(iv).decode('utf-8')
        return cipher_text_b64

    def decrypt_aes_cbc(self, ciphertext, key, iv):
        """aes-cbc解码"""
        # ciphertext如果是requests请求拿到的数据，需要使用response.content获取body内容，不能和response信息一起传递过来
        # ciphertext需要转换的文本内容，key是加密密钥，iv是偏移量
        # 解码Base64编码的密文和初始化向量
        cipher_text = base64.b64decode(ciphertext)
        key = key.encode()
        iv = iv.encode()
        # 创建AES对象
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 解密数据
        plain_text = cipher.decrypt(cipher_text)
        # 去除填充
        padding_length = plain_text[-1]
        plain_text = plain_text[:-padding_length]
        return plain_text

    def encrypt_aes_cfb(self, plain_text, key, iv, segment_size=128):
        """aes-cfb加密"""
        # plain_text需要转换的文本内容，key是加密密钥，iv是偏移量， segment_size==密钥长度
        # 创建AES对象
        key = key.encode()
        plain_text = plain_text.encode()
        iv = iv.encode()
        cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=segment_size)# segment_size==密钥长度
        # 加密数据
        cipher_text = cipher.encrypt(plain_text)
        # 将密文和初始化向量进行Base64编码
        cipher_text_b64 = base64.b64encode(cipher_text).decode('utf-8')
        return cipher_text_b64

    def decrypt_aes_cfb(self, ciphertext, key, iv, segment_size=128):
        """aes-cfb解码"""
        # ciphertext如果是requests请求拿到的数据，需要使用response.content获取body内容，不能和response信息一起传递过来
        # ciphertext需要转换的文本内容，key是加密密钥，iv是偏移量，， segment_size==密钥长度
        # 解码Base64编码的密文和初始化向量
        key = key.encode()
        iv = iv.encode()
        cipher_text = base64.b64decode(ciphertext)
        # iv = base64.b64decode(iv)
        # 创建AES对象
        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=segment_size)
        # 解密数据
        decrypted_data = cipher.decrypt(cipher_text)
        return decrypted_data

    def update_public_key(self, publicKey, privateKey):
        """public_key增加begin和end"""
        pem_start = '-----BEGIN RSA PUBLIC KEY-----'
        pem_end = '-----END RSA PUBLIC KEY-----'
        pub_keys_value = pem_start + "\n" + publicKey + "\n" + pem_end
        private_keys_value = pem_start + "\n" + privateKey + "\n" + pem_end
        pub_key = RSA.import_key(pub_keys_value)
        private_key = RSA.import_key(private_keys_value)
        # 获取公钥和私钥
        public_key = pub_key.publickey().export_key()
        private_key = private_key.export_key()
        return public_key, private_key

    def encrypt_rsa(self, plain_text, public_key, private_key):
        """rsa加密"""
        # plain_text 需要加密的字段
        public_key, private_key = self.update_public_key(public_key, private_key) # 密钥转换
        # 数据加密
        encrypt_text = RsaUtil(public_key, private_key).public_long_encrypt(plain_text)
        return encrypt_text

    def decrypt_rsa(self, ciphertext, public_key, private_key):
        """rsa解码"""
        # ciphertext需要解码的数据
        public_key, private_key = self.update_public_key(public_key, private_key) # 密钥转换
        # 数据解码
        decrypt_text = RsaUtil(public_key, private_key).private_long_decrypt(ciphertext)
        return decrypt_text