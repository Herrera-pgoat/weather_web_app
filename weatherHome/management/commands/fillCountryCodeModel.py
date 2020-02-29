import requests
from django.core.management.base import BaseCommand
from weatherHome.models import countryAndCode
import pandas as pd

#Class Name: Command
#fills the table of countryAndCode with the correct country code for the country names
#grabs iso 3166 codes from wikipedia table and uses panda to clean up tables to be beautiful
class Command(BaseCommand):
	#Function Name: handle
    def handle(self, *args, **options):
        #i need to figure out a way to run this when I want to. Just so that it can do my work for me not so that I can reuse it 
        #link that has table of iso 3661 country codes <-two char countryCOde
        wikiLink = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
        #Getting the html of the thing and saving it as a text
        url = requests.get(wikiLink).text

        #does something
        dataFrame = pd.read_html(url,header=0)[0]

        #getting a series that has all country names and twoCharCountryCodes
        usefulInfo = dataFrame[['ISO 3166[1]','ISO 3166-1[2]']]

        for index, info in usefulInfo.iterrows():
            #if this country satisfies that the coutnry code is two long then they can be a real character
            if isinstance(info[1],str) and len(info[1]) == 2 :
                #I think I should also make the info[1] lowercase but it might not really matter 
                countryCodeInstance = countryAndCode.objects.create(countryName = info[0],twoCharCountryCode = info[1])
                countryCodeInstance.save()
            #otherwise we don't save it because it doesn't have a two character code
		