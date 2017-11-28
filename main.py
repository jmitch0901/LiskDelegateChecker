import os
from lxml import html
import requests

liskAddress = ''

page = requests.get('http://earnlisk.com/')
tree = html.fromstring(page.content)


delegateNames = tree.xpath('//td/text()')[0::2]
delegatePayouts = tree.xpath('//td/text()')[1::2]

delegateNames.pop()
delegatePayouts.pop()


# Best delegates to vote for are in this array
delegatePayoutData = []

for x in range(0, len(delegateNames)):
    data = dict(payout=delegatePayouts[x], name=delegateNames[x])
    delegatePayoutData.append(data)


print '\nNumber of Delegates: ', len(delegateNames)


liskExplorerURL = 'https://explorer.lisk.io/api/getAccount?address=' + liskAddress

# My current voted delegates
votedDelegates = requests.get(liskExplorerURL).json()['votes']

myVoteSet = set()
for x in votedDelegates:
    myVoteSet.add(x['username'])

missingVotes = []

for x in delegatePayoutData:
    if not x['name'] in myVoteSet:
        missingVotes.append(x)
    else:
        myVoteSet.remove(x['name'])

print '\n**********Missing Votes: \n'

for x in missingVotes:
    print x['name'] + '->' + x['payout']

print '\n**********Current Bad Votes: \n'

for x in myVoteSet:
    print str(x)

print '\n'
