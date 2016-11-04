a = (1,2)
b = (2,3)
c = (3,4)

dict = {}
dict[c] = b
dict[b] = a

(d,e) = dict[c]
print "a = ", a
print 'b = ', b
print 'c = ', c
print 'dict[c] = ', dict[c]
print 'dict[b] = ', dict[b]
print d
print e