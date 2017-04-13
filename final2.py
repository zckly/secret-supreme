#!/bin/env python2.7

# Run around 1059 as early as 1055.
# Polling times vary pick something nice.
# Ghost checkout timer can be changed by 
# adjusting for loop range near bottom.
# Fill out personal data in checkout payload dict.

import sys, json, time, requests, urllib2
from datetime import datetime

qty='1'

def UTCtoEST():
    current=datetime.now()
    return str(current) + ' EST'
print
# poll=raw_input("Polling interval? ")
# poll=int(poll)
poll = .5
# keyword=raw_input("Product name? ").title()       # hardwire here by declaring keyword as a string - DISPLAY VALID OPTIONS IN ()
keyword = 'Box Logo Tee'
print 'First Item: ', keyword
#color=raw_input("Color? ").title()                # hardwire here by declaring keyword as a string - DISPLAY VALID OPTIONS IN ()
color = 'White'
#sz=raw_input("Size? ").title()                    # hardwire here by declaring keyword as a string - DISPLAY VALID OPTIONS IN ()
sz = 'Large'
print 
# keyword2=raw_input("Product 2 name? ").title()       # hardwire here by declaring keyword as a string - DISPLAY VALID OPTIONS IN ()
keyword2 = 'Box Logo Hooded'
print 'Second Item: ', keyword2
#color2=raw_input("Color? ").title()                # hardwire here by declaring keyword as a string - DISPLAY VALID OPTIONS IN ()
#sz2=raw_input("Size? ").title() 
color2 = 'Black'
sz2 = 'Large'
print UTCtoEST(),':: Parsing page...'
def main():
    global ID
    global variant
    global cw
    global styleNum
    global myproduct
    global sizeName

    global ID2
    global variant2
    global cw2
    global styleNum2
    global myproduct2
    global sizeName2
    req = urllib2.Request('http://www.supremenewyork.com/mobile_stock.json')
    req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
    resp = urllib2.urlopen(req)
    data = json.loads(resp.read())
    ID=0
    ID2=0
    #u'string' is unicode
    for i in range(len(data[u'products_and_categories'].values())):
        for j in range(len(data[u'products_and_categories'].values()[i])):
            item=data[u'products_and_categories'].values()[i][j]
            name=str(item[u'name'].encode('ascii','ignore'))
            # SEARCH WORDS HERE
            # if string1 in name or string2 in name:
            if keyword in name:
                # match/(es) detected!
                # can return multiple matches but you're 
                # probably buying for resell so it doesn't matter
                myproduct=name                
                ID=str(item[u'id'])
                print UTCtoEST(),'::',name, ID, 'found ( MATCHING ITEM DETECTED )'
            elif keyword2 in name:
                # match/(es) detected!
                # can return multiple matches but you're 
                # probably buying for resell so it doesn't matter
                myproduct2=name                
                ID2=str(item[u'id'])
                print UTCtoEST(),'::',name, ID2, 'found ( MATCHING ITEM DETECTED )'
    if (ID == 0 and ID2 == 0):
        # variant flag unchanged - nothing found - rerun
        time.sleep(poll)
        print UTCtoEST(),':: Reloading and reparsing page...'
        main()
    else:
        if (ID != 0):
          print UTCtoEST(),':: Selecting',str(myproduct),'(',str(ID),')'
          jsonurl = 'http://www.supremenewyork.com/shop/'+str(ID)+'.json'
          req = urllib2.Request(jsonurl)
          req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
          resp = urllib2.urlopen(req)
          data = json.loads(resp.read())
          found=0
          found2=0
          for numCW in data['styles']:
              # COLORWAY TERMS HERE
              # if string1 in numCW['name'] or string2 in numCW['name']:
              if color in numCW['name'].title():
                  styleNum=numCW['id']
                  for sizes in numCW['sizes']:
                      # SIZE TERMS HERE
                      if str(sizes['name'].title()) == sz: # Medium
                          found=1;
                          variant=str(sizes['id'])
                          cw=numCW['name']
                          sizeName=sizes['name']
                          print UTCtoEST(),':: Selecting size:', sizes['name'],'(',numCW['name'],')','(',str(sizes['id']),')'
          if found ==0:
              # DEFAULT CASE NEEDED HERE - EITHER COLORWAY NOT FOUND OR SIZE NOT IN RUN OF PRODUCT
              # PICKING FIRST COLORWAY AND LAST SIZE OPTION
              print UTCtoEST(),':: Selecting default colorway:',data['styles'][0]['name']
              sizeName=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['name'])
              variant=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['id'])
              cw=data['styles'][0]['name']
              styleNum=data['styles'][0]['id']
              print UTCtoEST(),':: Selecting default size:',sizeName,'(',variant,')'
        if (ID2 != 0):
          print UTCtoEST(),':: Selecting',str(myproduct2),'(',str(ID2),')'
          jsonurl2 = 'http://www.supremenewyork.com/shop/'+str(ID2)+'.json'
          req2 = urllib2.Request(jsonurl2)
          req2.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
          resp2 = urllib2.urlopen(req2)
          data2 = json.loads(resp2.read())
          found=0
          for numCW in data['styles']:
              # COLORWAY TERMS HERE
              # if string1 in numCW['name'] or string2 in numCW['name']:
              if color2 in numCW['name'].title():
                  styleNum2=numCW['id']
                  for sizes in numCW['sizes']:
                      # SIZE TERMS HERE
                      if str(sizes['name'].title()) == sz2: # Medium
                          found2=1;
                          variant2=str(sizes['id'])
                          cw2=numCW['name']
                          sizeName2=sizes['name']
                          print UTCtoEST(),':: Selecting size:', sizes['name'],'(',numCW['name'],')','(',str(sizes['id']),')'
          if found2 ==0:
              # DEFAULT CASE NEEDED HERE - EITHER COLORWAY NOT FOUND OR SIZE NOT IN RUN OF PRODUCT
              # PICKING FIRST COLORWAY AND LAST SIZE OPTION
              print UTCtoEST(),':: Selecting default colorway:',data['styles'][0]['name']
              sizeName2=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['name'])
              variant2=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['id'])
              cw2=data['styles'][0]['name']
              styleNum2=data['styles'][0]['id']
              print UTCtoEST(),':: Selecting default size:',sizeName2,'(',variant2,')'
                        
        

