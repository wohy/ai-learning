import requests

def test_chat_message_flow():
    # 测试消息创建
    create_url = 'http://localhost:6006/chat/new/message/'
    create_data = {
        'prompt': 'hello',
        'max_tokens': 1000
    }
    create_response = requests.post(create_url, json=create_data)
    assert create_response.status_code == 200
    assert "message_id" in create_response.json()

    # 测试消息获取
    get_url = 'http://localhost:6006/chat/get/messages/'
    get_response = requests.get(get_url)
    assert get_response.status_code == 200
    assert isinstance(get_response.json(), list)