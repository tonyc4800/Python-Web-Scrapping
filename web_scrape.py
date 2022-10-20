import requests, pandas
from bs4 import BeautifulSoup

# Gets webpage contents and convert to Beautifulsoup
r = requests.get("https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content
soup = BeautifulSoup(c, "html.parser")

# Gets all list of the page numbers used for the site, which will be cycled through in for loop below
all = soup.find_all("div", {"class":"propertyRow"})
all[0].find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")
page_num = soup.find_all("a", {"class":"Page"})[-1].text


# Extracts all the data about each house into a dictionary
house_listings = []
base_url = "https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_num)*10,10):
    # print(base_url + str(page)) 
    r = requests.get(base_url + str(page))
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})
    for item in all:
        d = {}    
        d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text 
        try:
            d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            pass
        d["Price"] = item.find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")
        try:
            d["Beds"] = item.find("span", {"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = None
        try:
             d["Area"] =item.find("span", {"class":"infoSqFt"}).find("b").text
        except:
             d["Area"] =None
        try:
             d["Full Baths"] = item.find("span", {"class":"infoValueFullBath"}).find("b").text
        except:
             d["Full Baths"] = None
        try:
            d["Half Baths"] = item.find("span", {"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None
        for col_grp in item.find_all("div", {"class":"columnGroup"}):
            for ft_grp, ft_name in zip(col_grp.find_all("span", {"class":"featureGroup"}),col_grp.find_all("span", {"class":"featureName"})):
                if "Lot Size" in ft_grp.text:
                    d["Lot Size"] = ft_name.text
        house_listings.append(d)

# Converts the dictionary into a pandas dataframe to then be written as a csv file.
df = pandas.DataFrame(house_listings)
df.to_csv("output.csv")