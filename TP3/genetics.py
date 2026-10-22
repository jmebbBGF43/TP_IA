# Imports
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import State
from pgmpy.sampling import BayesianModelSampling


# ---------Create nodes and conditional probabilityh distribution ------

def get_probs_gene_ancestor(varName):
    """
    Builds a conditional probability distribution (TabularCPD)
    using a priori probabilities, for a variable gene with no
    parents

    Parameter
    ----------
    varName : name of the variable (String)
    """
    raise NotImplementedError
    # TODO
    


def get_probs_trait(varName,evidenceName):
    """
    Builds a conditional probability distribution (TabularCPD)
    for traits given the number of genes

    Parameters
    ----------
    varName : name of the traits variable (String)
    evidenceName: name of the evidence gene variable (String)
    """
    raise NotImplementedError
    # TODO


# constant defining mutation probability of a gene
prob_mutation = 0.01

def get_probs_heredity1(geneParent):
    """
    Computes probability of inheriting 1 gene from
    a given parent: 
    P(Gene_{inherited chromosome}|Gene_{parent})

    Parameter
    ----------
    geneParent: number of genes (0, 1 or 2) of the
    parent (father or mother)
    """
    raise NotImplementedError
    # TODO



def get_probs_gene(varNameChild,evidenceNameFather,evidenceNameMother):
    """
    Builds a conditional probability distribution (TabularCPD)
    for the number of genes of a child given the number of genes
    of each of the parents

    Parameters
    ----------
    varNameChild : name of the traits variable (String)
    evidenceName: name of the evidence gene variable (String)
    """
    raise NotImplementedError
    # TODO

#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Father    |  2  |  2  |  2  |  1  |  1  |  0  |  0  |  0  |  0  |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Mother    |  2  |  1  |  0  |  2  |  1  |  0  |  2  |  1  |  0  |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=2   |                       ???                           |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=1   |                       ???                           |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=0   |                       ???                           |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+


#--------------------Create a Bayesian Network for family n°1 --------------------------------

model1 = DiscreteBayesianNetwork()

model1.add_cpds()
model1.check_model()

# viz = model1.to_graphviz()
# viz.draw('family1.png', prog='dot')


#--------------------Inference for family n°1 --------------------------------

# Exact inference 
infer = VariableElimination(model1)


# Calculate predictions based on the evidence provided by the Trait variables


# Calculate predictions based on the evidence provided by the Trait variables and knowing that Jessica and Alia have resp. 1 and 2 genes



# Approximate inference


#--------------------Create a Bayesian Network for family n°2 --------------------------------

lstP = ['Charles', 'Diana', 'Michael', 'Carole', 'Harry', 'Meghan', 'William', 'Katherine', 'Philippa',
        'Archie', 'Liliet', 'George', 'Charlotte', 'Louis']

model2 = DiscreteBayesianNetwork()

model2.add_cpds()

model2.check_model()

# viz = model2.to_graphviz()
# viz.draw('family2.png', prog='dot')

#--------------------Inference for family n°2 --------------------------------

# Exact inference 
infer = VariableElimination(model2)
dicT = {'T_Charles': 'oui', 'T_Diana': 'non', 'T_Michael': 'non', 'T_Carole': 'non',
        'T_Harry': 'non', 'T_Meghan': 'non', 'T_William': 'non', 'T_Katherine': 'non', 'T_Philippa': 'oui',
        'T_Archie': 'oui', 'T_Liliet': 'non', 'T_George': 'non', 'T_Charlotte': 'non', 'T_Louis': 'oui'}

# Calculate predictions based on the evidence provided by the Trait variables

# Calculate predictions based on the evidence provided by the Trait variables and knowing that Meghan has no gene
