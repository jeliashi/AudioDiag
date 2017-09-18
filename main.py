from Models.OutputSound import OutputSound

if __name__ == "__main__":
	x = OutputSound(1, generateBool=False)
	while True:
		for i in range(1000000):
			x.generateBool = False
			x.produceSound()
		x.generateBool=True
		x.produceSound()
