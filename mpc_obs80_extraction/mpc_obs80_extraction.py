


import psycopg2
from translate_mpc_unpacked_to_packed import unpacked_to_packed


#this function has full testing complete on it
def extract_obs80( provid=None, permid=None ):

    provid, permid, listOfProvids = determineCorrectPermid_Provid( provid=provid, permid=permid )

    #print ('provid', provid)
    #print ('permid', permid)
    #print ('listOfProvids', listOfProvids)

    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "mpc_sbn",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    #now check how the obs_sbn should be searched
    output = None
    if permid != None:

        psql = f"SELECT obs80 from obs_sbn where permid='{permid}' "
        #psql = f"SELECT count(*) from obs_sbn where permid='{permid}' "
        #print ('psql', psql)
        cur.execute( psql )
        
        output = cur.fetchall()

        #print (output)
    
    else: #if listOfSecondary Provids is zero then only one queue
        #print ('loop2')
        if len( listOfProvids) == 0:
            psql = f"SELECT obs80 from obs_sbn where provid='{provid}' "
            #psql = f"SELECT count(*) from obs_sbn where provid='{provid}' "
            cur.execute( psql )
            output = None
            output = cur.fetchall()

        else: #go through the whole list of secondary provid
            output = None
            for i in range( 0, len( listOfProvids ) ):
                psql = f"SELECT obs80 from obs_sbn where provid='{listOfProvids[i]}' "
                #psql = f"SELECT count(*) from obs_sbn where provid='{listOfProvids[i]}' "
                cur.execute( psql )
                if i == 0:
                    output = cur.fetchall()
                else:
                    output += cur.fetchall()

            #at the end, don't forget to get obs from the primary provid

            psql = f"SELECT obs80 from obs_sbn where provid='{provid}' "
            #psql = f"SELECT count(*) from obs_sbn where provid='{provid}' "
            cur.execute( psql )
            output += cur.fetchall()

    


    obs80 = format_obs80( provid=provid, permid=permid, obs80=output )

    #print ('len(obs80)', len(obs80))

    #once you have the output, now you need to get everything formated in obs80 to get ready for findOrb. All same name etc.
            
            
    con.close()

    return len(obs80), obs80, provid, permid

#this function has full testing complete on it
def format_obs80( provid=None, permid=None, obs80=None ):

    #1 make sure all are only 80 characters long
    #2 if permid is not None, replace all of their names with the permid
    #3 if permid is None, replace all of their name with the provid

    newObs80 = []
    for i in range( 0, len( obs80 ) ):
        #print (obs80[i])
        #stop
        if len( obs80[i][0] ) == 80: #make sure obs80 is 80 characters long
            #print ('obs80[i][0]', obs80[i][0])
            if permid != None:
                packed_provid, packed_permid = unpacked_to_packed( permid=permid )
                #print ('packed_permid', packed_permid)
                newLine = packed_permid + '          ' + obs80[i][0][15:] #this removes the K or any other obs character so the sort will be done on time only
                #print ('newLine', newLine)

                newObs80.append( newLine )

            #provid add issue
            else:
                packed_provid, packed_permid = unpacked_to_packed( provid = provid )
                newLine = '     ' + packed_provid + '   ' + obs80[i][0][15:] #this removes the K or any other obs Character so the sort will be done on time only

                #print ('newLine', newLine)

                newObs80.append( newLine )

    #at this point, all of the obs80 names should be the same name. Therefore, sort should be via time of obs only
    newObs80.sort()

    #print (newObs80[0])
    



    return newObs80


#this function has full testing complete on it.
def determineCorrectPermid_Provid( provid=None, permid=None ):

    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "mpc_sbn",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    #There are multiple things that need to be accomplished here to get a complete list.

    #Do not assume anything that a provid is correct or a permid is the lastest etc.
    #If permid is available
    #1) check numbered_identifications that permid is found
        #if True: then pull obs from database with permid
        #if False: search current_identifications and determine if we have the packed_primary_provisional_designation
            #if True: then search for obs with any of the secondary designations
            #if False: search for the pack_primary_provisional_designation:

    #print ('provid, permid', provid, permid)
    listOfProvids = []
    #checking if Permid is valid
    ouput = None
    isPermidFound = False
    if permid != None:

        psql = "SELECT count(*) from numbered_identifications where permid='%s' "%(permid)
        cur.execute( psql )
        output = cur.fetchall()

        if output[0][0] == 1: #if output count is 1, that means permid is correct
            isPermidFound = True
        else:
            if provid != None: #if provid is provided, then skip permid and move onto provid
                pass
            else: #if provid is not provided, then raise a valueError
                raise ValueError(f"Value {permid} is not found in the database and provid is None")





    #If permid is not valid, then switching to provid

    output = None
    isProvidFound = False
    newProvid = None
    if isPermidFound == False:

        #test if provid is a primary provid
        psql = "SELECT count(*) from current_identifications where unpacked_primary_provisional_designation='%s' "%( provid )
        cur.execute( psql )
        output = cur.fetchall()
        #print ('output1', output)
        if output[0][0] != 0: #current identifcations may have the same primary designation multiple times
            isProvidFound = True
            #if this is true, we have the current primary packed designation

        
        else: #we do not have the correct primary provid, we need to then search for the primary id in current identifcation
            psql = "SELECT unpacked_primary_provisional_designation from current_identifications where unpacked_secondary_provisional_designation='%s' "%( provid )
            cur.execute( psql )
            output = cur.fetchall()
            if len( output ) == 0: #this mean an empty list:
                raise ValueError(f"Value {provid} is not found in the database, if permid was provid it was also not found: permid={permid} ")
            
            else:
                if len( output[0] ) == 1: #confirm that the list only contains one value
                    newProvid = output[0][0]
                    isProvidFound = True
                    provid = newProvid
                    #print ('found newProvid', newProvid)
                else:
                    print ('Error, more than one primary designation has been found')

            
    
    #at this point, if permid is found, we are done. If provid is found, we need to check if it has a permid
    #print ('2-> provid, permid', provid, permid)
    if isProvidFound == True:

        psql = f"SELECT permid FROM numbered_identifications where unpacked_primary_provisional_designation='{provid}' "
        cur.execute( psql )
        output = None
        output = cur.fetchall()
        if len( output ) != 0:
            permid = output[0][0] #if we found a permid then we set the permid to that value

        else: #we need to find the list of secondary_prov... because we need to search for them in the database as well.


            #get all of the secondary designations: However, all primary have one with themselves listed as secondary. This queue does not include one where the secondary is the primary
            psql = f"SELECT unpacked_secondary_provisional_designation from current_identifications where unpacked_primary_provisional_designation='{provid}' and unpacked_secondary_provisional_designation!='{provid}' "
            cur.execute( psql )
            output = None
            output = cur.fetchall()
            if len( output ) != 0: #if there is a list of items deal with them, otherwise leave listOfProvids as an empty list
                #print ('output3', output)
                #print ('output3', output[0])
                for i in range(0, len( output[0] ) ):
                    listOfProvids.append( output[0][i] )
                #print ('listOfProvids', listOfProvids)
            
            

    con.close()


    return provid, permid, listOfProvids


if __name__ == '__main__':


    #extract_obs80(permid=600000)
    extract_obs80(provid='2023 NM1')