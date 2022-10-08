from fastapi import FastAPI

from scraper import scrape_content

app = FastAPI()

@app.get('/')
async def root_get():
    return await scrape_content()
