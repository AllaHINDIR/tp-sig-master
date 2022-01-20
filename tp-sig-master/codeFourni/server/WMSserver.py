#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse


from codeFourni.server import reponse

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)

            # params contient tous les paramètres GET
            # Il faut maintenant les traiter...
            # ... C'est à vous !
            if 'request' not in params:
                self.send_error(404,'Parametres request manquant!')

            elif params['request'][0] != 'GetMap' :
                self.send_error(404,'Parametres request erroné!')
            elif 'bbox' not in params:
                self.send_error(404,'Parametres bbox manquant!')
            elif 'layers' not in params:
                self.send_error(404,'Parametres layers manquant!')
            elif 'height' not in params:
                self.send_error(404,'Parametres height manquant!')
            elif 'width' not in params:
                self.send_error(404,'Parametres width manquant!')
            elif 'srs' not in params:
                self.send_error(404,'Parametres srs manquant!')
                return
            if params['srs'][0] != 'EPSG:3857':
                self.send_error(404,'Parametres srs erroné!')

            bboxList = [float(t) for t in params['bbox'][0].split(',')]
            bbox = (bboxList[0], bboxList[1], bboxList[2], bboxList[3])

            width = int(params['width'][0])
            height = int(params['height'][0])

            srid = [int(temp) for temp in str(params['srs'][0]).split(":") if temp.isdigit()]
            print(bbox)
            print(params['layers'])
            # génération de l'image
            image = reponse.draw_tile(bbox, srid[0], width, height, params['layers'][0])
            if params['layers'][0] == "highway":
                imagename = "image1.png"
                image.save(imagename)
                self.send_png_image(imagename)
            elif params['layers'][0] == "building":
                imagename = "image2.png"
                image.save(imagename)
                self.send_png_image(imagename)
            return

        self.send_error(404, 'Fichier non trouvé : %s' % self.path)

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()

