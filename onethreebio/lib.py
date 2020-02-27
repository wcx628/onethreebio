import requests
from bs4 import BeautifulSoup

# Drug query main function
def create_drugurl(drug_id):
    
    # Set base url
    baseurl = "https://drugbank.ca/drugs/"
    
    # logic for creating drugurl
    drugurl = baseurl+drug_id
    
    return drugurl


def process_drugurl(drugurl):
    '''Go to drugurl to get target gene information
    use requests and beautifulsoup
    '''
    
    # Get page
    page = requests.get(drugurl)

    # Check connectivity
    count = 1
    while page.status_code // 100 != 2 and count<=5:
        print("unable to connect to " + drugurl)
        print("attempt " + str(count))
        page = requests.get(drugurl)
        count += 1

    if page.status_code // 100 != 2:
        print("attempt to connect to " + drugurl + " failed")
        return None, 404

    # Process page
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find target container
    results = soup.find("div", class_='bond-list-container targets')

    if not results:
        print("no targets found for " + drugurl[-7:])
        return None, 405

    # Find tables in target container
    target_tables = results.find_all("dl")

    if not target_tables:
        print("no tables found in targets session for " + drugurl[-7:])
        return None, 405

    # Get gene names for this drug_id
    res = []
    
    for i,table in enumerate(target_tables):
        table_dt = []
        table_dd = []
        for item in target_tables[i].find_all("dt"):
            table_dt.append(item.text)
        for item in target_tables[i].find_all("dd"):
            table_dd.append(item.text)

        # If not able to find gene in this table, continue
        if "Gene Name" not in table_dt:
            continue

        # Store the gene value in the table
        for tag, value in zip(table_dt, table_dd):
            if tag == "Gene Name":
                res.append(value)
                    
    return res, 200
