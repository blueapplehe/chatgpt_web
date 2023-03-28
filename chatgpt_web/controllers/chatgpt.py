from django.http import JsonResponse
from django.http import HttpRequest
import openai
import json
import logging
import re
import os
logger = logging.getLogger("django")


def getArticle(request: HttpRequest):
    openai.api_key=os.environ.get("CHATGPT_KEY","")
    getdata = request.GET
    question = getdata.get("question")
    temperature = getdata.get("temperature")
    if question is None:
        postData = json.loads(request.body)
        question = postData.get("question")
        temperature = postData.get("temperature")
    if temperature is None:
        temperature = 0
    temperature = float(temperature)
    if temperature > 2.0:
        temperature = 2.0
    elif temperature < 0.0:
        temperature = 0.0
    logger.info("问题:"+str(question))
    error_code = 0
    message = ""
    data = {}
    choices = []
    img_url=""
    try:
        response = openai.Completion.create(
            model="text-davinci-003", prompt=question, temperature=float(temperature), top_p=1, n=1, max_tokens=3000)
        choices = response.choices
        article = response.choices[0].text
        logger.info("答:"+str(article))
        data = article
        img = re.findall(r'\[(.*?)\]\((.*?)\)', data)
        if len(img) > 0:
            img_url=img[0][1]
    except Exception as e:
        message = str(e)
        error_code = -1
    result = {"error_code": error_code, "message": message,
              "data": data, "choices": choices,"img_url":img_url}
    return JsonResponse(result)
