#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:41:00 2020

@author: gnanfack
"""


import time
from ortools.sat.python import cp_model
import graphviz
import numpy as np
import networkx as nx

import col1


def buildTree(y,Cl,K,L,V,M,X,Y,colnames,solver, C,
              classnames=["Mammal","Bird","Reptile","Fish","Amphibian","Bug","Invertebrate"],dico=None):
    indent=0
    Tnx=nx.DiGraph()
    root_attribute=None
    flag=False
    l=0
    while not(flag) and l<M:
        y_array=[solver.Value(y[(0,0,l,p)]) for p in range(V)]
        if 1 in y_array:
            root_attribute=l
            flag=True
        l+=1
    (values,counts) = np.unique(Y,return_counts=True)
    values=list(values)
    ind=np.argmax(counts)
    freq=[counts[values.index(i)] if i in values else 0 for i in range(len(classnames))]
    Tnx.add_node(indent,
                 label='best attribute='+colnames[root_attribute],attribute=root_attribute,samples=len(Y),
                 values=freq,value=None,instances=list(range(len(Y))), labels=Y, classe=classnames[ind],color=col1.get_color(freq,len(classnames)))
    for i in range(L):
        node=0
        j=0
        flag=False
        while not(flag) and j<K:
            attribute=-1
            value=-1
            flag1=False
            l=0

            while not(flag1) and l<M:
                y_array=[solver.Value(y[(i,j,l,p)]) for p in range(V)]
                if 1 in y_array:
                    attribute=l
                    value=y_array.index(1)
                    flag1=True
                l+=1
            if not(flag1):
                flag=True
                if dico and i in dico.keys():
                    Tnx.nodes[node]['best_attribute']="same_leaf_constraint="+str(dico[i])+"\n"
                else:
                    Tnx.nodes[node]['best_attribute']=""
                classe=[solver.Value(Cl[(i,c)]) for c in range(len(C))]
                Tnx.nodes[node]['class']=classe.index(1)
            else:
                neighbors=[i for i in Tnx.neighbors(node)]
                q=0
                drap=False
                while not(drap) and q<len(neighbors):
                    if Tnx.nodes[neighbors[q]]['attribute']==attribute and Tnx.nodes[neighbors[q]]['value']==value:
                        node=neighbors[q]
                        drap=True
                    q+=1
                if not(drap):
                    indent+=1
#                     print(Tnx.nodes[parent]['instances'])
                    indices_t=np.where(np.take(X[:,attribute], Tnx.nodes[node]['instances'])==value)[0]
                    instances_t=np.take(Tnx.nodes[node]['instances'],indices_t)
                    labels_t=np.take(Tnx.nodes[node]['labels'],indices_t)
                    #print(labels_t,indices_t,instances_t,node, parent,'attribute',attribute,value)
                    (values_t,counts_t) = np.unique(labels_t,return_counts=True)
                    values_t=list(values_t)
                    freq_t=[counts_t[values_t.index(i)] if i in values_t else 0 for i in range(len(classnames))]
                    color_t=None
                    if len(counts_t)==0:
                        color_t='black'
                        class_t='None'
                    else:
                        ind_t=np.argmax(freq_t)
#                         print(freq_t,counts_t,values_t,len(values_t),len(counts_t))
                        color_t=col1.get_color(freq_t,len(classnames))
                        class_t=classnames[ind_t]
                    Tnx.add_node(indent,instances=instances_t, labels=labels_t,samples=len(instances_t),
                                 attribute=attribute,value=value,values=freq_t,classe=class_t,color=color_t)
                    Tnx.add_edge(node,indent)
                    Tnx.nodes[node]['best_attribute']="attribute="+colnames[attribute]+"\n"
                    node=indent
                    if j==K-1:
                        if dico and i in dico.keys():
                            Tnx.nodes[node]['best_attribute']="same_leaf_constraint="+str(dico[i])+"\n"
                        else:
                            Tnx.nodes[node]['best_attribute']=""
                        classe=[solver.Value(Cl[(i,c)]) for c in range(len(C))]
                        Tnx.nodes[node]['class']=classe.index(1)
            j+=1
    return Tnx


def export_graphviz_cp(tree):
    Tree=graphviz.Digraph(format='png',graph_attr={"randir":"LR"},
                                    node_attr={'shape':"box"})
    indent=0
    list_nodes=[0]
    Tree.node(str(indent),
                      label=tree.nodes[0]['best_attribute']+'samples='+str(tree.nodes[0]['samples'])+'\nvalue='+str(tree.nodes[0]['values'])+'\nclass='+tree.nodes[0]['classe'],
                     fillcolor=tree.nodes[0]['color'],style="rounded,filled")
    here={}
    here[indent]=indent
    while len(list_nodes)>=1:
        node=list_nodes.pop(0)
        neighbors=[i for i in tree.neighbors(node)]
        if len(neighbors)!=0:
            node1=neighbors[0] if tree.nodes[neighbors[0]]['value']==1 else neighbors[1]
            node2=neighbors[0] if tree.nodes[neighbors[0]]['value']==0 else neighbors[1]
            indent+=1
            here[node1]=indent
            Tree.node(str(indent),
                      label=tree.nodes[node1]['best_attribute']+'samples='+str(tree.nodes[node1]['samples'])+'\nvalue='+str(tree.nodes[node1]['values'])+'\nclass='+tree.nodes[node1]['classe'],
                     fillcolor=tree.nodes[node1]['color'],style="rounded,filled")
            Tree.edge(str(here[node]),str(indent),label='\nvalue=1')
            indent+=1
            here[node2]=indent
            Tree.node(str(indent),
                      label=tree.nodes[node2]['best_attribute']+'samples='+str(tree.nodes[node2]['samples'])+'\nvalue='+str(tree.nodes[node2]['values'])+'\nclass='+tree.nodes[node2]['classe'],
                     fillcolor=tree.nodes[node2]['color'],style="rounded,filled")
            Tree.edge(str(here[node]),str(indent),label='\nvalue=0')
            if tree.out_degree(node1)!=0:
                list_nodes.append(node1)
            if tree.out_degree(node2)!=0:
                list_nodes.append(node2)


    return Tree

def decisionTreeConstraint(K,L,V,max_time,X,Y,classnames,colnames, C,imbalanced=True,min_number=1,precedence=None
                           ,must_link=None,max_cost=False,list_cost=[],must_be_in=None,distinct_leaves=None,hierarchy=None,
                          attribute_exclusion=None):
    model = cp_model.CpModel()
    N=X.shape[0]
    M=X.shape[1]
    x={}
    y={}
    cl={}
    #z={}
    #s={}
    u={}
    r={}
    z={}
    M=X.shape[1]
    for i in range(L):
        for j in range(K):
            for l in range(M):
                for p in range(V):
                    y[(i,j,l,p)]=model.NewBoolVar('y'+'('+str(i)+','+str(j)+','+str(l)+','+str(p)+')')
#                     for a in range(L):
#                         if a > i:
#                             u[(i,j,l,p,a)]=model.NewBoolVar('u'+'('+str(i)+','+str(j)+','+str(l)+','+str(p)+str(a)+')')
            for a in range(L):
                if a > i:
                    for q in range(3):
                        z[(i,j,a,q)]=model.NewBoolVar('z'+'('+str(i)+','+str(j)+','+str(a)+','+str(q)+')')

    for e in range(N):
        for i in range(L):
            x[(e,i)]=model.NewBoolVar('x'+'('+str(e)+','+str(i)+')')
#         for c in range(len(C)):
        r[(e)]=model.NewBoolVar('r'+'('+str(e)+')')


    for i in range(L):
        for c in range(len(C)):
            cl[(i,c)]=model.NewBoolVar('cl'+'('+str(i)+','+str(c)+')')

    #Constraints
    for i in range(L):
        model.Add(sum(y[(i,0,l,p)] for l in range(M) for p in range(V))>=1)
        for j in range(K):                         
            #Ensure that exactly no more than one variable is chosen
            model.Add(sum(y[(i,j,l,p)] for l in range(M) for p in range(V))<=1)
            if j!=0:
                model.Add(sum(y[(i,j,l,p)] for l in range(M) for p in range(V)) <= sum(y[(i,j-1,l,p)] for l in range(M) for p in range(V)))
    #         #Ensure that the value chosen corresponds to the variable chosen
    #         for l in range(m):
    #             model.Add(sum(y[(i,j,l,p)] for p in range(V))==x[(i,j,l)])

        for l in range(M):
            #Ensure that exactly each variable is chosen nomore than once in a branch
            model.Add(sum(y[(i,j,l,p)] for j in range(K) for p in range(V))<=1)

    #Ensure the existence of the complentary branch
    for i in range(L):
        L_i = [b for b in range(i+1,L)]
        for a in L_i:
            #model.Add(sum(u[(min(i,a),j,l,p,max(a,i))] for j in range(K) for l in range(M) for p in range(V))>=1)
            model.Add(z[(i, K-1, a, 0)]==0)
            model.Add(z[(i, 0, a, 2)]==0)
            for l in range(M):
                model.Add(sum(y[(i,0,l,p)] for p in range(V))==sum(y[(a,0,l,p)] for p in range(V)))
#         for j in range(K):
#             for l in range(M):
#                 for p in range(V):
#                     #model.Add(u[(i,j,l,p,i)]==0)
#                     for a in L_i:
#                         model.Add(y[(i,j,l,p)]==y[(a,j,l,p)]).OnlyEnforceIf(u[(min(i,a),j,l,p,max(a,i))].Not())
#                         model.Add(y[(i,j,l,p)]!=y[(a,j,l,p)]).OnlyEnforceIf(u[(min(i,a),j,l,p,max(a,i))])

        for j in range(K):
            for a in L_i:
                #model.Add(z[(i,j,a,1)]==z[(a,j,i,1)])
                for j1 in range(j):
                    for l in range(M):
                        for p in range(V):
                            model.Add(y[(i,j1,l,p)]==y[(a,j1,l,p)]).OnlyEnforceIf(z[(i,j,a,1)])
#                     model.Add(sum(u[(min(i,a),j1,l,p,max(a,i))] for j1 in range(j) for l in range(M) for p in range(V))==0).OnlyEnforceIf(z[(min(i,a),j,max(a,i),1)])
#                     model.Add(sum(u[(min(i,a),j1,l,p,max(a,i))] for j1 in range(j) for l in range(M) for p in range(V))>=1).OnlyEnforceIf(z[(min(i,a),j,max(a,i),2)])
#                 model.Add(sum(u[(min(i,a),j,l,p,max(a,i))] for j1 in range(j+1) for l in range(M) for p in range(V))==0).OnlyEnforceIf(z[(min(i,a),j,max(a,i),0)])
#                 model.Add(sum(u[(min(i,a),j,l,p,max(a,i))] for l in range(M) for p in range(V))>=1).OnlyEnforceIf(z[(min(i,a),j,max(a,i),1)])

                for j1 in range(j+1):
                    for l in range(M):
                        for p in range(V):
                            model.Add(y[(i,j1,l,p)]==y[(a,j1,l,p)]).OnlyEnforceIf(z[(i,j,a,0)])
                            
                model.Add(sum(z[(i,j1,a,1)] for j1 in range(j+1,K))>=z[(i,j,a,0)])
                model.Add(z[(i,j,a,0)]<=sum(y[(i,j,l,p)] for l in range(M) for p in range(V)))
                
                for j1 in range(j+1,K):
                    model.Add(z[(i,j1,a,2)]==1).OnlyEnforceIf(z[(i,j,a,1)])
                
                model.Add(sum(z[(i,j,a,q)] for q in range(3))==1)
                
                for l in range(M):
                    model.Add(sum(y[(i,j,l,p)] for p in range(V))==sum(y[(a,j,l,p)] for p in range(V))).OnlyEnforceIf(z[(i,j,a,1)])
                    model.Add(sum(y[(i,j,l,p)] for p in range(V))<=y[(i,j,l,0)]).OnlyEnforceIf(z[(i, j, a, 1)])
                    model.Add(sum(y[(a,j,l,p)] for p in range(V))<=y[(a,j,l,1)]).OnlyEnforceIf(z[(i, j, a, 1)])
            
                model.Add(z[(i,j,a,1)] <= sum(y[(i,j,l,p)] for l in range(M) for p in range(V)))
            
            model.Add(sum(z[(min(i,b),j,max(b,i),1)] for b in range(L) if b!=i )>=sum(y[(i,j,l,p)] for l in range(M) for p in range(V)))
            
        for j in range(K-1):
            for a in L_i:
                model.Add(z[(i,j,a,0)]<=sum(y[(i,j+1,l,p)] for l in range(M) for p in range(V)))
    for e in range(N):
        model.Add(sum(x[(e,i)] for i in range(L))==1)
        for i in range(L):
            for j in range(K):
                for l in range(M):
                    val= [1,0] if X[e,l]==0 else [0,1]
                    for p in range(V):
                        model.Add(x[(e,i)]<=1-val[p]*sum(y[(i,j,l,p)] for p in range(V))+y[(i,j,l,p)])
                        model.Add(x[(e,i)]<=1+val[p]*sum(y[(i,j,l,p)] for p in range(V)) -y[(i,j,l,p)])
                        
#                         model.Add(x[(e,i)]<=1-val[p]+y[(i,j,l,p)]).OnlyEnforceIf(y[(i,j,l,p)])
#                         model.Add(x[(e,i)]<=1+val[p]-y[(i,j,l,p)]).OnlyEnforceIf(y[(i,j,l,p)])


    for i in range(L):
        model.Add(sum(cl[(i,c)] for c in range(len(C)))==1)
        model.Add(sum(x[(e,i)] for e in range(N))>=min_number)
        for c in range(len(C)):
            for cp in range(len(C)):
                if c!=cp:
                    model.Add(sum(x[(e,i)]*Y[e,c] for e in range(N))>=sum(x[(e,i)]*Y[e,cp] for e in range(N))).OnlyEnforceIf(cl[(i,c)])
    for e in range(N):
        for c in range(len(C)):
            #model.Add(sum(r[(e,c)] for c in range(len(C)))==1)
            for i in range(L):
                model.Add(r[(e)]>=-cl[(i,c)]+Y[e,c]).OnlyEnforceIf(x[(e,i)])
                #model.Add(r[(e,c)]>=cl[(i,c)]-Y[e,c]).OnlyEnforceIf(x[(e,i)])
                model.Add(r[(e)]<=2-cl[(i,c)]-Y[e,c]).OnlyEnforceIf(x[(e,i)])
    if imbalanced:
        for c in range(len(C)):
            model.Add(sum(cl[(i,c)] for i in range(L))>=1)
    
    #Attributes that must be taken
    if must_be_in:
        model.Add(sum(y[(i,j,b,p)] for i in range(L) for j in range(K) for b in must_be_in for p in range(V))>=1)
    
    #Distinct leaves
    if distinct_leaves:
        for es in distinct_leaves:
            for i in range(L):
                model.Add(sum(x[(e,i)] for e in es)<=1)
    
    #ordering constraint
    if precedence:
        for pair in precedence:
            for i in range(L):
                for j in range(1,K):
                    model.Add(sum(y[(i,j1,pair[1],p)] for j1 in range(j) for p in range(V))<=1-sum(y[(i,j,pair[0],p)] for p in range(V)))
    if must_link: 
        for se in must_link:
            for e in se:
                for i in range(L):
                    model.Add(sum(x[(ep,i)] for ep in se)==len(se)).OnlyEnforceIf(x[(e,i)])
    if hierarchy:
        i1=0
        for he in hierarchy:
            for at in he:
                model.Add(sum(y[(i1,j,at,p)] for j in range(K) for p in range(V))>=1)
            i1+=1
    if attribute_exclusion:
        for att_list in attribute_exclusion:
            model.Add(sum(y[(i,j,at,p)] for i in range(L) for j in range(K) for at in att_list for p in range(V))<=2*len(att_list)-1)        
    
    # if branch_attrib_exclusion:
    #     for att_list in branch_attrib_exclusion:
    #         for i in range(L):
    #             model.Add(sum(y[(i,j,at,p)] for j in range(K) for at in att_list for p in range(V))<=2*len(att_list)-1)
    
    # if max_cost:
    #     for i in range(L):
    #         model.Add(sum(y[(i,j,l,p)]*list_cost[l] for j in range(K) for l in range(M) for p in range(V))<=max_cost)

    #Create a solver and solve.
    solver = cp_model.CpSolver()
    model.Minimize(sum(r[(e)] for e in range(N) ))
    #solver.parameters.random_seed = 10
    solver.parameters.max_time_in_seconds = max_time
    solver.parameters.linearization_level=0
    solver.parameters.cp_model_probing_level=0
    solver.parameters.num_search_workers=8
    #solver.parameters.deterministic_parallel_search = 134
    tic = time.time()
    status = solver.Solve(model)
    tac = time.time()
        #filename='visual_cp_bis/dt_ortools_leaves='+str(L)+'_depth='+str(K)+'_time='+str(max_time)+'s'
    if status == cp_model.FEASIBLE or status==cp_model.OPTIMAL:
        dico={}
        if must_link:
            for es in must_link:
                for i in range(L):
                    if solver.Value(x[(es[0],i)])==1:
                        if i in dico.keys():
                            dico[i]+=es
                        else:
                            dico[i]=es
#         if distinct_leaves:
#             for es in distinct_leaves:
#                 for i in range(L):
#                     print("Leaf, ",i,", ",sum(solver.Value(x[(e,i)]) for e in es))
        tree=buildTree(y=y,Cl=cl,K=K,L=L,V=V,M=M,colnames=colnames, C = C,solver=solver,classnames=classnames,X=X,Y=np.argmax(Y,axis=1),dico=dico)
        if status==status == cp_model.FEASIBLE:

#             for se in must_link:
#                 for e in se:
#                     for i in range(L):
#                         if solver.Value(x[(e,i)])==1:
#                             print("Example: ",e,", branch: ",i)
#                             for j in range(K):
#                                 for l in range(M):
#                                     if sum(solver.Value(y[(i,j,l,p)]) for p in range(V))==1:
#                                         print("\t attribute: ",colnames[l],", Value: ",X[e,l])
            return tree,'Not_Optimal', tac-tic
        else:
            return tree, 'Optimal', tac-tic
    else:
        return None, 'No_Solution', tac-tic

def getClass(tree, node,features):
        if tree.out_degree(node)==0:
            #print(node)
            return tree.nodes[node]['class']
        else :
            p=0
            flag=True
            nextnode=-1
            neighbors=[t for t in tree.neighbors(node)]
            while flag and p<= len(neighbors):
                  if features[tree.nodes[neighbors[p]]['attribute']]==tree.nodes[neighbors[p]]['value']:
                      nextnode=neighbors[p]
                      #print(node,nextnode,tree.nodes[neighbors[p]]['attribute'],features[tree.nodes[neighbors[p]]['attribute']])
                      #print(tree.nodes[neighbors[p]]['value'])
                      flag=False
                  p+=1
            return getClass(tree,nextnode,features)

    #Just returning the class
def predict(tree,x):
    return getClass(tree,0,x)
