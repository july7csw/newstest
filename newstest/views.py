#-*- coding:UTF-8 -*-

import pickle
import numpy as np
from django.shortcuts import render


def replytest(request):
    resultText = ""
    replyText = ""
    if request.method == "POST":
        reply = request.POST['reply']
        label = est(reply)[0]
        acc = est(reply)[1]
        replyText = reply
        resultText = "결과: " + label + " / 정확도: " + str(acc) + "%"
    else:
        replyText = ""
        resultText = ""
    return render(request, 'newstest/replytest.html', {"resultText" : resultText, "replyText" : replyText})

def est(text):
    pcklFile = open("estimate01.pkl", "rb")
    piclf = pickle.load(pcklFile)
    text = [text]
    label = {0: '부정', 1: '중립', 2: '긍정'}
    return label[piclf.predict(text)[0]], np.max(piclf.predict_proba(text) * 100)

