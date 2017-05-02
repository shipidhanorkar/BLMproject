import os
import PyPDF2
import re

# import slate
# from tika import parser

path = '/Users/simply/Documents/BLM-workspace/blmdocumentexampleslong1'
#Path of other files that were tested
path = '/Users/simply/Documents/BLM-workspace/blmdocumentexampleslong2'
x = 0

os.chdir(path)
# pdfFileObj = open('BLM-2012-0001-7222_Number=7&di.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

dirs = os.listdir(path)
for file in dirs:
    # Technical support documents and petition preprocessing
    if file.endswith('.pdf'):
        #  assert isinstance(file,IOBase)
        print "******* File %s *******" % file
        fp = os.path.join(path, file)
        pdfFileObj = open(fp, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print ' This file has %d pages' % pdfReader.numPages
        type = []
        processed_flag = 0
        #  start with matching a long document:
        for i in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            pgtext = pageObj.extractText()
            #  if file in 'BLM-2013-0002-1093_Number=1&d.pdf':
            #     print pgtext
            # Not able to locate Table of Contents because perhaps it is in colored font.
            # More processing required
            match = (re.search('Table of Contents', pgtext) or
                     re.search('table of contents', pgtext) or
                     re.search('Table of contents', pgtext) or re.search('TABLE OF CONTENTS', pgtext) or re.search(
                'Contents', pgtext))
            if match:
                # it is indeed a long document
                # 2 cases not handled, colored text and table of contents possibly on right header
                print "   Table of Contents found on page %d" % i
                print "   Classify as a supporting document submitted by an organization"
                # print pgtext
                type.append('supporting doc')
                processed_flag = 1
                break
            else:
                match = (
                re.search('Appendix', pgtext) or re.search('Executive Summary', pgtext) or re.search('Key Findings',
                                                                                                     pgtext))
                if match:
                    print '   Appendix|Executive Summary| Key Findings string found on page %d' % i
                    print "   Classify as a supporting document submitted by an organization"
                    type.append('supporting doc')
                    processed_flag=1
                    x = i
                    break
        pdfFileObj.close()

        if processed_flag == 0:
            # not a long doc, check if it is a petition format
            print " Did not find a table of contents"
            # with open(fp) as f:                    # slate implementation : unresolved import error with pdfminer
            #    doc = slate.PDF(f)
            #    print doc[0]
            # parsedPDF = parser.from_file(fp)        # tika implementation unresolved connection error
            # parsedPDF["content"]
            for i in range(0, pdfReader.numPages):
                pgtext = ""
                start = []
                pageObj = pdfReader.getPage(i)
                print(pageObj.extractText())  # for some pdf's contains empty string
                pgtext = pageObj.extractText()
                print pgtext
                start = re.search('Dear',pgtext) or re.search('Dear Sir',pgtext) or re.search(
                    '[t|T]o.*[w|W]hom.*[i|I]t.*[m|M]ay.*[c|C]oncern', pgtext)
                end = pgtext.find('Sincerely')
                print "Start value is:"
                print start
                print "End value is:"
                print end
                if (start==None) and (end == -1):
                    if i == 0:
                        print " No matching"
                        print "possibly a different format."
                        break
                elif (start != None) and (end == -1):
                    if i == 0:
                        print " Found only start"
                        print "Possibly a collection of petitions from multiple people. Additional Analysis required."
                        break
                elif (start == None) and (end != -1):
                    if i == 0:
                        print " Found only end"
                        print "Possibly a collection of petitions from multiple people. Additional Analysis required."
                        break
                else:
                    print "Found start and end on same page"
                    print "Classifying as a collection of petitions from multiple people"
                    break

                    # # matching = (((re.search('Dear', pgtext) or (re.search('Dear Sir', pgtext)) or
                    # #            re.search('dear', pgtext) or
                    # #            re.search('To', pgtext) or re.search('to', pgtext)) or
                    # #            re.search('[t|T]o [w|W]hom [i|I]t [m|M]ay [c|C]oncern',pgtext)) and
                    # #            (re.search('sincerely',pgtext) or re.search('Sincerely',pgtext)))
                    # if matching:
                    #     # a petition long document in the form of multiple letters
                    #     print 'Dear and Sincerely found on the same page %d' %i
                    #     print "Maybe a long document in the form of petition letters"
                    #     petitionLetter.append(pgtext) #store letter
                    #     print (petitionLetter)
                    #     #print petitionLetter.count()
                    #     #print pgtext
                    #     #startbody=pgtext.find("Dear")
                    #     #endbody=pgtext.find("Sincerely")
                    #     #letterbody=pgtext[startbody+4:endbody]
                    #     #print letterbody
                    #     processed_flag=1
                    #     break
                    # if i==0 and matching == None and pdfReader.numPages >3:
                    #     foreword=pgtext
                    #     print foreword
                    # elif matching is not -1 and i ==0:
                    #     print "Match for dear on page %d"%i
                    # # matching = (((re.search('Dear', pgtext) or (re.search('Dear Sir', pgtext)) or
                    # #            re.search('dear', pgtext) or
                    # #            re.search('To', pgtext) or re.search('to', pgtext)) or
                    # #            re.search('[t|T]o [w|W]hom [i|I]t [m|M]ay [c|C]oncern',pgtext)) and
                    # #            (re.search('sincerely',pgtext) or re.search('Sincerely',pgtext)))
                    # if matching:
                    #     # a petition long document in the form of multiple letters
                    #     print 'Dear and Sincerely found on the same page %d' %i
                    #     print "Maybe a long document in the form of petition letters"
                    #     petitionLetter.append(pgtext) #store letter
                    #     print (petitionLetter)
                    #     #print petitionLetter.count()
                    #     #print pgtext
                    #     #startbody=pgtext.find("Dear")
                    #     #endbody=pgtext.find("Sincerely")
                    #     #letterbody=pgtext[startbody+4:endbody]
                    #     #print letterbody
                    #     processed_flag=1
                    #     break
                    # if i==0 and matching == None and pdfReader.numPages >3:
                    #     foreword=pgtext
                    #     print foreword
                    # print("Number of petition comments in the doc are %d" %len(petitionLetter))
    else:
        print "%s not a pdf, file needs different processing" % file
