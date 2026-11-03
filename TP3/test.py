# Imports
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import State
from pgmpy.sampling import BayesianModelSampling


# ---------Create nodes and conditional probability distribution ------

def get_probs_gene_ancestor(varName):
    """
    Builds a conditional probability distribution (TabularCPD)
    using a priori probabilities, for a variable gene with no
    parents

    Parameter
    ----------
    varName : name of the variable (String)
    """
    return TabularCPD(
        variable=varName,
        variable_card=3,
        values=[
            [0.01],  # Gene = 2
            [0.03],  # Gene = 1
            [0.96]  # Gene = 0
        ],
        state_names={varName: [2, 1, 0]}
    )


def get_probs_trait(varName, evidenceName):
    """
    Builds a conditional probability distribution (TabularCPD)
    for traits given the number of genes

    Parameters
    ----------
    varName : name of the traits variable (String)
    evidenceName: name of the evidence gene variable (String)
    """
    return TabularCPD(
        variable=varName,
        variable_card=2,
        values=[
            [0.65, 0.56, 0.01],  # Trait = oui (déficience auditive présente)
            [0.35, 0.44, 0.99]  # Trait = non (déficience auditive absente)
        ],
        evidence=[evidenceName],
        evidence_card=[3],
        state_names={
            varName: ['oui', 'non'],
            evidenceName: [2, 1, 0]
        }
    )


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
    geneParent = int(geneParent)
    if geneParent == 2:
        # Le parent a 2 copies mutées, il transmet forcément une copie mutée.
        # Celle-ci reste mutée si elle ne mute pas vers saine : 1 - prob_mutation
        return 1.0 - prob_mutation
    elif geneParent == 1:
        # Le parent a 1 copie mutée et 1 normale. Il transmet l'une ou l'autre avec proba 0.5.
        # 0.5 * (1 - prob_mutation) + 0.5 * prob_mutation = 0.5
        return 0.5 * (1.0 - prob_mutation) + 0.5 * prob_mutation
    elif geneParent == 0:
        # Le parent a 0 copie mutée, il transmet une copie saine.
        # Elle devient mutée uniquement par mutation : prob_mutation
        return prob_mutation
    else:
        raise ValueError(f"geneParent invalide : {geneParent}. Doit être 0, 1 ou 2.")


def get_probs_gene(varNameChild, evidenceNameFather, evidenceNameMother):
    """
    Builds a conditional probability distribution (TabularCPD)
    for the number of genes of a child given the number of genes
    of each of the parents

    Parameters
    ----------
    varNameChild : name of the child gene variable (String)
    evidenceNameFather: name of the father gene variable (String)
    evidenceNameMother: name of the mother gene variable (String)
    """
    # Ordre des états : 2, 1, 0
    states = [2, 1, 0]
    row_2 = []
    row_1 = []
    row_0 = []

    # pgmpy ordonne les colonnes selon le produit cartésien evidence[0] x evidence[1]
    # avec evidence=[Father, Mother], Father varie plus lentement, Mother varie plus vite :
    # (2,2), (2,1), (2,0), (1,2), (1,1), (1,0), (0,2), (0,1), (0,0)
    for f in states:
        for m in states:
            pf = get_probs_heredity1(f)
            pm = get_probs_heredity1(m)
            # Enfant reçoit 2 copies mutées : père ET mère transmettent un gène muté
            p_c2 = pf * pm
            # Enfant reçoit 1 copie mutée : (père ET pas mère) OU (pas père ET mère)
            p_c1 = pf * (1.0 - pm) + (1.0 - pf) * pm
            # Enfant reçoit 0 copie mutée : ni père ni mère ne transmettent de gène muté
            p_c0 = (1.0 - pf) * (1.0 - pm)

            row_2.append(p_c2)
            row_1.append(p_c1)
            row_0.append(p_c0)

    return TabularCPD(
        variable=varNameChild,
        variable_card=3,
        values=[row_2, row_1, row_0],
        evidence=[evidenceNameFather, evidenceNameMother],
        evidence_card=[3, 3],
        state_names={
            varNameChild: states,
            evidenceNameFather: states,
            evidenceNameMother: states
        }
    )


