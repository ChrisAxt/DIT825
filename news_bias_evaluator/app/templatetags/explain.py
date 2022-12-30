from django import template

register = template.Library()

@register.simple_tag
def getIndex(sentence, word):
    print('sentence length is: ', len(sentence))
    return sentence.index(word)

@register.simple_tag
def getWord(array, index):
    print('array length is:',len(array))
    return array[index]
