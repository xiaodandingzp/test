from flask import Flask, jsonify, request
import requests
import jwt
import datetime

from db import init_db, get_user_by_openid, create_user

app = Flask(__name__)

# JWT 密钥
JWT_SECRET = "your_secret_key_here"
JWT_ALGORITHM = "HS256"


def generate_token(openid):
    """生成 JWT Token"""
    payload = {
        "openid": openid,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token):
    """验证 JWT Token，返回解析后的 payload，无效返回 None"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# 初始化数据库
init_db()

@app.route('/test')
def index():
    return jsonify(True)

@app.route('/products')
def products():
    return jsonify([
        {"name": "商品一", "price": 10},
        {"name": "商品二", "price": 20}
    ])


@app.route('/login', methods=['POST'])
def wechat_login():
    """微信登录接口"""
    data = request.get_json()
    # 打印data日志
    print("wechat_login  data: ", data)
    code = data.get('code')
    appid = data.get('appid')

    if not code or not appid:
        return jsonify({"error": "缺少必要参数"}), 400

    # 读取 AppSecret
    try:
        from AppSecret import AppSecret
    except ImportError:
        return jsonify({"error": "AppSecret 配置错误"}), 500

    # 请求微信接口换取 openid 和 session_key
    wx_url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={AppSecret}&js_code={code}&grant_type=authorization_code"
    try:
        wx_response = requests.get(wx_url)
        wx_data = wx_response.json()
    except Exception as e:
        return jsonify({"error": f"请求微信接口失败: {str(e)}"}), 500

    if 'errcode' in wx_data:
        return jsonify({"error": f"微信接口错误: {wx_data.get('errmsg')}"}), 400

    openid = wx_data.get('openid')
    session_key = wx_data.get('session_key')

    if not openid:
        return jsonify({"error": "无法获取 openid"}), 400

    # 根据 openid 查找或创建用户
    user = get_user_by_openid(openid)
    if not user:
        # 创建新用户，用户名为 openid 的值
        create_user(openid, openid)
        user = (openid, openid)

    # 生成 JWT Token
    token = generate_token(openid)

    return jsonify({
        "token": token,
        "username": user[1]
    })


@app.route('/userinfo', methods=['GET'])
def get_userinfo():
    """获取用户信息接口"""
    # 从请求头中获取 token
    token = request.headers.get('Authorization')
    print("get_userinfo  token: ", token)

    if not token:
        return jsonify({})

    # 验证 token
    payload = verify_token(token)
    if not payload:
        return jsonify({})

    # 从 token 中获取 openid
    openid = payload.get('openid')
    if not openid:
        return jsonify({})

    # 根据 openid 获取用户信息
    user = get_user_by_openid(openid)
    if not user:
        return jsonify({})

    return jsonify({
        "username": user[1]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
