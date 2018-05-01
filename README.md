## Multiple-criteria decision analysis

When we need to compare two things by multiple criteria we need a way to distribute 100% among those criteria.
With this in hand we can easily compute summary value for any thing and compare them to know which one has more value for us.

This script uses approach of comparing two criteria at a time. After all criteria is compared it prints all asigned values.

### Uses

    from criteria_analyzer import Analyzer
    criterias = ['a', 'b', 'c']
    Analyzer.from_criterias(criterias).print_matrix()
    
this will produce result like this:
    
    What is better: ['b', 'c'], select 1 or 2? 
    1
    What is better: ['a', 'c'], select 1 or 2? 
    1
    What is better: ['a', 'b'], select 1 or 2? 
    1
    Rate is: 
    
    a: %66.66666666666667
    b: %33.333333333333336
    c: %0
    
### Requirements

script is writen for python 3.6
