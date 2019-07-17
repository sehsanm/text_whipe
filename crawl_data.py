import os
import threading
from selenium import webdriver
from PIL import Image

DRIVER = 'chromedriver'


def get_screenshot(driver, url, output_name):
    print(url)
    driver.get(url)
    screenshot = driver.save_screenshot(output_name + '.png')
    driver.execute_script("var style = document.createElement('style');"
                          "style.innerHTML ='*{color: transparent!important;} ::-webkit-input-placeholder{color: transparent!important;}';"
                          "var ref = document.querySelector('script');"
                          "ref.parentNode.insertBefore(style, ref);")
    screenshot = driver.save_screenshot(output_name + '_whiped.png')


def crwal_website(driver, base_url, site_id, restricted_domain , max_page=100):
    queue = []
    crawled = set()
    driver.get(base_url)
    queue.append(base_url)

    while len(crawled) < max_page and len(queue) > 0:
        pop = queue.pop(0)
        if pop in crawled:
            continue
        try:
            get_screenshot(driver, pop, './data/' + site_id + '_' + str(len(crawled)))

            links = driver.find_elements_by_tag_name('a')
            for l in links:
                href = l.get_attribute('href')
                if href is None:
                    continue
                href = href.split('#')[0]  # stips out inner links
                if len(href) > 0 and href.find(restricted_domain) > -1:
                    queue.append(l.get_attribute('href'))
                else:
                    print(href)
        except Exception as e:
            print('Skipping URL:', pop, ' Error:', e)
        crawled.add(pop)

def unify_sizes(input_folder, files, width, height, from_right=True):
    for f in files:
        image = Image.open(input_folder + '/' + f)
        print(image.size)
        if from_right:
            cropped = image.crop((image.size[0] - width, 0, image.size[0], height))
        else:
            cropped = image.crop(0, 0 , width , height)
        cropped.save(input_folder + '/croppped_' + f)


def crop_files(input_folder):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(input_folder):
        for file in f:
            if '.png' in file:
                files.append(file)
    unify_sizes(input_folder, files, 2074, 1444)


def thread_run(site_id, base_url, restricted_domain,  count):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1500 , 3000)
    crwal_website(driver, base_url, site_id, restricted_domain, count)
    driver.quit()

if __name__ == "__main__":
    # driver = webdriver.PhantomJS("node_modules/.bin/phantomjs.cmd")
    # driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome(DRIVER)
    # crwal_website(driver, 'https://fa.wikipedia.org', 'wiki', 1000)
    #
    sites = {
        'wiki': {'url': 'https://fa.wikipedia.org' , 'count': 5 , 'restriction' : 'https://fa.wikipedia.org'},
        'blogfa' : {'url' : 'http://blogfa.com' , 'count' : 5, 'restriction' : 'blogfa.com'},
        'irna' : {'url' : 'https://www.irna.ir/' , 'count' : 5, 'restriction' : 'https://www.irna.ir/'},
        'ganjoor' : {'url' : 'https://ganjoor.net/' , 'count' : 5, 'restriction' : 'https://ganjoor.net/'},
        'bbc' : {'url' : 'https://www.bbc.com/persian' , 'count' : 5, 'restriction' : 'www.bbc.com/persian'}
    }
    for s in sites:
        threading.Thread(target=thread_run, args=(s, sites[s]['url'], sites[s]['restriction'], sites[s]['count'])).start()