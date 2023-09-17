import requests
from bs4 import BeautifulSoup
import json

def get_latest_release_id():
    url = "https://pib.gov.in/indexd.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    release_list = soup.find("ul", class_="release_list")
    latest_release_id = 0

    for li in release_list.find_all("li"):
        text = li.get_text().strip()
        if len(text) > 15:
            url_release = li.find("a")["href"]
            release_id = int(url_release.split("PRID=")[1].split("&")[0])
            latest_release_id = max(latest_release_id, release_id)
            print(latest_release_id)
    # return latest_release_id

def get_release(id):
    latest_release_id = get_latest_release_id()
    if not id:
        release_url = f"https://pib.gov.in/PressReleasePage.aspx?PRID={latest_release_id}"
    else:
        release_url = f"https://pib.gov.in/PressReleasePage.aspx?PRID={id}"

    response = requests.get(release_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    release_heading = soup.find("h2").get_text()
    release_subtitle = soup.find("span", id="ltrSubtitle")
    if release_subtitle:
        release_subtitle = release_subtitle.get_text().strip()

    posted_by = soup.find("div", class_="ReleaseDateSubHeaddateTime text-center pt20")
    if posted_by:
        posted_by = posted_by.get_text().strip()

    tables = []
    table_counter = 1
    # for table in soup.find_all("table"):
    #     table.replace_with(f"<i>Table {table_counter}</i>")
    #     tables.append(str(table))
    #     table_counter += 1
    p_content= []
    p_text_set=set()
    for p in soup.find_all("p"):
        text = p.text.strip()
        if text and text not in p_text_set:
            p_content.append(text)
            p_text_set.add(text)
    p_content=p_content[:-2]
    
    # p_with_images = soup.find_all("p", recursive=True)
    # image_links = []
    # image_text_set=set()
    # for p_tag in p_with_images:
    #     img_tags = p_tag.find_all("img")
    #     if img_tags:
    #         for img_tag in img_tags:
    #             image_links.append(img_tag["src"])
    unique_image_links = set()

    # Find all <p> tags that contain <img> tags
    p_with_images = soup.find_all("p", recursive=True)

    for p_tag in p_with_images:
        img_tags = p_tag.find_all("img")
        if img_tags:
            for img_tag in img_tags:
                src = img_tag.get("src")
                if src:
                    unique_image_links.add(src)

    release_languages = {}
    languages_div = soup.find("div", class_="ReleaseLang")
    if languages_div:
        for link in languages_div.find_all("a", target="_blank"):
            release_languages[link.text.strip()] = link["href"]

    release_id = soup.find("span", id="ReleaseId").get_text(strip=True)

    data = {
        "pageURL": release_url,
        "releaseHeading": release_heading,
        "release_id":release_id,
        # "releaseSubheading": release_subtitle,
        "postedOn": posted_by,
        # "releaseContentHTML": str(soup.find("div", class_="pt20")),
        # "tables": tables,
        "paragraph":p_content,
        "imageList": unique_image_links,
        "releaseLanguages": release_languages,
    }
    return data
    # print(data)


    # return json.dumps({"data": data})
# get_latest_release_id()
# 

# @app.route("/")
# def index():
#     release_id = request.args.get("id", "")
#     return get_release(release_id)

# if __name__ == "__main__":
#     app.run()
