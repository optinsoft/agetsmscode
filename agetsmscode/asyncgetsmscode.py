import aiohttp
import ssl
import certifi
import json
from urllib.parse import urlencode

class AsyncGetSmsCodeException(Exception):
    pass

class NoSMSException(AsyncGetSmsCodeException):
    pass

class AsyncGetSmsCode:
    def __init__(self, username: str, token: str, endpoint: str = 'https://api.getsmscode.com/do.php'):
        self.username = username
        self.token = token
        self.endpoint = endpoint

    def checkResponse(self, respJson: dict):
        return respJson
    
    async def doRequest(self, url: str, respNames: list, respDelimiter: str = ''):
        if len(respNames) > 1 and respNames[-1].startswith('...'):
            sublistName = respNames[-1][3:]
            respNames = respNames[:-1]
            respNames.append(sublistName)
        else:
            sublistName = ''
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn, raise_for_status=False) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    respText = await resp.text()
                    raise AsyncGetSmsCodeException(f"Request failed:\nStatus Code: {resp.status}\nText: {respText}")
                try:
                    respText = await resp.text()
                    if len(respDelimiter) > 0:
                        respObj = []
                        if len(respText) > 0:
                            x = respText.split(respDelimiter)
                            for t in x:
                                if len(t) > 0:
                                    respValues = t.split('|')
                                    if len(sublistName) > 0 and len(respValues) >= len(respNames):
                                        sublistValues = respValues[len(respNames)-1:]
                                        respValues = respValues[:len(respNames)-1]
                                        respValues.append(sublistValues)
                                    else:
                                        sublistValues = None
                                    if len(respValues) != len(respNames):
                                        raise AsyncGetSmsCodeException(f"Bad response: {respText}")
                                    respObj.append({name: respValues[i] for i, name in enumerate(respNames)})
                    else:
                        respValues = respText.split('|')
                        if len(respValues) != len(respNames):
                            raise AsyncGetSmsCodeException(f"Bad response: {respText}")
                        respObj = {name: respValues[i] for i, name in enumerate(respNames)}
                    respJson = respObj
                except ValueError as e:
                    raise AsyncGetSmsCodeException(f"Request failed: {str(e)}")
                return self.checkResponse(respJson)

    async def login(self):
        url = self.endpoint + '?' + urlencode({'action': 'login', 'username': self.username, 'token': self.token})
        return await self.doRequest(url, ['username', 'balance', 'points', 'discount_rate', 'api_thread'])
    
    async def getNumber(self, pid: str, cocode: str = '', removevr: str = '0'):
        url = self.endpoint + '?' + urlencode({'action': 'getmobile', 'username': self.username, 'token': self.token, 'pid': pid, 'cocode': cocode, 'removevr': removevr})
        return await self.doRequest(url, ['number'])

    async def getSMS(self, pid: str, number: str, cocode: str = '', author: str = ''):
        url = self.endpoint + '?' + urlencode({'action': 'getsms', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number, 'cocode': cocode, 'author': author})
        return await self.doRequest(url, ['code','sms'])

    async def addBlack(self, pid: str, number: str, cocode: str = ''):
        url = self.endpoint + '?' + urlencode({'action': 'addblack', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number, 'cocode': cocode})
        return await self.doRequest(url, ['message','text'])

    async def mobileList(self):
        url = self.endpoint + '?' + urlencode({'action': 'mobilelist', 'username': self.username, 'token': self.token})
        return await self.doRequest(url, ['mobile', 'pid'], ',')

    async def projectList(self, pid: str=''):
        url = 'http://api.getsmscode.com/projectapi.php'
        if len(pid) > 0: url = url + '? ' + urlencode({'pid': pid})
        return await self.doRequest(url, ['pid', 'project_name', '...cc_price'], '<br>')
    