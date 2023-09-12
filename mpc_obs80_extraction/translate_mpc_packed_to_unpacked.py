
Char=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
		,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','~' ]


#test code has been written for all of this for provid and permid
def packed_to_unpacked( provid = None, permid = None): #only translate one

    #print (provid, permid)

    #start with permid
    if permid != None:
        firstLetter = permid[0]
        if firstLetter.isnumeric(): #if the first value is a number then the number must below 99,999

            return provid, int( permid )
        
        else:
            
            lastFour = permid[1:5]
            firstValueFound = False
            for i in range( 0, len( Char ) ):
                if Char[i] == firstLetter:
                    firstValue = i + 10
                    firstValueFound = True
                    break

            if firstValueFound == False:
                raise ValueError(f"Value {permid} first digit is not currently regonized")
            
            #print (lastFour, firstLetter, firstValue)
            permid = (firstValue * 10000) + int( lastFour )

            return provid, permid
        
    else: #nowthe provid section is below

        if provid[0] == 'J':
            firstValue = '19'
        elif provid[0] == 'K':
            firstValue = '20'

        secondValue = provid[1:3] #get the trailing two digits from the year

        thridValue = provid[3] #get the first charcter after the year

        fourValue = provid[6] #the 7th value will be the last value in the packed

        #get the number converisions.
        value = provid[4]
        if value.isnumeric(): #if the five value is a number then it is not a triple digit
            
            lastValue = provid[4:6]

        else: #this means the fifth charcater is not a number and therefore a tripple digit

            conv = provid[4]
            for i in range( 0, len( Char ) ):
                if Char[i] == conv:
                    convLetter = i + 10
                    break

            lastValue = str( convLetter ) + provid[5]

            #print ('lastValue', lastValue)

        
        provid = firstValue + secondValue + ' ' + thridValue + fourValue + lastValue

        
        return provid, permid


        

    
