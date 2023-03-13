from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email

pf = PetFriends()

#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#2
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#3
def test_add_new_pet_valid_data(name='Кира', animal_type= 'овчарка', age= '5', pet_photo = 'ovcharki.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type

#4
def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

#5
def test_update_info_about_pet(name='Kira', animal_type='собака', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

#6
def test_add_photo_of_pet(pet_photo = 'maxi.jpg'):
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        if len(my_pets['pets']) > 0:
            status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
            _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
            assert status == 200
            assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        else:
            raise Exception("Питомцы отсутствуют")

#7
def test_new_pet_without_photo(name='Беки', animal_type= 'такса', age= '6'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#8
def test_get_api_key_for_invalid_email_and_invalid_password(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#9
def test_get_api_key_for_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#10
def test_get_api_key_for_invalid_email_and_valid_password(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#11
def test_add_new_pet_empty_value_in_name(name='', animal_type= 'овчарка', age= '5', pet_photo = 'ovcharki.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result['name']

#12
def test_add_new_pet_icct_format_in_age(name='Кара', animal_type= 'овчарка', age= 'страус', pet_photo = 'ovcharki.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result['name']

#13
def test_add_new_pet_with_icct_age(name='Кара',animal_type= 'овчарка', age= '5000'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age

#14
def test_add_new_pet_with_a_long_name_of_101_characters(animal_type= 'овчарка', age= '5'):
    name = 'Кираааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа'
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age

#15
def test_add_a_pet_with_special_characters_in_animal_type(name='Kira', animal_type='!@#$%^&*()_+', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['animal_type'] == animal_type