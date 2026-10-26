import win32com.client
import os

wdFormatPDF = 17
word = win32com.client.Dispatch('Word.Application')
word.Visible = False

f = 'NLP_MiniProject_Report_Kinjal_Ashish.docx'
src = os.path.abspath(f)
dst = src.replace('.docx', '.pdf')
doc = word.Documents.Open(src)
doc.SaveAs(dst, FileFormat=wdFormatPDF)
doc.Close(False)
print('PDF:', dst)

word.Quit()
print('done')
