from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import time

import openai
import os
import vobject
import re


# "/start" 라고 입력하면 메뉴가 뜸
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("명함-연락처 변환 서비스", callback_data="namecard")],
        [InlineKeyboardButton("서비스", callback_data="service")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🚨서비스 선택 메뉴", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == "namecard":
        query.edit_message_text("이미지를 첨부해주세요!")
        context.user_data["wait_for_image"] = True

    elif query.data == "service":
        query.edit_message_text("서비스 준비중입니다!")


def main():
    bot_token = "Telegram Bot Token"
    updater = Updater(bot_token, use_context=True)
    bot = updater.bot
    dispatcher = updater.dispatcher

    # 이미지 처리 함수
    def handle_image(update, context):
        message = update.message

        if not context.user_data.get("wait_for_image", False):
            return
        context.user_data["wait_for_image"] = False

        photo = message.photo[-1].file_id

        photo_file = bot.getFile(photo)
        image_path = "image.png"
        photo_file.download(image_path)

        message.reply_text("열심히 변환중 · · ·")

        # ------------------------------------
        # ----------------------- OCR
        # ------------------------------------

        # API Set
        subscription_key = "MS Azure API key"
        endpoint = "MS Azure Endpoint"

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        local_image = open(image_path, "rb")

        read_response = computervision_client.read_in_stream(local_image, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ["notStarted", "running"]:
                break
            time.sleep(1)

        text_results = []
        if read_result.status == OperationStatusCodes.succeeded:
            text_results = [line.text for text_result in read_result.analyze_result.read_results for line in
                            text_result.lines]

        # 메모리 파일 삭제
        os.remove(image_path)

        # ------------------------------------
        # ----------------------- GPT
        # ------------------------------------

        openai.api_key = "GPT API key"
        model = "gpt-3.5-turbo"

        # Message
        messages = [
            {"role": "user", "content": f"{text_results}이 리스트에서 사람이름, 회사이름, 휴대폰번호가 뭐야?"},
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response["choices"][0]["message"]["content"]

        v = vobject.vCard()

        v.add("fn").value = answer.split("\n")[0].split(":")[1]
        v.add("title").value = answer.split("\n")[1].split(":")[1]
        v.add("tel").value = re.sub("[^0-9]", "", answer.split("\n")[2].split(":")[1].strip())

        # vcf 파일로 저장
        vcf_file = v.serialize()
        vcf_path = "contact.vcf"
        with open("contact.vcf", "w", encoding="utf-8") as f:
            f.write(vcf_file)

        message.reply_document(document=open(vcf_path, "rb"), filename="연락처.vcf")

        # 메모리 파일 삭제
        os.remove(vcf_path)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
