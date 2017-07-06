from math import log

class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. 
  islead (boolean): whether this is a leaf. False.
  """
  
  def __init__(self,attr):
    self.children = {}
    self.attr = attr
    self.isleaf = False

class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.
    
    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """
    def __init__(self,value):
        self.value = value
        self.isleaf = True
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print(str(self))
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.isleaf:
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.isleaf:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)
  
  def classify(self, classificationData):
    """
    Uses the classification tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with this tree.
    """
    #YOUR CODE HERE
    # If we've reached a leaf node, we've found the correct class
    if isinstance(self.root, LeafNode):
        return self.root.value

    attrValue = classificationData[self.root.attr]
    subtree = Tree(self.root.children[attrValue])
    return subtree.classify(classificationData)

  
def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE
    for example in examples:
        if example[attrName] == attrValue:
            newExamples.append(example)
    return newExamples
  
def getClassCounts(examples,className):
    """
    Helper function to get a dictionary of counts of different class values
    in a set of examples. That is, this returns a dictionary where each key 
    in the list corresponds to a possible value of the class and the value
    at that key corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """
    classCounts = {}
    #YOUR CODE HERE
    for example in examples:
        classValue = example[className]
        if classValue not in classCounts.keys():
            classCounts[classValue] = 0
        classCounts[classValue] += 1
    return classCounts

def getMostCommonClass(examples,className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples,className)
    return max(counts, key=counts.get) if len(examples)>0 else None

