from django.shortcuts import render
from django.http import HttpResponse
import feedparser
import string
import urllib2
from BeautifulSoup import BeautifulSoup

# Create your views here.

def linkContent(url):
    output = ""
    try:
        content = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return output

    html = content.read()

    paragraph = BeautifulSoup(''.join(html)).find('p')

    print paragraph

    if paragraph is not None and paragraph.string is not None:
        output += paragraph.string + "<br/>\n"

    return output


def parseLinks(msg):
    output = ""

    ustart = string.find(msg, "http://")

    while ustart != -1:
        url = msg[ustart:].split("&")[0]
        ustart += len(url)
        ustart = string.find(msg[ustart:], "http://")
        output += "<a href='" + url + "'>" + url + "</a><br/>\n"
        output += linkContent(url)

    return output

def main(request, resource):

    parsedrss = feedparser.parse("http://twitrss.me/twitter_user_to_rss/"
                            + "?user=" + resource)
    output = ""
    for index in range(5):
        tweet = parsedrss.entries[index].summary + "<br/>\n"
        output += tweet + parseLinks(tweet) + "<br/>\n"

    return HttpResponse(output)
