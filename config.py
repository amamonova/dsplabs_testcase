"""
TOKEN_ID - an authorization token for your bot
DEFAULT_REQUEST_KWARGS - proxy url for working in Russia
VOICE_FOLDER_PATH - path to saving voice messages
PHOTO_FOLDER_PATH - path to saving photo messages
STICKER_PATH - path to image that sends when the bot gets something except
voice or photo message
DATABASE_NAME - name for creating database
"""

CONFIG = dict(TOKEN_ID='1075047114:AAGfBzoqWfVhfQWYDvyyNU-nZ3TDw0H-ZHI',
              DEFAULT_REQUEST_KWARGS={'proxy_url':
                                      'https://51.38.71.101:8080'},
              VOICE_FOLDER_PATH='voices',
              PHOTO_FOLDER_PATH='photos',
              STICKER_PATH='http://b.webpurr.com/anY5.webp',
              DATABASE_NAME='bot.db')
