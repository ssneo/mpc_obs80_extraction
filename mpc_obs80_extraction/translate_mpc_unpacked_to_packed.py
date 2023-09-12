

Char=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
		,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','~' ]


#this function has a full set of test functions for provid and permid
def unpacked_to_packed( provid = None, permid = None): #only translate one

    #print (provid, permid)

    #start with permid
    if permid != None:

        if int(permid) <= 99999: #do nothing, the number is under 99,999
            permid = str( permid ).zfill(5)

            return provid, permid
        
        else:
            permidStr = str( permid )

            #get the numbers before the last 4 digits
            lastFour = permidStr[-4:]

            beginingValues = permidStr[0:-4]

            value2Use = int( beginingValues ) - 10

            #print ('value2Use', value2Use)
            

            begV = Char[ value2Use ]

            permid = begV + lastFour

            return provid, permid
        
    else: #nowthe provid section is below

        if provid[0:2] == '19':
            firstValue = 'J'
        elif provid[0:2] == '20':
            firstValue = 'K'

        secondValue = provid[2:4] #get the trailing two digits from the year

        thridValue = provid[5] #get the first charcter after the year

        lastValue = provid[6] #the 7th value will be the last value in the packed

        #get the number converisions.

        if len(provid) == 7: #this is a length with no numbers which are assumed to be zero '1984 EN'
            provid = firstValue + secondValue + thridValue + '00' + lastValue

        elif len(provid) == 8: #this is a length with only one number so the other is assumed to be a zero '1984 EN1'
            provid = firstValue + secondValue + thridValue + '0' + provid[7] + lastValue

        elif len(provid) == 9: #this is a normal length object '1984 EN10'
            provid = firstValue + secondValue + thridValue + provid[7:9] + lastValue

        elif len(provid) == 10: #this is a tripple number objects '1984 EN123'
            conv = int( provid[7:9] ) - 10
            convLetter = Char[ conv ]
            provid = firstValue + secondValue + thridValue + convLetter + provid[9] + lastValue

        else:
            raise ValueError(f'Length of Provid {provid} is not currently regconized')
        
        return provid, permid


        






    