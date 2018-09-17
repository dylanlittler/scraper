# Imports for web.py and scraping and emailing modules of this package

import web
import scraping
import email_handler

render = web.template.render('templates/')


urls = (
    '/', 'index',
    '/stackoverflow', 'stackoverflow'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        return render.index()

class stackoverflow:
    def GET(self):
        scrape_params = web.input() # Gets input from form on index.html
        scrape_data = scraping.search_stackoverflow(scrape_params.url,
                                                    scrape_params.tag, scrape_params.attribute, scrape_params.return_url) # passes results to scraping function
        if hasattr(scrape_params, 'email_results'): # checks if user wants to send email
            email_handler.send_email(scrape_params.from_email,
                                     scrape_params.email_server, scrape_params.password, scrape_params.to_email, scrape_data) # sends email using parameters obtained from index.html
        return render.stackoverflow(scrape_data.items()) # passes key and value returned by search_stackoverflow function to stackoverflow.html

if __name__ == "__main__":
    app.run()
