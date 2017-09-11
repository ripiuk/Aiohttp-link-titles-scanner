from aiohttp import web
import aiohttp_jinja2
from testt import main
import os


class Check(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {'lol': 'Some text'}

    @aiohttp_jinja2.template('index.html')
    async def post(self):
        reader = await self.request.multipart()
        csv = await reader.next()
        filename = csv.filename
        size = 0

        if filename == '':
            return web.Response(text='You don`t choose any file')

        with open(os.path.join(os.getcwd() + '/uploaded_data/', filename), 'wb+') as f:
            while True:
                chunk = await csv.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        titles = await main(file='uploaded_data/' + filename)
        return {'result': titles}
