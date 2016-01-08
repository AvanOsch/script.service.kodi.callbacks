#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2015 KenV99
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from resources.lib.events import Events

allevts = Events().AllEvents
output = []
ssp = '    <setting '
evts = ['None']
for evtkey in allevts.keys():
    evts.append(allevts[evtkey]['text'])
evts.sort()
evts = "|".join(evts)
tasks = ''
for i in xrange(1,11):
    tasks += 'Task %s|' % str(i)
tasks = tasks[:-1]

def getoffset(idx, lst):
    return str(idx-len(lst))

output.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
output.append('<settings>\n')
output.append('  <category label="32001">\n')

for i in xrange(1,11):
    prefix = "T%s" % str(i)
    output.append('    <setting label="%s" type="lsep"/>\n'% str(32100 + i))
    output.append('    <setting default="none" id="%s.type" label="32002" type="labelenum" values="none|script|python|builtin|http" />\n' % prefix)
    output.append('    <setting default="-1" id="%s.maxrunning" label="32089" type="number" visible="!eq(-1,0)" />\n' % prefix)
    output.append('    <setting default="-1" id="%s.maxruns" label="32090" type="number" visible="!eq(-2,0)" />\n' % prefix)
    output.append('    <setting default="-1" id="%s.refractory" label="32091" type="number" visible="!eq(-3,0)" />\n' % prefix)
    output.append('    <setting default="" id="%s.scriptfile" label="32003" type="file" visible="eq(-4,1)" />\n' % prefix)
    output.append('    <setting default="true" label="32008" id="%s.shell" visible="eq(-5,1)" type="bool" />\n' % prefix)
    output.append('    <setting default="" id="%s.pythondoc" label="32004" type="file" visible="eq(-6,2)" />\n' % prefix)
    output.append('    <setting default="" id="%s.builtin" label="32005" type="text" visible="eq(-7,3)" />\n' % prefix)
    output.append('    <setting default="" id="%s.http" label="32006" type="text" visible="eq(-8,4)" />\n' % prefix)
output.append('  </category>\n\n')
output.append('  <category label="32092">\n')
for i in xrange(1,11):
    prefix = 'E%s' % str(i)
    output.append(ssp + 'label="' + str(32110 + i) + '" type="lsep" />\n')
    idx = len(output)
    output.append(ssp + 'default="None" id="%s.type" label="32002" type="select" values="%s" />\n' % (prefix, evts))
    output.append(ssp + 'default="Task 1" id="%s.task" label="32095" type="select" visible="!eq(%s,None)" values="%s" />\n' %(prefix, getoffset(idx,output),tasks))
    for evtkey in allevts.keys():
        evt = allevts[evtkey]
        for req in evt['reqInfo']:
            r1 = req[1]
            if r1 in ['float', 'int']:
                r1 = 'number'
            output.append(ssp + 'default="%s" id="%s.%s" label="%s" type="%s" visible="eq(%s,%s)" />\n' % (req[2], prefix, req[0], req[0], r1, getoffset(idx,output), evt['text'] ))
        output.append(ssp + 'label="Hint - variables can be subbed (%%%%=%%): " type="lsep" visible="eq(%s,%s)" />\n' % (getoffset(idx,output), evt['text']))
        try:
            vargs = evt['varArgs']
        except:
            vargs = {}
        vs = ''
        for key in vargs.keys():
            vs += '%s=%s,' % (key, vargs[key])
        vs = vs[:-1]
        brk = 60
        if len(vs) < brk:
            output.append(ssp + 'label="%s" type="lsep" visible="eq(%s,%s)" />\n' % (vs, getoffset(idx,output), evt['text']))
        else:
            x = vs.rfind(',', 0, brk)
            output.append(ssp + 'label="%s" type="lsep" visible="eq(%s,%s)" />\n' % (vs[:x], getoffset(idx,output), evt['text']))
            output.append(ssp + 'label="%s" type="lsep" visible="eq(%s,%s)" />\n' % (vs[x+1:], getoffset(idx,output), evt['text']))
    output.append(ssp + 'default="" id="%s.userargs" label="Var subbed arg string" type="text" visible="!eq(%s,None)" />\n' % (prefix, getoffset(idx, output)))
    output.append(ssp + 'default="" id="%s.test" label="32009" type="action" action="RunScript($CWD/default.py, %s)" visible="!eq(%s,0)" />\n' % (prefix, prefix,getoffset(idx, output)))

output.append('  </category>\n')
output.append('  <category label="General">\n')
output.append('    <setting default="false" id="Notify" label="Display Notifications when Tasks Run?" type="bool" />\n')
output.append('    <setting default="500" id="LoopFreq" label="Loop Pooling Frequency (ms)" type="number" />\n')
output.append('    <setting default="500" id="LogFreq" label="Log Polling Frequency (ms)" type="number" />\n')
output.append('    <setting default="100" id="TaskFreq" label="Task Polling Frequency (ms)" type="number" />\n')
output.append('  </category>\n')
output.append('</settings>')
output = "".join(output)
print output