def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a dictionary of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
	  That is, this returns a dictionary of dictionaries, where each key  
	  corresponds to a possible value of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for the attribute
        className (str): the name of the class
    Returns:
        dictionary<str,dictionary<str,int>>
        This is a dictionary that for each value of the attribute has a
        dictionary from class values to class counts, as in getClassCounts
    """
    attributeCounts={}
    #YOUR CODE HERE
    for attrValue in attrValues:
        pertinentExamples = getPertinentExamples(examples, attrName, attrValue)
        attributeCounts[attrValue] = (getClassCounts(pertinentExamples, className))
    return attributeCounts
        

def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE
    # B(q) = -(qlog2q + (1-q)log2(1-q)), where q is probability
    entropy = 0
    if type(classCounts) == list:
        for count in classCounts:
            prob = float(count) / sum(classCounts)
            entropy += -(prob * log(prob, 2))
    elif type(classCounts) == dict:
        for count in classCounts.values():
            prob = float(count) / sum(classCounts.values())
            entropy += -(prob * log(prob, 2))

    return entropy


def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    # Remainder (A) = sum (pk + nk / p + n)B(pk / (pk + nk)) from k = 1 to d, where d is # distinct values
    remainder = 0
    classCounts = getClassCounts(examples, className)
    for attrValue in attrValues:
        pertinentExamples = getPertinentExamples(examples, attrName, attrValue)
        pertinentClassCounts = getClassCounts(pertinentExamples, className)
        prob = (float(sum(pertinentClassCounts.values())) / sum(classCounts.values()))
        remainder += prob * setEntropy(pertinentClassCounts)
    return remainder

          
def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    classCounts = getClassCounts(examples, className)
    return setEntropy(classCounts.values()) - remainder(examples, attrName, attrValues, className)
  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE
    index = 1
    for classCount in classCounts:
        index -= (float(classCount) / sum(classCounts)) ** 2
    return index
  
def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE
    import sys
    # gini^D(S, cs) = (n1/n)gini(S1) + (n2/n)gini(S2) where S1 and S2 are subsets, n1 and n2 are the number of examples
    # in each respective subset, and cs is the splitting criterion
    gain = 0
    # Subset for each attribute value
    for attrValue in attrValues:
        # This is the set of examples included in the subset corresponding to this attribute value
        pertinentExamples = getPertinentExamples(examples, attrName, attrValue)
        # This is the subset of length n
        pertinentClassCounts = getClassCounts(pertinentExamples, className)
        # add (nj/n)gini(Sj) to the rolling sum
        gain += (float(len(pertinentExamples)) / len(examples)) * giniIndex(pertinentClassCounts.values())
    if gain == 0:
        return sys.maxsize
    # return the inverse of this function
    return 1.0 / gain
    
def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE
    # A decision tree is a function that takes in a vector of attribute values and returns a "decision" -- a single
    # output value
    # Each internal node in the tree corresponds to a test of the value of one of the input attributes, Ai, and
    # the branches from the node are labeled with the possible values of the attribute, Ai =vik.
    # Each leaf node in the tree specifies a value to be returned by the function.

    if len(examples) == 0:
        return LeafNode(defaultLabel)

    # If the remaining examples are all positive (or all negative), then we are done: we can return their value
    firstValue = examples[0][className]
    allSame = True
    for example in examples[1:]:
        if example[className] != firstValue:
            allSame = False
            break
    if allSame:
        return LeafNode(firstValue)

    # If there are no more attributes left to examine, the best we can do is return the plurality value of the remaining
    # examples
    # Remember, class values are like decisions, and class counts refer to the number of paths that lead to a particular
    # decision (class value)
    if len(remainingAttributes) == 0:
        return LeafNode(getMostCommonClass(examples, className))

    remainingAttributes = list(remainingAttributes)
    # This refers to the best attribute to be used to split the subtree
    splitAttr = remainingAttributes[0]
    for attribute in remainingAttributes:
        # Check whether the amount of information gained by selecting the current attribute is greater than that gained
        # by the current split attribute. If so, replace the old split attribute with the current attribute
        if gainFunc(examples, attribute, attributeValues[attribute], className) \
                > gainFunc(examples, splitAttr, attributeValues[splitAttr], className):
            splitAttr = attribute

    # The split attribute will not be included in the next subtree
    newRemainingAttributes = list(remainingAttributes)
    newRemainingAttributes.remove(splitAttr)

    root = Node(splitAttr)
    for attrValue in attributeValues[splitAttr]:
        # Examples pertinent to the subtrees generated by this split
        pertinentExamples = getPertinentExamples(examples, splitAttr, attrValue)
        root.children[attrValue] = makeSubtrees(newRemainingAttributes, pertinentExamples, attributeValues,
                                                    className, getMostCommonClass(examples, className), setScoreFunc, gainFunc)

    return root

def makePrunedTree(examples, attrValues,className,setScoreFunc,gainFunc,q):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makePrunedSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc,q))
    
def makePrunedSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc,q):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE (Extra Credit)
    from scipy.stats.stats import chisqprob

    classCounts = getClassCounts(examples, className)

    if len(examples) == 0 or examples is None:
        return LeafNode(defaultLabel)

    # If the remaining examples are all positive (or all negative), then we are done: we can return their value
    firstValue = examples[0][className]
    allSame = True
    for example in examples[1:]:
        if example[className] != firstValue:
            allSame = False
            break
    if allSame:
        return LeafNode(firstValue)

    if remainingAttributes is None or len(remainingAttributes) == 0:
        return LeafNode(getMostCommonClass(examples, className))

    # This refers to the best attribute to be used to split the subtree
    splitAttr = remainingAttributes[0]
    for attribute in remainingAttributes:
        # Check whether the amount of information gained by selecting the current attribute is greater than that gained
        # by the current split attribute. If so, replace the old split attribute with the current attribute
        if gainFunc(examples, attribute, attributeValues[attribute], className) \
                > gainFunc(examples, splitAttr, attributeValues[splitAttr], className):
            splitAttr = attribute

    mostCommon = getMostCommonClass(examples, className)
    if chiSquareTest(examples, attributeValues, className, splitAttr, classCounts, q):
        return LeafNode(mostCommon)
    else:
        newRemainingAttributes = list(remainingAttributes)
        newRemainingAttributes.remove(splitAttr)

        root = Node(splitAttr)
        for value in attributeValues[splitAttr]:
            pertinentExamples = getPertinentExamples(examples, splitAttr, value)
            root.children[value] = makePrunedSubtrees(newRemainingAttributes, pertinentExamples, attributeValues, className,
                                                      mostCommon, setScoreFunc, gainFunc, q)
        return root


def chiSquareTest(examples, attributeValues, className, splitAttr, classCounts, q):
    from scipy.stats.stats import chisqprob
    # Dev(X) = sum( (px - phatx)^2 / phatx) + (nx - nhatx)^2 / nhatx for all values x of X, where X is the split
    # attribute
    totalSum = sum(classCounts.values())
    deviation = 0.0
    # attributeValues[splitAttr] = X
    for value in attributeValues[splitAttr]:
        pertinentExamples = getPertinentExamples(examples, splitAttr, value)
        pertinentClassCounts = getClassCounts(pertinentExamples, className)
        newTotalSum = sum(pertinentClassCounts.values())
        classKeys = classCounts.keys()

        for indivClass in classKeys:
            # So we don't get that KeyError
            if indivClass not in pertinentClassCounts:
                pertinentClassCounts[indivClass] = 0

            phat = (float(classCounts[indivClass]) / totalSum) * newTotalSum
            # (px - phatx) ^ 2 / phatx
            deviation += ((float(pertinentClassCounts[indivClass]) - phat) ** 2) / phat
    p = chisqprob(deviation, (len(attributeValues[splitAttr]) - 1) * (len(classKeys) - 1))
    return p > q
