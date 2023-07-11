from .asyncgetsmscode import AsyncGetSmsCode, AsyncGetSmsCodeException, NoSMSException
from typing import Coroutine

async def testApi(apiName: str, apiRoutine: Coroutine):
    print(apiName)
    try:
        response = await apiRoutine
        print(response)
        return response
    except NoSMSException:
        print("No SMS")
    except AsyncGetSmsCodeException as e:
        print("AsyncGetSmsCodeException:", e)
    return None

async def testAsyncGetSmsCode(username: str, token: str, endpoint: str = 'https://api.getsmscode.com/do.php', cocode: str = ''):
    agetsms = AsyncGetSmsCode(username, token, endpoint)

    print('--- agetsmscode ---')

    await testApi('login', agetsms.login())
    await testApi('projectList', agetsms.projectList())
    await testApi('mobileList', agetsms.mobileList())
    pid = '1'
    number = await testApi('getNumber', agetsms.getNumber(pid, cocode))
    if number:
        await testApi('mobileList', agetsms.mobileList())
        await testApi('getSMS', agetsms.getSMS(pid, number['number'], cocode))
        await testApi('addBlack', agetsms.addBlack(pid, number['number'], cocode))

    print('--- agetsmscode test completed ---')