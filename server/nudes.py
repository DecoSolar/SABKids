from nudenet import NudeDetector

default = ['EXPOSED_BREAST_F', 'EXPOSED_ANUS', 'COVERED_BREAST_F', 'COVERED_GENITALIA_F', 'EXPOSED_GENITALIA_F',
           'EXPOSED_GENITALIA_M', 'COVERED_BELLY', 'COVERED_BUTTOCKS', 'EXPOSED_BUTTOCKS']

detector = NudeDetector()


def contain_nudity(path: str):
    result_detect = detector.detect(path)

    my_values = [l['label'] for l in result_detect]
    result = False
    for i in range(len(default)):
        if default[i] in my_values:
            print(my_values)
            result = True
            print(result)
            break
    print(result)
    return result