main()


session=requests.Session()
if (ID != 0):
  addUrl='http://www.supremenewyork.com/shop/'+str(ID)+'/add.json'
if (ID2 != 0):
  addUrl2='http://www.supremenewyork.com/shop/'+str(ID2)+'/add.json'

addHeaders={
    'Host':              'www.supremenewyork.com',                                                                                                                     
    'Accept':            'application/json',                                                                                                                             
    'Proxy-Connection':  'keep-alive',                                                                                                                                   
    'X-Requested-With':  'XMLHttpRequest',                                                                                                                               
    'Accept-Encoding':   'gzip, deflate',                                                                                                                                
    'Accept-Language':   'en-us',                                                                                                                                        
    'Content-Type':      'application/x-www-form-urlencoded',                                                                                                            
    'Origin':            'http://www.supremenewyork.com',                                                                                                                
    'Connection':        'keep-alive',                                                                                                                                   
    'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',                               
    'Referer':           'http://www.supremenewyork.com/mobile'   
}

addPayload={
    'style' : str(styleNum),
    'size': str(variant),
    'qty':  '1'
}

addPayload2={
    'style' : str(styleNum2),
    'size': str(variant2),
    'qty':  '1'
}
print UTCtoEST() +' :: Adding product to cart...'
addResp=session.post(addUrl,data=addPayload,headers=addHeaders)

print UTCtoEST() +' :: Checking status code of response...'

if addResp.status_code!=200:
    print UTCtoEST() +' ::',addResp.status_code,'Error \nExiting...' #CHECK THIS - DID ITEM ADD TO CART? MAKE POST AGAIN - something like while status != 200 - wait and request again
    print
    sys.exit()
