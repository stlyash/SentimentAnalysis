import re

textString = '''Good muffins cost $3.88\nin New York. I am we and I live in USA Please buy me two of them.\n\nThanks.'''
forPronounCount = re.compile(r'\b(I|we|ours|my|mine|(?-i:us))\b', re.I)
pronCount = len(forPronounCount.findall(textString))
print(pronouns)