#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Father    |  2  |  2  |  2  |  1  |  1  |  1  |  0  |  0  |  0  |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Mother    |  2  |  1  |  0  |  2  |  1  |  0  |  2  |  1  |  0  |
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=2   |0.980|0.495|0.010|0.495|0.250|0.005|0.010|0.005|0.000|
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=1   |0.020|0.500|0.980|0.500|0.500|0.500|0.980|0.500|0.020|
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#  | Gene_Child=0   |0.000|0.005|0.010|0.005|0.250|0.495|0.010|0.495|0.980|
#  +----------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+


# --------------------Create a Bayesian Network for family n°1 --------------------------------

edges1 = [
    ('G_Leto', 'G_Paul'),
    ('G_Jessica', 'G_Paul'),
    ('G_Leto', 'G_Alia'),
    ('G_Jessica', 'G_Alia'),
    ('G_Leto', 'T_Leto'),
    ('G_Jessica', 'T_Jessica'),
    ('G_Paul', 'T_Paul'),
    ('G_Alia', 'T_Alia')
]

model1 = DiscreteBayesianNetwork(edges1)

model1.add_cpds(
    get_probs_gene_ancestor('G_Leto'),
    get_probs_gene_ancestor('G_Jessica'),
    get_probs_gene('G_Paul', 'G_Leto', 'G_Jessica'),
    get_probs_gene('G_Alia', 'G_Leto', 'G_Jessica'),
    get_probs_trait('T_Leto', 'G_Leto'),
    get_probs_trait('T_Jessica', 'G_Jessica'),
    get_probs_trait('T_Paul', 'G_Paul'),
    get_probs_trait('T_Alia', 'G_Alia')
)

model1.check_model()
print("Famille 1 : Modèle validé avec check_model() = True")

try:
    viz = model1.to_graphviz()
    viz.draw('family1.png', prog='dot')
except Exception:
    pass

# --------------------Inference for family n°1 --------------------------------

# Exact inference
infer = VariableElimination(model1)

# Question 2 : Calculate predictions based on the evidence provided by the Trait variables
# Dans la figure 3 : Leto (sans étoile), Jessica (étoile), Paul (sans étoile), Alia (étoile)
evidence_traits1 = {
    'T_Leto': 'non',
    'T_Jessica': 'oui',
    'T_Paul': 'non',
    'T_Alia': 'oui'
}
print("\n==================== FAMILLE 1 - QUESTION 2 ====================")
print("Prédiction exacte de G pour Paul avec preuves sur les traits T :")
res_q2 = infer.query(['G_Paul'], evidence=evidence_traits1)
print(res_q2)

# Question 3 : Calculate predictions based on the evidence provided by the Trait variables
# and knowing that Jessica and Alia have resp. 1 and 2 genes
evidence_traits_genes1 = dict(evidence_traits1)
evidence_traits_genes1.update({
    'G_Jessica': 1,
    'G_Alia': 2
})
print("\n==================== FAMILLE 1 - QUESTION 3 ====================")
print("Prédiction exacte de G pour Paul (Traits T + G_Jessica=1 et G_Alia=2) :")
res_q3 = infer.query(['G_Paul'], evidence=evidence_traits_genes1)
print(res_q3)

# Question 4 : Approximate inference
print("\n==================== FAMILLE 1 - QUESTION 4 ====================")
print("Prédiction approchée de G pour Paul par échantillonnage (Rejection Sampling) :")
sampler1 = BayesianModelSampling(model1)
ev_states1 = [State(var=k, state=v) for k, v in evidence_traits_genes1.items()]

nb_samples = 300
samples1 = sampler1.rejection_sample(evidence=ev_states1, size=nb_samples, show_progress=False)
dist_approx = samples1['G_Paul'].value_counts(normalize=True)

print(f"Distribution empirique de G_Paul ({nb_samples} échantillons acceptés) :")
for val in [2, 1, 0]:
    p_approx = dist_approx.get(val, 0.0)
    print(f"  P(G_Paul={val}) = {p_approx:.4f}")

print("\nComparaison avec l'inférence exacte :")
print(f"  P(G_Paul=2) : Exact = {res_q3.values[0]:.4f} | Approché = {dist_approx.get(2, 0.0):.4f}")
print(f"  P(G_Paul=1) : Exact = {res_q3.values[1]:.4f} | Approché = {dist_approx.get(1, 0.0):.4f}")
print(f"  P(G_Paul=0) : Exact = {res_q3.values[2]:.4f} | Approché = {dist_approx.get(0, 0.0):.4f}")

