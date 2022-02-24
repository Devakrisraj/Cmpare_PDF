from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request,'pdfcompare.html')
print ('Initial')
def pdfcompare(request):
    print ('bf-post')
    if request.method == 'POST' and request.FILES['file1'] and request.FILES['file2']:
        print ('aft-post')
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        print ('file1= ',file1)
        fs = FileSystemStorage()
        filename1 = fs.save(file1.name, file1)
        filename2 = fs.save(file2.name, file2)
        uploaded_file_url = fs.url(filename1)
        print ('filename1= ',filename1)
    #if request.method == 'POST' and request.FILES['file2']:
     #   file2 = request.FILES.get('file2')
      #  print ('file1= ',file1)
       # fs = FileSystemStorage()
        #filename2 = fs.save(file2.name, file2)
        #uploaded_file_url2 = fs.url(filename2)
        #print ('filename2= ',filename2)
    
    from skimage.measure import compare_ssim
    import argparse
    import imutils
    import cv2
    import os
    from pdf2image import convert_from_path
    import PIL
    from PIL import Image
    import img2pdf
#    from gtts import gTTS
#   import os
#    from django.conf import settings
#    import os
    
#    from datetime import datetime
    
#    savfile = datetime.now().strftime('%Y%m%d%H%M%S')    
    
    base_dir =settings.MEDIA_ROOT
    pdf_file1 = os.path.join(base_dir, str(file1))
        
    pages = convert_from_path(pdf_file1,"",poppler_path=r'C:\Users\dkrishna\.spyder-py3\poppler-0.68.0\bin')
    img_file1 = pdf_file1.replace(".pdf","")
    count = 0
    for page in pages:
        count +=1
        jpeg_file1 = img_file1 + "." + str(count) + ".jpeg"
        page.save(jpeg_file1, 'JPEG')

    pdf_file2 = os.path.join(base_dir, str(file2))
    
    pages = convert_from_path(pdf_file2,"",poppler_path=r'C:\Users\dkrishna\.spyder-py3\poppler-0.68.0\bin')
    img_file2 = pdf_file2.replace(".pdf","")
    count = 0
    for page in pages:
        count +=1
        jpeg_file2 = img_file2 + "." + str(count) + ".jpeg"
        page.save(jpeg_file2, 'JPEG')

    print ('bf-cv2')
    count = 0
    for page in pages:
        count +=1
        imgA = (img_file1 + "." + str(count) + ".jpeg")
        imgB = (img_file2 + "." + str(count) + ".jpeg")
        imageA = cv2.imread(img_file1 + "." + str(count) + ".jpeg")
        imageB = cv2.imread(img_file2 + "." + str(count) + ".jpeg")
#        imageA = cv2.imread(jpeg_file1)
#        imageB = cv2.imread(jpeg_file2)
# convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
#
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))
        print("test")
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        print("test1")
# loop over the contours
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
#        
        cjpegA = ("Original"  + str(count) + ".jpeg")
        cjpegB = ("Modified"  + str(count) + ".jpeg")
        print ("cjpegA: ", cjpegA)
        print ("cjpegB: ", cjpegB)
        cv2.imwrite(cjpegA, imageA)
        cv2.imwrite(cjpegB, imageB)
        cv2.waitKey(0)
#
    os.chdir('C:\\Users\\dkrishna\\.spyder-py3\\compare')
    
    with open("Original.pdf","wb") as f:
        f.write(img2pdf.convert([x for x in os.listdir(".") if (x.startswith("Original") and x.endswith(".jpeg"))]))
#
    with open("Modified.pdf","wb") as f:
        f.write(img2pdf.convert([x for x in os.listdir(".") if (x.startswith("Modified") and x.endswith(".jpeg"))]))
#
    base_dir =settings.TEMPLATE_ROOT
    os.chdir(base_dir)
    return render(request, 'pdfcompare.html', {
            'uploaded_file_url': uploaded_file_url
            })  
# show the output images
#cv2.imshow("Original", imageA)
#cv2.imshow("Modified", imageB)
#cv2.waitKey(0)
#directory = r'C:\Users\dkrishna\Desktop'
#os.chdir(directory)
#Original = 'original.jpg'
#Modified = 'modified.jpg'
#
# Below codes are used in previously
#    base_dir =settings.MEDIA_ROOT
#    os.chdir(base_dir)
#    cv2.imwrite("Original.jpeg", imageA)
#    cv2.imwrite("Modified.jpeg", imageB)
#    cv2.waitKey(0)
#    
#    image1 = Image.open("Original.jpeg")
#    image2 = Image.open("Modified.jpeg")
#        
#    if image1.mode == "RGBA":
#        image1 = image.convert("RGB")
#
#    Original = "Original.pdf"
#
#    if not os.path.exists(Original):
#        image1.save(Original,"PDF",resolution=100.0)
#
#    if image2.mode == "RGBA":
#        image2 = image.convert("RGB")
#
#    Modified = "Modified.pdf"
#
#    if not os.path.exists(Modified):
#        image2.save(Modified,"PDF",resolution=100.0)
#    base_dir =settings.TEMPLATES
#    base_dir =settings.TEMPLATE_ROOT
#    os.chdir(base_dir)
#    return render(request, 'pdfcompare.html', {
#            'uploaded_file_url': uploaded_file_url
#            })    
#    return render(request, 'pdfcompare.html', {
#               uploaded_file_url1': uploaded_file_url1})
#    fh = open(txtfile,"r")
#    text = fh.read().replace("\n", " ")
#    print ('fh.read')
#    print (text)
#    
#    print ('Dest_Lang:', dl)
#    translator = Translator()
#    dt = translator.detect(text)
#    dtsl = dt.lang
#    print ('dtsl:', dtsl)
#    translated = translator.translate(text,dl)
#    output = translated.text
#    print ('Output:', output)
#    resultfile = os.path.join(base_dir,("%s.txt") % str(savfile))
#    print ('resultfile:', resultfile)
#    with open(resultfile, 'w', encoding='utf-8') as f:
#        f.write(output)
  #  output.save(os.path.join(base_dir,("%s.txt") % (savfile)))
#    print ('Close-Prev:')
#    fh.close()
#    print ('Close-Aft:')
#   return render(request, 'pdfcompare.html', {
#            uploaded_file_url1': uploaded_file_url1})
#return render(request, 'pdfcompare.html', {
#            'uploaded_file_url2': uploaded_file_url2
#        })