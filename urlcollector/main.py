from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates    
from urlcollector.url_Collect import UrlExtractor, UrlsModel


    

app = FastAPI()     
templates = Jinja2Templates(directory='templates')


@app.post('/inputUrl', response_model=UrlsModel)
def get_url(url: str = Form(...)):

    try:
        extract=UrlExtractor(url)
        extract.get_all_urls()
        extract.driver.quit()
    except Exception as e:
        print("Error: ", e)
        extract.result.urls.append("Error")
        extract.driver.quit()
        
    
    return extract.result 

@app.get("/",response_class=HTMLResponse)
async def main(request: Request):          
    return templates.TemplateResponse('index.html', {'request': request})