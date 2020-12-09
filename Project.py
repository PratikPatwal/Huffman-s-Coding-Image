import numpy as np
import imageio 
import queue
# following code is used for huffman compression
class Apex:
	def __init__(self):
		self.mess = None
		self.rules = None
		self.proof = None
		self.right = None
		self.left = None 	
	def __lt__(self, other):
		if (self.mess < other.mess):		
			return 1
		else:
			return 0
	def __ge__(self, other):
		if (self.mess > other.mess):
			return 1
		else:
			return 0
			
def rgb2ash(pht):
	ash_pht = np.rint(pht[:,:,0]*0.2989 + pht[:,:,1]*0.5870 + pht[:,:,2]*0.1140)
	ash_pht = ash_pht.astype(int)
	return ash_pht

def get2highest(proof):			
    early = extra = 1
    a_id=b_id=0
    for y,z in enumerate(proof):
        if (z < early):
            extra = early
            b_id = a_id
            early = z
            a_id = y
        elif (z < extra and z != early):
            extra = z
    return a_id,early,b_id,extra
    
def bush(chance):
	x = queue.PriorityQueue()
	for glow,fact in enumerate(chance):
		image = Apex()
		image.proof = glow
		image.mess = fact
		x.put(image)

	while (x.qsize()>1):
    	# underneath code is used for creating code
		newknot = Apex()		
		lx = x.get()
		rx = x.get()			
						
		newknot.right = lx 		
		newknot.left = rx

        # the sum of other two must be the new prob in the node is shown in the below code
		newmess = lx.mess+rx.mess	
		newknot.mess = newmess
		x.put(newknot)	# new node is added as a image, replacing the other two 
	return x.get()		# it return to the origin node - bush is complete

# Underneath codes is the bush to generate codes
def huffman_disclaimer(origin_node,tmp_batch,f):		
	if (origin_node.right is not None):
		tmp_batch[huffman_disclaimer.count] = 1
		huffman_disclaimer.count+=1
		huffman_disclaimer(origin_node.right,tmp_batch,f)
		huffman_disclaimer.count-=1
	if (origin_node.left is not None):
		tmp_batch[huffman_disclaimer.count] = 0
		huffman_disclaimer.count+=1
		huffman_disclaimer(origin_node.left,tmp_batch,f)
		huffman_disclaimer.count-=1
	else:
    	# underneath code count the number of bits for each glow
		huffman_disclaimer.output_bits[origin_node.proof] = huffman_disclaimer.count		
		bitstream = ''.join(str(cell) for cell in tmp_batch[1:huffman_disclaimer.count]) 
		glow = str(origin_node.proof)
		wr_str = glow+' '+ bitstream+'\n'

        # write the glow and the code to a file
		f.write(wr_str)		
	return

# Read the image file into a numpy array
pht = imageio.imread('Texting Image file.jpg')

# convert to black and white
ash_pht = rgb2ash(pht)

# compute the history of pixels
history = np.bincount(ash_pht.ravel(),minlength=256)

#underneath code discover chance from frequencies
chance = history/np.sum(history)

# Underneath code is to creare bush using probes
origin_node = bush(chance)			
tmp_batch = np.ones([64],dtype=int)
huffman_disclaimer.output_bits = np.empty(256,dtype=int) 
huffman_disclaimer.count = 0
f = open('codes.txt','w')

# Underneath code traverse the bush and write the codes
huffman_disclaimer(origin_node,tmp_batch,f)		

# Underneath code calculate bits in black and white
note_bits = pht.shape[0]*pht.shape[1]*8	

# Underneath code calculate the compression rate
compression = (1-np.sum(huffman_disclaimer.output_bits*history)/note_bits)*100
print('Compression is ',compression,' percent')
