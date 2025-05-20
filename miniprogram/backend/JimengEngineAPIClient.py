import json
import sys
import os
import base64
import datetime
import hashlib
import hmac
import requests


class VolcEngineAPIClient:
    def __init__(self, access_key, secret_key, host='visual.volcengineapi.com', region='cn-north-1', service='cv'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host
        self.region = region
        self.service = service
        self.endpoint = f'https://{host}'
        self.method = 'POST'
        self.res = ''

    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def get_signature_key(self, key, date_stamp, region_name, service_name):
        k_date = self.sign(key.encode('utf-8'), date_stamp)
        k_region = self.sign(k_date, region_name)
        k_service = self.sign(k_region, service_name)
        k_signing = self.sign(k_service, 'request')
        return k_signing

    def format_query(self, parameters):
        request_parameters_init = ''
        for key in sorted(parameters):
            request_parameters_init += key + '=' + parameters[key] + '&'
        request_parameters = request_parameters_init[:-1]
        return request_parameters

    def sign_v4_request(self, req_query, req_body):
        if self.access_key is None or self.secret_key is None:
            print('No access key is available.')
            sys.exit()

        t = datetime.datetime.utcnow()
        current_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope
        canonical_uri = '/'
        canonical_querystring = req_query
        signed_headers = 'content-type;host;x-content-sha256;x-date'
        payload_hash = hashlib.sha256(req_body.encode('utf-8')).hexdigest()
        content_type = 'application/json'
        canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + self.host + \
            '\n' + 'x-content-sha256:' + payload_hash + \
            '\n' + 'x-date:' + current_date + '\n'
        canonical_request = self.method + '\n' + canonical_uri + '\n' + canonical_querystring + \
            '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'HMAC-SHA256'
        credential_scope = date_stamp + '/' + self.region + '/' + self.service + '/' + 'request'
        string_to_sign = algorithm + '\n' + current_date + '\n' + credential_scope + '\n' + hashlib.sha256(
            canonical_request.encode('utf-8')).hexdigest()
        signing_key = self.get_signature_key(self.secret_key, date_stamp, self.region, self.service)
        signature = hmac.new(signing_key, (string_to_sign).encode(
            'utf-8'), hashlib.sha256).hexdigest()

        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + \
            credential_scope + ', ' + 'SignedHeaders=' + \
            signed_headers + ', ' + 'Signature=' + signature
        headers = {'X-Date': current_date,
                   'Authorization': authorization_header,
                   'X-Content-Sha256': payload_hash,
                   'Content-Type': content_type
                   }

        request_url = self.endpoint + '?' + canonical_querystring

        print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        print('Request URL = ' + request_url)
        try:
            r = requests.post(request_url, headers=headers, data=req_body)
        except Exception as err:
            print(f'error occurred: {err}')
            raise
        else:
            print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
            print(f'Response code: {r.status_code}\n')
            resp_str = r.text.replace("\\u0026", "&")
            #print(f'Response body: {resp_str}\n')
            resp_dict = json.loads(resp_str)
            return  str(resp_dict["data"]["binary_data_base64"])[2:-2]

    #调用
    def send_request(self, query_params, body_params):
        formatted_query = self.format_query(query_params)
        formatted_body = json.dumps(body_params)
        self.res = self.sign_v4_request(formatted_query, formatted_body)
        return self.res
    def base64_to_image(self, save_dir, file_name, file_extension='jpg'):
        """
        将 base64 格式的字符串转换为图片并保存到指定目录。
        文件名由外部传入。

        :param save_dir: 保存图片的目录路径
        :param file_name: 文件名（不包含扩展名）
        :param file_extension: 图片文件的扩展名，默认为 'jpg'
        """
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        # 构造完整的文件路径
        filename = f"{file_name}.{file_extension}"
        output_path = os.path.join(save_dir, filename)

        # 解码 base64 字符串
        try:
            image_data = base64.b64decode(self.res)
        except Exception as e:
            print(f"解码 base64 字符串时出错: {e}")
            return

        # 将解码后的二进制数据写入文件
        try:
            with open(output_path, "wb") as image_file:
                image_file.write(image_data)
            print(f"图片已成功保存到 {output_path}")
            return output_path  # 返回保存的文件路径
        except Exception as e:
            print(f"保存图片时出错: {e}")
