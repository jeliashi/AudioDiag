from numpy import empty,nan,random, sin, pi, arange, float32
from pandas import DataFrame


# returns np array of length nrows
class Noise:
	def __init__(self):
		pass

	def PinkNoise(self, nrows, ncols=16):
		array = empty((nrows, ncols))
		array.fill(nan)
		array[0, :] = random.random(ncols)
		array[:, 0] = random.random(nrows)

		cols = random.geometric(0.5, nrows)
		cols[cols >= ncols] = 0
		rows = random.randint(nrows, size=nrows)
		array[rows, cols] = random.random(nrows)

		df = DataFrame(array)
		df.fillna(method='ffill', axis=0, inplace=True)
		total = df.sum(axis=1)
		return total.values

	def WhiteNoise(self, nrows):
		pass

	def BlueNoise(self, nrows):
		pass

	def RedNoise(self, nrows):
		pass


class Tone:
	def __init__(self):
		pass

	def SineWave(self, nrows, toneF, phase):
		vals = 2*pi*arange(nrows)*(toneF)/nrows - phase
		samples = (sin(vals)).astype(float32)
		phase = vals[-1]%(2*pi)
		return samples, phase


	def TriWave(self, nrows, toneF):
		pass

	def SqWave(self, nrows, toneF):
		pass

