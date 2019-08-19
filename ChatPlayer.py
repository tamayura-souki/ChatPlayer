# -*- coding: utf-8 -*-

# YoutubeChatで遊ぶためのコード

import codecs
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

print('start')

driver.get('https://www.youtube.com/live_chat?is_popout=1&v=Sflq-_arjDg')

for body in [driver.find_element_by_css_selector('yt-live-chat-renderer')]:
    #print(codecs.encode(body.get_attribute('innerHTML'), 'utf-8', 'ignore'))
    print(body.text)

#print(codecs.encode(driver.page_source, 'utf-8', 'ignore'))

driver.save_screenshot('search_results.png')
driver.quit()