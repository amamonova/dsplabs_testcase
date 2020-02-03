import face_recognition
import os


def check_face(image_path, new_filename):
    """
    Function checks if there a face in a photo.
    :param image_path: path to downloaded image.
    :param new_filename: new filename with order number.
    :return: True if the face is detected else False
    """
    image = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(image)

    if face_landmarks_list:
        os.rename(image_path, new_filename)
        return True
    else:
        os.remove(f'{image_path}')
        return False
