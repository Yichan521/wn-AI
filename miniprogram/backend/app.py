from flask import Flask, request, jsonify,send_from_directory
import requests
import os
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
#jimeng-api类调用
from JimengEngineAPIClient import VolcEngineAPIClient

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "deepseek-ai/DeepSeek-V3"
SYSTEM_PROMPT = """
你是“文案大师”，一位拥有超过20年经验的顶尖营销专家和广告文案撰稿人。你的专长在于洞察产品核心价值，并将其转化为能够触动人心、激发购买欲望的文字。你深谙消费者心理，擅长运用各种修辞手法和叙事技巧，为不同类型的产品量身打造专属的爆款文案。

你的任务是：根据用户提供的【产品名】、【产地】、【产品特色/优势】、【产品描述】以及可选的【目标受众】和【期望风格/调性】，创作一篇引人入胜且具有高度说服力的产品宣传文案。

输出规范：
1.  **纯文本格式**：你的回答必须严格为纯文本，绝对禁止使用任何Markdown格式（如标题、加粗、斜体、列表符号`*`、`-`、`>`等）。
2.  **直接文案输出**：直接提供最终生成的宣传文案内容。不要包含任何前言（例如“好的，这是为您生成的文案：”）、解释、自我介绍、总结、或任何与文案本身无关的客套话。
3.  **聚焦核心卖点**：文案应突出产品的核心特色和独特优势，清晰传达能为消费者带来的价值。
4.  **引人入胜**：文案应具有吸引力，能够迅速抓住潜在客户的注意力。
5.  **说服力强**：文案应具有说服力，能够激发消费者的购买欲望或行动意愿。
6.  **语言精炼**：在保证信息完整和吸引力的前提下，力求文字简洁、有力。

请等待用户提供具体的产品信息，然后你将直接开始创作。

"""


def build_prompt(data):
    return f"""产品名：{data.get('productName')}
产地：{data.get('productOrigin')}
产品特色/优势：{data.get('productFeature')}
产品描述：{data.get('productDesc')}
请根据以上信息生成一篇引人入胜的产品宣传文案。"""

@app.route('/api/gen_copy', methods=['POST'])
def gen_copy():
    data = request.json
    prompt = build_prompt(data)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers)
    if resp.status_code == 200:
        result = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"result": result})
    else:
        print(f"[ERROR] OpenAI API调用失败: 状态码={resp.status_code}, 响应={resp.text}")
        return jsonify({"result": "生成失败，请稍后重试"}), 500

@app.route('/api/gen_social_copy', methods=['POST'])
def gen_social_copy():
    data = request.json
    social_system_prompt = "你是一个小说家，能够根据产品名、产地、产品卖点编写一篇能挑起读者情绪（愤怒或者激动）的文章，结尾峰回路转提及我们的产品，使用纯文本回复"
    prompt = f"""产品名：{data.get('productName')}
产地：{data.get('productOrigin')}
产品卖点：{data.get('productSellingPoint')}
请根据以上信息生成一篇带货文案。"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": social_system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers)
    if resp.status_code == 200:
        result = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"result": result})
    else:
        print(f"[ERROR] OpenAI API调用失败: 状态码={resp.status_code}, 响应={resp.text}")
        return jsonify({"result": "生成失败，请稍后重试"}), 500
"""
===============================================================================================================
海报部分
"""
# 配置海报保存目录
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化 jimeng-api
jimeng_ak = os.getenv("JIMENG_AK")
jimeng_sk = os.getenv("JIMENG_SK")
volc_engine_client = VolcEngineAPIClient(jimeng_ak, jimeng_sk)

#海报生成调用
@app.route('/generate_poster', methods=['POST'])
def generate_poster():
    try:
        # 获取前端传递的参数
        data = request.json
        if not data:
            return jsonify({"status": 400, "message": "Invalid request data"}), 400

        prompt = data.get('prompt')

        # 构造请求参数
        query_params = {
            'Action': 'CVProcess',
            'Version': '2022-08-31',
        }

        body_params = {
            "req_key": "jimeng_high_aes_general_v21_L",
            "prompt": prompt
        }

        # 调用 VolcEngineAPIClient 发送请求
        response = volc_engine_client.send_request(query_params, body_params)

        # 假设 response 是一个 base64 编码的字符串
        if not response:
            return jsonify({"status": 500, "message": "Failed to generate image"}), 500

        # 动态生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_image_{timestamp}"

        # 调用 base64_to_image 方法保存图片
        saved_path = volc_engine_client.base64_to_image(app.config['UPLOAD_FOLDER'], filename)

        if not saved_path:
            return jsonify({"status": 500, "message": "Failed to save image"}), 500

        # 生成图片 URL
        image_url = f"/uploads/{os.path.basename(saved_path)}"

        # 返回结果
        return jsonify({
            "status": 200,
            "result": image_url  # 返回图片的 URL
        })

    except Exception as e:
        return jsonify({"status": 500, "message": "Internal Server Error", "error": str(e)}), 500

#图片读取
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
"""
================================================================================================================
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 