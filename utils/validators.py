def validate_user_data(data):
    if not data:
        return False, "Missing JSON body"
    if 'name' not in data or not data['name']:
        return False, "Name is required"
    if 'email' not in data or not data['email']:
        return False, "Email is required"
    if 'password' not in data or not data['password']:
        return False, "Password is required"
    return True, None
