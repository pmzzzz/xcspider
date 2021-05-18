import requests
import execjs

# 需要的一些环境
BrowserEnvironment = """ 
var window = {};
window.navigator = {};
window.navigator.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/532.36 (KHTML, like Gecko) Chrome/83.0.1127.05 Safari/527.16";
function getCookie() {
    return window.cookie;
}
var document = {
    createElement: function(tag){
        var innerHTML;
        return {
            firstChild: {
                href: "https://www.mafengwo.cn/"
            }
        }
    }
};
window.document = document;
var location = {"href": "https://www.mafengwo.cn/"};
window.location = location;
"""
ASTContext = execjs.compile(open("ast.js", "r",encoding='utf8').read())


def get_content(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/532.36 (KHTML, like Gecko) Chrome/83.0.1127.05 Safari/527.16",
        "cookie": "__jsluid_s=8f0ed86e64be8f70ffe0d9bacbbaaf7f; __jsl_clearance=1597471392.957|0|kwsM9EZXPySOSHcJWP0SyV7vZQ8%3D;"
        # 1597471392.957|0|kws  EZXPySOSHcJWP0SyV7vZQ8%3D
    }
    r = requests.get(url, headers=headers)
    #
    # print(r.text)
    __jsluid_s = r.headers["Set-Cookie"].split(";")[0] + "; "
    cookieStr = __jsluid_s
    # with open("input.js", "w") as f:
    #     f.write(r.text)
    jsCode = ASTContext.call(
        "compile",
        BrowserEnvironment + r.text.strip().strip("<script>").strip("</script>"),
    )
    context = execjs.compile(jsCode)
    jsl_clearance = context.call("getCookie").split(";")[0] + ";"
    cookieStr += jsl_clearance

    headers.update({"cookie": cookieStr})
    r = requests.get(url, headers=headers)
    print(r.text)


get_content("https://www.mafengwo.cn/i/18252205.html")