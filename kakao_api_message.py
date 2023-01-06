import requests
import json

def get_accesstoken():
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = '자신의 rest api key'
    redirect_uri = '자신의 redirect uri'  # 보통은 http://example.oauth.com
    authorize_code = '발급받은 authorization code'

    parameter = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }

    response = requests.post(url, data=parameter)  # post 형태로 요청
    tokens = response.json()
    print("token is : ")
    print()
    print(tokens)

    # json 저장

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)

    return tokens

def get_friend_list():
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friend_list = requests.get(friend_url, headers=headers)
    friend_list = friend_list.json()

    # json 저장
    with open("friend_list.json", "w") as fp:
        json.dump(friend_list, fp)

    friends_list = result.get("elements")
    print("friend_list is : ")
    print()
    print(friend_list)

    friend_uuid = []

    for i in range(result.get("total_count")): #total count 자신의 애플리케이션에 등록된 친구 수 만큼 uuid를 가져옴
        friend_uuid.append(friends_list[i].get("uuid"))

    return friend_uuid

def send_msg(friend_uuid, template_id):


    for i in range(len(friend_uuid)):
        send_url = "https://kapi.kakao.com/v1/api/talk/friends/message/send"
        parameter = {
            'receiver_uuids': '["{}"]'.format(friend_uuid[i]),
            "template_id": str(template_id)
        }
        response = requests.post(send_url, headers=headers, data=parameter)
        if response.status_code != 200:
            print(response.text)
            raise Exception("ERROR [send_msg]")
        print('ok!!')

def token_info():
    token_info_url = "https://kapi.kakao.com/v1/user/access_token_info"
    response = requests.get(token_info_url, headers=headers)
    result = json.loads(response.text)
    print("token_info is ", result)
    token_expire = result.get("expires_in")
    print("token_expire : " , token_expire)

def update_token():
    token_update_url = "https://kauth.kakao.com/oauth/token"
    parameter = {
           "grant_type": "refresh_token",
           'client_id' : 'rest api key',
           'refresh_token':"발급받은 refresh token"
           }
    response = requests.post(token_update_url, data=parameter)
    result = json.loads(response.text)
    updated_token = result.get("access_token")
    updated_refresh_token = result.get("refresh_token")
    print("updated_token is : ", updated_token)
    print("updated_refresh_token is : ", updated_refresh_token)

if __name__ == '__main__':
    tokens = get_accesstoken()
    headers = {"Authorization": "Bearer " + '발급받은 access token'}
    friend_uuid = get_friend_list()
    send_msg(friend_uuid, 82349)
    token_info()
    update_token()












