import sys
import requests
import bs4
import csv

URL_BASE = "https://volby.cz/pls/ps2017nss/"


def scrape_villages(url):
    parsed_page = get_parsed_page(url)
    village_info_header_items = ["Číslo obce", "Obec"]#get_village_info_header_items(parsed_page)
    village_details_header_items = None
    villages_info = get_villages_info(parsed_page)
    scrapped_villages = []
    for village_info in villages_info:
        village_url = village_info[2]
        village_parsed_page = get_parsed_page(village_url)
        if village_parsed_page.find("div", class_="in_940"):
            district_urls = get_district_urls(village_parsed_page)
            merged_village_to_write = []
            for district_url in district_urls:
                village_parsed_page = get_parsed_page(district_url)
                village_details_header_items = get_village_details_header_items(village_parsed_page)
                village_details = get_village_details(village_parsed_page)
                village_to_write = village_item_to_write(village_info, village_details)
                if not merged_village_to_write:
                    merged_village_to_write = village_to_write
                else:
                    merged_village_to_write = merge_village_items(merged_village_to_write, village_to_write)
            scrapped_villages.append(merged_village_to_write)
        else:
            village_details_header_items = get_village_details_header_items(village_parsed_page)
            village_details = get_village_details(village_parsed_page)
            village_to_write = village_item_to_write(village_info, village_details)
            scrapped_villages.append(village_to_write)
    header_items = village_item_to_write(village_info_header_items, village_details_header_items)
    scrapped_villages.insert(0, header_items)
    return scrapped_villages


def get_parsed_page(url):
    response = get_page_from_url(url)
    return parse_page(response.text)


def get_page_from_url(url):
    try:
        response = requests.get(url)
    except:
        quit("Invalid URL")
    else:
        if response.status_code != 200:
            quit("Response status code not OK")
        return response


def parse_page(page):
    try:
        soup = bs4.BeautifulSoup(page, "html.parser")
        return soup
    except:
        quit("Cannot parse page")


# Vraci seznam obci - (kod, nazev, URL)
def get_villages_info(parsed_page):
    try:
        villages = []
        villages_tables = parsed_page.find("div", id="inner").find_all("table")
        for village_table in villages_tables:
            rows = village_table.find_all("tr")
            for row in rows:
                village_code_tag = row.find("td", class_="cislo")
                village_name_tag = row.find("td", class_="overflow_name")
                village_link_tag = row.find("td", class_="center")
                if village_code_tag:
                    villages.append(
                        (village_code_tag.a.text, village_name_tag.text, URL_BASE + village_link_tag.a['href']))
        return villages
    except:
        quit("Get village info error")


# Vraci hlavicky pro prvni 2 polozky
def get_village_info_header_items(parsed_page):
    try:
        table = parsed_page.find("div", id="inner").find("table")
        header_item_code = table.find("th", class_="fixed45", id="t1sb1").text
        header_item_name = table.find("th", class_="fixed150", id="t1sb2").text
        return header_item_code, header_item_name
    except:
        quit("Get village header info error")


# Vraci seznam okrsku v obci - URL
def get_district_urls(parsed_page):
    try:
        districts = []
        districts_tables = parsed_page.find("div", id="publikace").find_all("table")
        for district_table in districts_tables:
            district_tags = district_table.find_all("td", class_="cislo")
            if district_tags:
                for district_tag in district_tags:
                    districts.append(URL_BASE + district_tag.a['href'])
        return districts
    except:
        quit("Get district urls error")


# Vraci detail obce - (pocet volicu, pocet vydanych obalek, pocet platnych hlasu, seznam kandidujicich stran)
def get_village_details(parsed_page):
    try:
        table = parsed_page.find("table")
        header_item_voters_count = table.find("td", class_="cislo", headers="sa2").text
        header_item_envelops_count = table.find("td", class_="cislo", headers="sa3").text
        header_item_valid_votes_count = table.find("td", class_="cislo", headers="sa6").text
        parties = get_parties(parsed_page)
        return header_item_voters_count, header_item_envelops_count, header_item_valid_votes_count, parties
    except:
        quit("Get villages detail error")


def get_village_details_header_items(parsed_page):
    try:
        voters_count = "Voliči v seznamu"
        envelops_count = "Vydané obálky"
        valid_votes_count = "Platné hlasy"
        parties_header_items = get_parties_header_items(parsed_page)
        return voters_count, envelops_count, valid_votes_count, parties_header_items
    except:
        quit("Get villages detail header items error")


def get_parties(parsed_page):
    try:
        parties = []
        parties_tables = parsed_page.find("div", id="inner").find_all("table")
        for table_index in range(len(parties_tables)):
            parties_table = parties_tables[table_index]
            rows = parties_table.find_all("tr")
            for row in rows:
                table_number = table_index + 1
                headers = "t" + str(table_number) + "sa2 t" + str(table_number) + "sb3"
                party_valid_votes_tag = row.find("td", class_="cislo", headers=headers)
                if party_valid_votes_tag:
                    parties.append(party_valid_votes_tag.text)
        return parties
    except:
        quit("Get parties error")


def get_parties_header_items(parsed_page):
    try:
        parties_header_items_names = []
        parties_tables = parsed_page.find("div", id="inner").find_all("table")
        for table_index in range(len(parties_tables)):
            parties_table = parties_tables[table_index]
            rows = parties_table.find_all("tr")
            for row in rows:
                table_number = table_index + 1
                headers = "t" + str(table_number) + "sa1 t" + str(table_number) + "sb2"
                party_header_item_name_tag = row.find("td", class_="overflow_name", headers=headers)
                if party_header_item_name_tag:
                    parties_header_items_names.append(party_header_item_name_tag.text)
        return parties_header_items_names
    except:
        quit("Get parties header items error")


def village_item_to_write(village_info, village_details):
    items = [village_info[0], village_info[1], village_details[0], village_details[1], village_details[2]]
    for item in village_details[3]:
        items.append(item)
    return items


def merge_village_items(old_village_items, new_village_items):
    village_items = old_village_items
    for index in range(2, len(new_village_items)):
        village_items[index] = str(
            int("".join(old_village_items[index].split())) + int("".join(new_village_items[index].split())))
    return village_items


def write_to_file(items, csv_file_name):
    try:
        file = open(csv_file_name + ".csv", 'w')
        try:
            file_writer = csv.writer(file, delimiter=",")
            file_writer.writerows(items)
        except:
            print("Writing to file error")
        finally:
            file.close()
    except:
        print("Open file error")


if __name__ == "__main__":
    try:
        url = str(sys.argv[1])
        csv_file_name = str(sys.argv[2])
    except:
        quit("Arguments error")
    else:
        if not url or not csv_file_name:
            quit("Empty URL or file name")
        else:
            villages_to_write = scrape_villages(url)
            write_to_file(villages_to_write, csv_file_name)
