from config import CONFIG
from db import get_name, create_conn, insert_data, close_conn, create_db
from voice import convert
from face import check_face

import os
import logging

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode


logging.basicConfig(format=('%(asctime)s - %(name)s - '
                            '%(levelname)s - %(message)s'),
                    level=logging.INFO)
logger = logging.getLogger()


def download_file(update, context, file_type):
    """
    This function downloads files from Telegram.
    :param update:
    :param context:
    :param file_type: `photo` or `voice`. Type of downloaded file.
    :return: old filename and new_filename if file_type is correct else False.
    filename - path to file, new_filename - filename with order number of file
    in database.
    """
    user_id = update.effective_user.id

    if file_type == 'voice':
        file_id = update.message.voice.file_id
        filename = f'{user_id}_voice.ogg'
        path = CONFIG['VOICE_FOLDER_PATH']
    elif file_type == 'photo':
        file_id = update.message.photo[-1].file_id
        filename = f'{user_id}_photo.jpg'
        path = CONFIG['PHOTO_FOLDER_PATH']
    else:
        return False

    new_file = context.bot.get_file(file_id)
    new_file.download(os.path.join(path, filename))

    conn, cursor = create_conn()

    new_filename = os.path.join(path, get_name(cursor, user_id, file_type,
                                               f'{file_type}_path'))

    close_conn(conn)

    return filename, new_filename


def add_handlers(updater):
    """
    This function adds handlers for start and message_processing functions.
    :param updater: an Updater object
    :return: None
    """
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all,
                                                  message_processing))


def start(update, context):
    """
    Function sends reply every time the Bot receives message with
    /start command.
    :return: None
    """
    context.bot.send_message(parse_mode=ParseMode.MARKDOWN,
                             chat_id=update.effective_chat.id,
                             text='I\'m a bot for *DSP Labs* test case. '
                                  'If you send me a *photo* with a face or an '
                                  '*voice message*, I\'ll save it in a DB.')


def message_processing(update, context):
    """
    Function saves voice messages in wav format with simple rate 16MHz and
    photos if a face is detected there. All path store in database `bot`.
    :return: None
    """

    logger.info(f'Waiting for message_processing function for '
                f'{update.effective_user.name} at '
                f'{update.effective_message.date}')

    user_id = update.effective_user.id

    conn, cursor = create_conn()

    if update.message.voice:
        filename, new_filename = download_file(update, context, 'voice')
        new_filename = f'{new_filename}.wav'

        convert(os.path.join(CONFIG['VOICE_FOLDER_PATH'], filename),
                new_filename)

        insert_data(conn, cursor, 'voice', user_id, 'audio_path', new_filename)

        answer_text = 'Thanks, I\'ve saved this voice message to my database.'

    elif update.message.photo:
        filename, new_filename = download_file(update, context, 'photo')
        new_filename = f'{new_filename}.jpg'

        PHOTO_FOLDER_PATH = CONFIG['PHOTO_FOLDER_PATH']

        if check_face(f'{PHOTO_FOLDER_PATH}/{user_id}_photo.jpg',
                      new_filename):
            insert_data(conn, cursor, 'photo', user_id, 'photo_path',
                        new_filename)
            answer_text = ('I saved this photo in the database because I\'ve '
                           'detected the face here.')
        else:
            answer_text = ('I didn\'t save this photo in my database, because '
                           'I haven\'t found the face here.')

    else:
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker=CONFIG['STICKER_PATH'])
        answer_text = 'Send me a voice message or a photo, please.'

    context.bot.send_message(parse_mode=ParseMode.MARKDOWN,
                             chat_id=update.effective_chat.id,
                             text=answer_text)
    close_conn(conn)

    logger.info(f'Answer ready for {update.effective_user.name} '
                f'at {update.effective_message.date}')


def run():
    get_request = requests.get('http://pubproxy.com/api/proxy?limit=1&'
                               'format=txt&port=8080&level=anonymous&'
                               'type=socks5&country=FI|NO|US&'
                               'https=True')
    proxy_response = get_request.text

    if proxy_response != 'No proxy':
        REQUEST_KWARGS = {'proxy_url': f'https://{proxy_response}'}
    else:
        logger.info(
            f"Using proxy by default: "
            f"{CONFIG['DEFAULT_REQUEST_KWARGS']}")
        REQUEST_KWARGS = CONFIG['DEFAULT_REQUEST_KWARGS']

    updater = Updater(CONFIG['TOKEN_ID'],
                      request_kwargs=REQUEST_KWARGS,
                      use_context=True)
    add_handlers(updater)
    updater.start_polling()


if __name__ == '__main__':
    create_db()
    run()
