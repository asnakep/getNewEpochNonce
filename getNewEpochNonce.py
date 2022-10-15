import json
import requests
import subprocess as sp
import hashlib

BlockFrostId = ""

### newEpochNonce Availability ###
headers      = {'content-type': 'application/json', 'project_id': BlockFrostId}
latestBlocks = requests.get("https://cardano-mainnet.blockfrost.io/api/v0/blocks/latest", headers=headers)
json_data    = latestBlocks.json()
epochSlot    = latestBlocks.json().get("epoch_slot")
currEpoch    = latestBlocks.json().get("epoch")
nextEpoch    = int(currEpoch + 1)

### New epochNonce is not computable
if epochSlot <  302400:

 ### Print Json Data
 data = {}
 data['nextEpoch'] = nextEpoch
 data['nextNonce'] = ""
 jsonData = json.dumps(data, indent=2)
 print(jsonData)
 exit()


### New epochNonce is computable
if epochSlot >= 302400:

 ### Take "candidateNonce" from protocol-state
 candidateNonce = sp.getoutput('cardano-cli query protocol-state --mainnet | jq -r .candidateNonce.contents')

 ### Take "lastEpochBlockNonce" from protocol-state
 lastEpochBlockNonce = sp.getoutput("cardano-cli query protocol-state --mainnet | jq -r .lastEpochBlockNonce.contents")

 ### Extract newEpochNonce
 newEpochNonce = hashlib.blake2b(bytes.fromhex(candidateNonce + lastEpochBlockNonce),digest_size=32).hexdigest()

 ### Print Json Data
 data = {}
 data['nextEpoch'] = nextEpoch
 data['nextNonce'] = newEpochNonce
 jsonData = json.dumps(data, indent=2)
 print(jsonData)
