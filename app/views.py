from django.shortcuts import render
import qrcode
import qrcode.image.svg
from io import BytesIO
import cv2

def qRoku(name):
    img= cv2.imread(f"media/{name}")
    det=cv2.QRCodeDetector()
    val, pts, st_code=det.detectAndDecode(img)
    return val

# gelen qr code i kaydet
def handle_uploaded_file(f):
    name = f.name
    with open(f"media/{name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    context = {}
    if request.method == 'POST':
        
        # text to qrcode
        if  request.FILES.get('qr_file'):
            name =  request.FILES['qr_file'].name
            print("name: ", name)
            # qr_code yazma
            handle_uploaded_file(request.FILES['qr_file'])
        
            # yazılan qr kodu okuma
            sonuc = qRoku(request.FILES['qr_file'].name)
            print("sonuc ",sonuc)

            # qr code okunamazsa
            if len(sonuc) < 1:
                sonuc = "Qr Code Bozuk"

            return render(request, "index.html",{"sonuc": sonuc})

        # qr_code image  to text
        elif request.POST.get("qr_text"):
            if len(request.POST.get('qr_text')) > 7089:
                print("çok uzun")
            else:
                print("qr_text geldi: ")
                factory = qrcode.image.svg.SvgImage
                img = qrcode.make(request.POST.get("qr_text", ""),
                image_factory=factory, box_size=20)
                stream = BytesIO()
                img.save(stream)
                context["svg"] = stream.getvalue().decode()
            return render(request, "index.html", context=context)


          
    return render(request, "index.html", context=context)