# --------------------Create a Bayesian Network for family n°2 --------------------------------

lstP = ['Charles', 'Diana', 'Michael', 'Carole', 'Harry', 'Meghan', 'William', 'Katherine', 'Philippa',
        'Archie', 'Liliet', 'George', 'Charlotte', 'Louis']

parents2 = {
    'Harry': ('Charles', 'Diana'),
    'William': ('Charles', 'Diana'),
    'Katherine': ('Michael', 'Carole'),
    'Philippa': ('Michael', 'Carole'),
    'Archie': ('Harry', 'Meghan'),
    'Liliet': ('Harry', 'Meghan'),
    'George': ('William', 'Katherine'),
    'Charlotte': ('William', 'Katherine'),
    'Louis': ('William', 'Katherine')
}

edges2 = []
cpds2 = []

for p in lstP:
    # Trait dépend du gène
    edges2.append(('G_' + p, 'T_' + p))
    cpds2.append(get_probs_trait('T_' + p, 'G_' + p))

    # Si la personne a des parents dans le modèle
    if p in parents2:
        father, mother = parents2[p]
        edges2.append(('G_' + father, 'G_' + p))
        edges2.append(('G_' + mother, 'G_' + p))
        cpds2.append(get_probs_gene('G_' + p, 'G_' + father, 'G_' + mother))
    else:
        # Ancêtre sans parents connus
        cpds2.append(get_probs_gene_ancestor('G_' + p))

model2 = DiscreteBayesianNetwork(edges2)
model2.add_cpds(*cpds2)
model2.check_model()
print("\nFamille 2 : Modèle validé avec check_model() = True")

try:
    viz = model2.to_graphviz()
    viz.draw('family2.png', prog='dot')
except Exception:
    pass

# --------------------Inference for family n°2 --------------------------------

# Exact inference
infer2 = VariableElimination(model2)
dicT = {'T_Charles': 'oui', 'T_Diana': 'non', 'T_Michael': 'non', 'T_Carole': 'non',
        'T_Harry': 'non', 'T_Meghan': 'non', 'T_William': 'non', 'T_Katherine': 'non', 'T_Philippa': 'oui',
        'T_Archie': 'oui', 'T_Liliet': 'non', 'T_George': 'non', 'T_Charlotte': 'non', 'T_Louis': 'oui'}

# Question 1 : Calculate predictions based on the evidence provided by the Trait variables
print("\n==================== FAMILLE 2 - QUESTION 1 ====================")
print("Prédiction exacte de G pour George (evidence : dicT) :")
res_george_q1 = infer2.query(['G_George'], evidence=dicT)
print(res_george_q1)

print("\nPrédiction exacte de G pour Liliet (evidence : dicT) :")
res_liliet_q1 = infer2.query(['G_Liliet'], evidence=dicT)
print(res_liliet_q1)

# Question 2 : Calculate predictions knowing that Katherine has no defective gene (G_Katherine = 0)
evidence_katherine0 = dict(dicT)
evidence_katherine0['G_Katherine'] = 0

print("\n==================== FAMILLE 2 - QUESTION 2 ====================")
print("Sachant que Katherine n'a aucune version défectueuse (G_Katherine = 0) :")
print("\nPrédiction de G pour George (avec G_Katherine=0) :")
res_george_q2 = infer2.query(['G_George'], evidence=evidence_katherine0)
print(res_george_q2)

print("\nPrédiction de G pour Liliet (avec G_Katherine=0) :")
res_liliet_q2 = infer2.query(['G_Liliet'], evidence=evidence_katherine0)
print(res_liliet_q2)

# Précision supplémentaire pour le commentaire de squelette (G_Meghan = 0) :
evidence_meghan0 = dict(dicT)
evidence_meghan0['G_Meghan'] = 0
print("\n--- Complément : Inférence avec G_Meghan = 0 (selon le commentaire dans le squelette) ---")
print("G_George (avec G_Meghan = 0) :")
print(infer2.query(['G_George'], evidence=evidence_meghan0))
print("G_Liliet (avec G_Meghan = 0) :")
print(infer2.query(['G_Liliet'], evidence=evidence_meghan0))