else:
    if addResp.json()==[]: #FIGURE OUT WHY EMPTY JSON RESPONSE 
        print UTCtoEST() +' :: Response Empty! - Problem Adding to Cart\nExiting...'  #CHECK THIS - DID ITEM ADD TO CART? MAKE POST AGAIN
        print
        sys.exit()
    assert addResp.json()[0]["in_stock"]==True,"Error Message: Not in stock"
    #assert addResp.json()[0]["size_id"]==str(variant),"Error Message: Incorrect variant returned in response"
    print UTCtoEST() +' :: '+str(myproduct)+' - '+str(cw)+' - '+str(sizeName)+' added to cart!'
    print UTCtoEST() +' :: Adding product 2 to cart...'
    addResp2=session.post(addUrl2,data=addPayload2,headers=addHeaders)
    print UTCtoEST() +' :: Checking status code of response...'
    if addResp2.status_code != 200:
      print UTCtoEST() +' ::',addResp.status_code,'Error \nExiting...' #CHECK THIS - DID ITEM ADD TO CART? MAKE POST AGAIN - something like while status != 200 - wait and request again
      print
      sys.exit()
    else:
      if addResp2.json()==[]: #FIGURE OUT WHY EMPTY JSON RESPONSE 
          print UTCtoEST() +' :: Response Empty! - Problem Adding to Cart\nExiting...'  #CHECK THIS - DID ITEM ADD TO CART? MAKE POST AGAIN
          print
          sys.exit()
      assert addResp2.json()[0]["in_stock"]==True,"Error Message: Not in stock"
      #assert addResp2.json()[0]["size_id"]==str(variant2),"Error Message: Incorrect variant returned in response"
      print UTCtoEST() +' :: '+str(myproduct2)+' - '+str(cw2)+' - '+str(sizeName2)+' added to cart!'

    
    checkoutUrl='https://www.supremenewyork.com/checkout.json'
    checkoutHeaders={
        'host':              'www.supremenewyork.com',
        'If-None-Match':    '"*"',
        'Accept':            'application/json',                                                                                                                             
        'Proxy-Connection':  'keep-alive',                                                                                                                                   
        'Accept-Encoding':   'gzip, deflate',                                                                                                                                
        'Accept-Language':   'en-us',                                                                                                                                        
        'Content-Type':      'application/x-www-form-urlencoded',                                                                                                            
        'Origin':            'http://www.supremenewyork.com',                                                                                                                
        'Connection':        'keep-alive',                                                                                                                                   
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',                               
        'Referer':           'http://www.supremenewyork.com/mobile'   
    }

    #################################
    # FILL OUT THESE FIELDS AS NEEDED
    #################################
    captchaResponse = "" #Put captcha token string here
    checkoutPayload={
        'store_credit_id':          '',      
        'from_mobile':              '1',
        'cookie-sub':               '%7B%22'+str(variant)+'%22%3A1%7D',       # cookie-sub: eg. {"VARIANT":1} urlencoded
        'same_as_billing_address':  '1',                                    
        'order[billing_name]':      'Zack Lee',                              # FirstName LastName
        'order[email]':             'w.zachary.lee@gmail.com',                    # email@domain.com
        'order[tel]':               '713-202-1535',                           # phone-number-here
        'order[billing_address]':   '900 W 23rd St',                        # your address
        'order[billing_address_2]': 'Apt 310',
        'order[billing_zip]':       '78705',                                  # zip code
        'order[billing_city]':      'Austin',                                 # city
        'order[billing_state]':     'TX',                                     # state
        'order[billing_country]':   'USA',                                    # country
        'store_address':            '1',                                
        'credit_card[type]':        'visa',                                   # master or visa or 
        'credit_card[cnb]':         'xxxx xxxx xxxx xxxx',                    # credit card number
        'credit_card[month]':       '04',                                     # expiration month
        'credit_card[year]':        '2019',                                   # expiration year
        'credit_card[vval]':        '999',                                    # cvc/cvv
        'order[terms]':             '0',
        'order[terms]':             '1',
        'g-recaptcha-response':     captchaResponse,
        'is_from_ios_native':       '1'
                
    }
    
    '''
    captchaResponse post here  https://www.google.com/recaptcha/api2/userverify?k=6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz
    {
        v:
        c:
        response:
        t:
        ct:
        bg:
    }

    reponse "uvresp",captchaResponse string
    '''


    # GHOST CHECKOUT PREVENTION WITH ROLLING PRINT
    for i in range(1):
            sys.stdout.write("\r" +UTCtoEST()+ ' :: Sleeping for '+str(5-i)+' seconds to avoid ghost checkout...')
            sys.stdout.flush()
            time.sleep(1)
    print 
    print UTCtoEST()+ ' :: Firing checkout request!'
    checkoutResp=session.post(checkoutUrl,data=checkoutPayload,headers=checkoutHeaders)
    try:
        print UTCtoEST()+ ' :: Checkout',checkoutResp.json()['status'].title()+'!'
    except:
        print UTCtoEST()+':: Error reading status key of response!'
        print checkoutResp.json()
    print 
    print checkoutResp.json()
    if checkoutResp.json()['status']=='failed':
        print
        print '!!!ERROR!!! ::',checkoutResp #CHECK THIS DATA STRUCT FOR KEY
        checkoutPayload.pop("g-recaptcha-response", 0)
        checkoutResp=session.post(checkoutUrl,data=checkoutPayload,headers=checkoutHeaders)
        try:
            print UTCtoEST()+ ' :: Checkout',checkoutResp.json()['status'].title()+'!'
        except:
            print UTCtoEST()+':: Error reading status key of response!'
            print checkoutResp.json()
        print
        print checkoutResp.json()
        if checkoutResp.json()['status']=='failed':
            print
            print '!!!fuck!!! ::',checkoutResp #CHECK THIS DATA STRUCT FOR KEY

    print
