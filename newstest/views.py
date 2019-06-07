#-*- coding:UTF-8 -*-

import pickle
import numpy as np
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


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

def getlink(request):
    medias = ["경향신문", "국민일보", "동아일보", "서울신문", "세계일보", "조선일보", "중앙일보", "한겨레신문", "디지털타임스", "매일경제", "머니투데이", "서울경제",
              "전자신문", "파이낸셜뉴스", "한국경제", "한국일보"]
    mediacodes = ["032", "005", "020", "081", "022", "023", "025", "028", "029", "009", "008", "011", "030", "014",
                  "015", "469"]
    articlelinks = []

    for mc in mediacodes:
        url = "https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=" + mc
        html = getHtml(url)
        firstlist = html.find("ul", {"class": "firstlist"})
        naverlink = firstlist.findAll("a")
        naverlink = naverlink[1].get("href")
        html2 = getHtml(naverlink)
        sponsor = html2.find("div", {"class": "sponsor"})
        articlelink = sponsor.find("a").get("href")
        articlelinks.append(articlelink)
    # context = {'medias': medias, 'articlelinks':articlelinks}
    return render(request, 'newstest/getlink.html', {'medias': medias, 'articlelinks':articlelinks})

def getHtml(url):
    r = requests.get(url)
    c = r.content
    html = BeautifulSoup(c, "html.parser")
    return html