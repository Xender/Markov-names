#!/usr/bin/env python

import bisect
import itertools
import sys
import random

markov_samples = {}

class CumulativeDistributionSet:
	def __init__(self, samples):
		self.choices = []
		self.accdist = [] # Accumulated Distribution (of weights)

		for choice, weight in samples.items():
			self.choices.append(choice)
			self.accdist.append(weight + len(self))

	def __len__(self):
		try:
			return self.accdist[-1]
		except IndexError:
			return 0

	def __getitem__(self, index):
		return self.choices[ bisect.bisect(self.accdist, index) ]

	def __repr__(self):
		return "<CumulativeDistributionSet:\n choices = {}\n accdist = {}\n>".format(
			repr(self.choices),
			repr(self.accdist)
		)

def add_markov_sample(samples, from_, to):
	try:
		samples[from_][to] += 1
	except KeyError:
		try:
			samples[from_][to] = 1
		except KeyError:
			samples[from_] = { to: 1 }

def main():
	# Read
	for line in sys.stdin:
		line = line.strip()

		prev_c = ''
		for c in line:
			add_markov_sample(markov_samples, prev_c, c)
			prev_c = c

		add_markov_sample(markov_samples, prev_c, '')

	# "Serialize" samples
	print(markov_samples, file=sys.stderr)

	# Samples to CDF
	markov_cdf = {}
	for c, samples in markov_samples.items():
		markov_cdf[c] = CumulativeDistributionSet(samples)

	# "Serialize" CDF
	print(markov_cdf, file=sys.stderr)

	# Generate
	#random.seed() #TODO let user set seed

	for i in range(10):
		c = ''
		result = ""
		while True: # I want do-while or assignment as expression...
			c = random.choice(markov_cdf[c])
			if c is '':
				break

			result += c

		print(result)

if __name__ == "__main__":
	main()
