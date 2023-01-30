from django.shortcuts import redirect, render
from webapp.forms import UserImageForm
from webapp.models import UploadImage
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse
from pickle import dump, load
from .training_caption_generator import train_data
from keras.applications.xception import Xception, preprocess_input
from keras.utils import pad_sequences
from keras.models import Model, load_model

def extract_features(filename, model):
    try:
        image = Image.open(filename)
    except:
        print('error')
        return None
    image = image.resize((299, 299))
    image = np.array(image)

    if image.shape[2] == 4:
        image = image[..., :3]
    image = np.expand_dims(image, axis=0)
    image = image/127.5
    image = image - 1.0
    feature = model.predict(image)
    return feature

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen = max_length)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text

def generate_caption(filename):
    max_length = 32
    tokenizer = load(open('tokenizer.pkl', 'rb'))
    model = load_model('models/model_9.h5')
    xception_model = Xception(include_top=False, pooling='avg')
    # img_path = 'media/images' + '/' + filename
    # print(img_path)
    photo = extract_features(filename, xception_model)
    img = Image.open(filename)
    description = generate_desc(model, tokenizer, photo, max_length)
    return description

def home(request):
    description = None
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            img_object = request.FILES['image'].name
            filename = 'media/images' + '/' + img_object
            description = generate_caption(filename)
            # max_length = 32
            # tokenizer = load(open('tokenizer.p', 'rb'))
            # model = load_model('models/model_9.h5')
            # xception_model = Xception(include_top=False, pooling='avg')

            # photo = extract_features(img_object.image.name, xception_model)
            # # img = Image.open(img_object.image.url)

            # description = generate_desc(model, tokenizer, photo, max_length)

            # def extract_features(filename, model):
            #     try:
            #         image = Image.open(filename)
            #     except:
            #         print('error')
            #     image = image.resize((299, 299))
            #     image = np.array(image)

            #     if image.shape[2] == 4:
            #         image = image[..., :3]
            #     image = np.expand_dims(image, axis=0)
            #     image = image/127.5
            #     image = image - 1.0
            #     feature = model.predict(image)
            #     return feature

            # def word_for_id(integer, tokenizer):
            #     for word, index in tokenizer.word_index.items():
            #         if index == integer:
            #             return word
            #     return None


            # def generate_desc(model, tokenizer, photo, max_length):
            #     in_text = 'start'
            #     for i in range(max_length):
            #         sequence = tokenizer.texts_to_sequences([in_text])[0]
            #         sequence = pad_sequences([sequence], maxlen = max_length)
            #         pred = model.predict([photo, sequence], verbose=0)
            #         pred = np.argmax(pred)
            #         word = word_for_id(pred, tokenizer)
            #         if word is None:
            #             break
            #         in_text += ' ' + word
            #         if word == 'end':
            #             break
            #     return in_text
                
                

        return render(request, 'home.html', {'form': form, 'img_obj': img_object, 'description': description})
    form = UserImageForm()
    return render(request, 'home.html', {'form': form})
