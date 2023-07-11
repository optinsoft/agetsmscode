# Async API wrapper for getsmscode

## Installation

```bash
pip install git+https://github.com/optinsoft/agetsmscode.git
```

## Usage

```python
from agetsmscode import AsyncGetSmsCode
import asyncio

async def test(apiUsername: str, apiToken: str):
    agetsms = AsyncGetSmsCode(apiUsername, apiToken, 'https://api.getsmscode.com/do.php')
    print("login\n", await agetsms.login())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test('PUT_YOUR_API_USERNAME_HERE', 'PUT_YOUR_API_TOKEN_HERE'))
```
