# GetHref.py
"""
a small tool chain to extract, modify & output all hyperlinks on a website.

## Function List:
1. DepthCounter(): a function to analyse depth/level of an absolute URL string
2. Rel2Abs(): converts relative addresses like './index.php' or '../index.php' to absolute addresses like 'www.baidu.com/news/index.php',
3. GetAllHref(): get all hyper links as a list from an assigned URL



"""
# ----------------
# dependencies
import urllib.request  # pull HTML from website
import urllib.parse  # processing url
from bs4 import BeautifulSoup  # user-friendly HTML filter & parser
import codecs  # for multi-language I/O
# ----------------
def DepthCounter(URLStr):
    """
    a function to analyse depth/level of an **absolute** URL string.
    receives an URL string e.g. "http://news.ifeng.com/a/20181112/60156625_0.shtml",
    counts '/' to determine depth of the URL (e.g. depth = 3 for this example, where depth of 'news.ifeng.com' is 0);
    returns an integer DepthVal;
    """
    # 1. type assertion
    if not isinstance(URLStr, str):
        raise TypeError("requires a string")
    # 2. count
    DepthVal = len( urllib.parse.urlsplit(URLStr) )  # depth = 0 for root URL like "www.baidu.com"

    return DepthVal
# ----------------
def Rel2Abs(RelURLStr,PaterURL):
    """
    converts relative addresses like './index.php' or '../index.php' or '/index.php' to absolute addresses like 'www.baidu.com/news/index.php',
    requiring a father URL like 'www.baidu.com/news' or 'www.baidu.com/news/' (http & https part can be ignored);
    if one-layer ('./'), PaterURL should be one layer; if two-layer backed ('../'), PaterURL should be also two-layer backed; 
    for reference from root layer, ParerURL should be a root address like "https://www.baidu.com"
    supports multi-layer backed.
    returns a string AbsURLStr.

    (in Chinese) 也就是说无论几个点，还是直接一道'/'引用根目录，PaterURL都要对应级别的。下面给出一个非常具体的例子：
    ## Example:
    考虑这样一个多层的链接结构 consider a multi-layer address：'https://www.baidu.com/news/finance/2018/index001.htm'
    1. if RelURLStr = "./index001.htm", it is euqal to "https://www.baidu.com/news/finance/2018/index001.htm"; then requires PaterURL = "https://www.baidu.com/news/finance/2018/" or "https://www.baidu.com/news/finance/2018"
    2. if RelURLStr = "../index001.htm", it is equal to "https://www.baidu.com/news/finance/index001.htm"; them requires PaterURL = "https://www.baidu.com/news/finance/" or "https://www.baidu.com/news/finance"
    3. if RelURLStr = "/index001.htm", it is equal to ""https://www.baidu.com/index001.htm"; then requires PaterURL  = "https://www.baidu.com" or "https://www.baidu.com/"
    """
    # 1. validation
    if not ( isinstance(RelURLStr, str) | isinstance(PaterURL, str) ):
        raise TypeError("requires strings")
    # 2. join urls
    AbsURLStr = ''
    if RelURLStr[0] == '/':  # because urllib.parse.urljoin cannot deal with the case to an absolute address
        tmpPater = PaterURL[:-1] if PaterURL[-1] == "/" else PaterURL[:]
        AbsURLStr = tmpPater + RelURLStr
    else:
        AbsURLStr = urllib.parse.urljoin(PaterURL, RelURLStr)  # otherwise, use urljoin() for relative URLs starting with dots
        
    return AbsURLStr
# ----------------
def GetAllHref(URLstr, encoding = "urf-8"):
    """
    returns a list of all hyperlinks on the website of input URL;
    receives an URL string, returns a list of string (hyperlinks);
    however, the function does not deal with relative refrences
    """
    # 1. validation
    if not isinstance(URLstr, str):
        raise TypeError("requires a string URL")
    # 2. pull HTML texts
    tmpHTMLstr = urllib.request.urlopen(URLstr).read()
    # 3. parse html string
    SoupIns = BeautifulSoup(tmpHTMLstr, "html.parser", from_encoding= encoding )  # use "utf8" for Chinese websites
    # 4. select all hyperlinks (with tag 'a')
    AllLinks = SoupIns.findAll('a')
    AllLinksClean = []
    for x in AllLinks:
        if 'href' in x.attrs.keys(): # because some empty 'a' tags may not have a 'href=' attribute, so we drop those links
            AllLinksClean.append(x['href'])
    # NOTE: data processing is in another function
    return AllLinksClean
# ----------------
def unique( List ):
    """
    a R-style unique() method to get a compact set of a list
    return a compact set/list (only unique elements) of input list :List
    """
    Res = [List[0]]
    for x in List:
        if x not in Res:
            Res.append(x)
    return Res










