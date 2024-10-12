import datatime
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
			'time_stamp':str(datatime.datatime.now()),
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
			hash_opration=hashlib.sha256(str(proof**3-prev_proof**7).encode()).hexdigest()
			if hash_opration[:4] =='0000':
				return False
			prev_block=block
			block_index+=1
		return True






