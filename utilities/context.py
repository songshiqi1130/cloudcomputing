

# TODO
# This is a placeholder for getting information out of the environment, vault, ... ...


__context = {
    "AWSInfo": {
        "aws_access_key_id": "AKIASF6EH44YJUUTLVX5",
        "aws_secret_access_key": "lMkPw/5fY2WzJwXiFZZjkiGxybD4QdDLnO0X4wmK",
        "region_name": "us-east-2"
    }
}

def get_ctx_element(e_name):

    return __context.get(e_name, None)