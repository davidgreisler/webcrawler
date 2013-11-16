import PageRank

print "Testing the page rank computer."
print

webgraph = { 'A' : [ 'B', 'C' ],
             'B' : [ 'C' ],
             'C' : [ 'B', 'D' ],
             'D' : [] }

print "Web graph: "
print webgraph

computer = PageRank.Computer(webgraph)
computer.compute()
result = computer.page_ranks

print ""
print "Results:"

result_sum = 0
for website in sorted(result.keys()):
    result_sum += result[website]
    
    print "  " + website + ": " + str(result[website])

print
print "Sum: " + str(result_sum)
