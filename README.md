# Gym Statics Crawler

This app is built to crawl statistics data from Taipei sport center websites, including the number of people in gyms and swimming pools.

To Crawl data, the client secret key is needed to pass the validation from Google and obtain credentials to access Google resources, which in this case is Google Spread Sheets.

To regarly and automatically run this app, it is uploaded to the cloud server provider: Heroku. With the help of its scheduling task, this app will be executed by scheduling worker every 10 minutes, since this is the first scheduling job in my account, it's completely free, but there's also a drawback that it is not stable in its executiion time, delays happen all the time. However, delays are acceptable due to the purpose of this app is simply for observing number of people in sport centers, no accuracy is needed.