import datetime
import hashlib
import json
from flask import Flask,jsonify

class BlockChain:
	def __init__(self):
		self.chain=[]
		self.creat_block(proof=1,prev_hash="0")

	def creat_block(self,proof,prev_hash):
		block={
			'index':len(self.chain)+1,
			'time_stamp':str(datetime.datetime.now()),
			'proof':proof,
			'prev_hash':prev_hash
			}
		self.chain.append(block)
		return block

	def get_last_block(self):
		return self.chain[-1]

	def proof_of_work(self,prev_proof):
		new_proof=1
		check_proof=False
		while(not check_proof):
			#regex that matchs SHA256 hexadecimal: [A-Fa-f0-9]{64}
			hash_opration=hashlib.sha256(str(new_proof**3-prev_proof**7).encode()).hexdigest()
			if hash_opration[:4] =='0000':
				check_proof=True
			else:
				new_proof+=1
		return new_proof

	def hash(self,block):
		encoded_block=json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self,chain):
		prev_block=chain[0]
		block_index=1
		while(block_index < len(chain)):
			block=chain[block_index]
			if block["prev_hash"]!= self.hash(prev_block):
				return False
			prev_proof=prev_block['proof']
			proof=block['proof']
			hash_opration=hashlib.sha256(str(proof*2-prev_proof**2).encode()).hexdigest()
			if hash_opration[:4] =='0000':
				return False
			prev_block=block
			block_index+=1
		return True



#creating a backend
app=Flask(__name__)
block_chain=BlockChain()

@app.route("/mine_block",methods=['GET'])
def mine_block():
	prev_block=block_chain.get_last_block()
	proof=block_chain.proof_of_work(prev_block['proof'])
	prev_hash=block_chain.hash(prev_block)
	current_block=block_chain.creat_block(proof,prev_hash)
	respons={'message':"congratulations, you just minted a block",
			'index':current_block['index'],
			'time_stamp':current_block['time_stamp'],
			'proof':current_block['proof'],
			'prev_hash':current_block['prev_hash']
	}
	return jsonify(respons),200
@app.route('/get_chain',methods=['GET'])
def display_blockchain():
	respons={'length':len(block_chain.chain),
	'chain':block_chain.chain}
	return jsonify(respons),200
@app.route('/check_valid',methods=['GET'])
def is_chain_valid():
	respons={}
	chain=block_chain.chain
	if block_chain.chain_valid(chain):
		respons={'message':'block chain is valid'}
	else:
		respons={'message':'WARNING block chain is NOT valid'}
	return respons,200
app.run(host='0.0.0.0',port='5000')
