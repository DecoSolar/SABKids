from nudes import contain_nudity
from weapons import detect_weapons
from text_detection import contains_bad_words


def search_and_block(image):
    # image = data # переданное изображение
    result = detect_weapons(image)
    result.append({'nude': contain_nudity(image)})
    result.append({'bad_words': contains_bad_words(image)})
    detect = 1  # 1 = False, 2 = True
    for i in range(0, len(result)):
        for key in result[i]:
            if result[i][key] == True:
                detect = 2
                return detect
    return detect
