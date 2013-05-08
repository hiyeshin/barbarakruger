class MarkovGenerator(object):

	def __init__(self, n, max):
		self.n = n #length of ngrams
		self.max = max #maximum number of elements to generate
		self.ngrams = dict() #ngrams as keys
		self.beginnings = list() #beginning ngram of every line

	def tokenize(self, text):
		return text.split(" ") #let every word count

	def feed(self, text):
		tokens = self.tokenize(text)

		if len(tokens) < self.n:
			return

		beginning = tuple(tokens[:self.n])
		self.beginnings.append(beginning)

		for i in range(len(tokens) - self.n):

			gram = tuple(tokens[i:i+self.n])
			next = tokens[i+self.n] # get the element after the gram

			if gram in self.ngrams:
				self.ngrams[gram].append(next)
			else:
				self.ngrams[gram] = [next]


	# put together generated elements
	def concatenate(self, source):
		return " ".join(source)


	def generate(self):
		from random import choice

		current = choice(self.beginnings)
		output = list(current)

		for i in range(self.max):
			if current in self.ngrams:
				possible_next = self.ngrams[current]
				next = choice(possible_next)
				output.append(next)

				current = tuple(output[-self.n:])
			else:
				break

		output_str = self.concatenate(output)
		return output_str



if __name__ == '__main__':
	import sys

	generator = MarkovGenerator(n = 4, max = 200)

	for line in sys.stdin:
		line = line.strip()
		generator.feed(line)

	for i in range(14):
		print generator.generate()





