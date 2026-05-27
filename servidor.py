from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from get_query import *
from tables import *
from error import *
HOST_ADDRESS = "127.0.0.1"
HOST_PORT = 21080

class RequestHandler(BaseHTTPRequestHandler):
    def set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        try:
            msg = msg_error_servidor
            if (self.path == "/index.html" or self.path == "/"):
                self.set_response(200)
                with open('index.html', 'r', encoding='utf-8') as archivo:
                    msg = archivo.read()

            elif (self.path == "/author"):
                self.set_response(200)
                with open("autor.html", "r", encoding="utf-8") as archivo:
                    msg = archivo.read()

            elif (self.path.startswith("/searchTarget?id=")):
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                idTarget = query_components["id"]
                dict_target = get_query_target(idTarget)
                lines, diseases_json = tabla_target(dict_target)
                if ((not dict_target) or lines == ""):
                    msg = msg_incorrect_query
                    self.set_response(404)
                else:
                    self.set_response(200)                
                    with open("targetresults.html", "r", encoding="utf-8") as fichero:
                        contenido_html = fichero.read()
                        msg = contenido_html.replace("{lines}", lines).replace("{id}", idTarget).replace("{results.json}", "diseases_associated.json").replace("{json}", json.dumps(diseases_json))

                        
            elif (self.path.startswith("/searchDisease?id=")):
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                idDisease = query_components["id"]
                dict_disease = get_query_disease(idDisease)
                lines, targets_json = tabla_disease(dict_disease)
                if ((not dict_disease) or lines == ""):
                    msg = msg_incorrect_query
                    self.set_response(404)
                else:
                    self.set_response(200)
                    with open("diseaseresults.html", "r", encoding="utf-8") as fichero:
                            contenido_html = fichero.read()
                            msg = contenido_html.replace("{lines}", lines).replace("{id}", idDisease).replace("{results.json}", "Targets_associated.json").replace("{json}", json.dumps(targets_json))
                        
            elif (self.path.startswith("/results")):
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                query_target = query_components["target"]
                query_disease = query_components["disease"]
                query_score = query_components["score"]
                if query_target  == "" and query_disease == "":
                    self.set_response(404)
                    self.send_header("Location","/")
                    self.end_headers()
                    msg = msg_not_enter_query
                
                elif query_target != "" and query_disease == "":
                    dict_diseases_asociated = get_diseases_asociated(query_target)
                    lines, association_json = table_diseases_associated(dict_diseases_asociated, float(query_score))
                    if ((not dict_diseases_asociated) or lines == ""):
                        msg = msg_incorrect_query
                        self.set_response(404)
                    else: 
                        self.set_response(200)
                        with open("results.html", "r", encoding="utf-8") as file:
                            content_html = file.read()
                            msg = content_html.replace("{lines}", lines).replace("{json}", json.dumps(association_json)).replace("{results.json}","Target.json").replace("{Id}",query_target)
                            
                elif query_target == "" and query_disease != "":
                    dict_targets_asociated = get_targets_asociated(query_disease)
                    lines, association_json = table_targets_asociated(dict_targets_asociated, float(query_score))
                    if ((not dict_targets_asociated) or lines == ""):
                        msg = msg_incorrect_query
                        self.set_response(404)
                    else:
                        self.set_response(200)
                        with open("results.html", "r", encoding="utf-8") as file:
                            content_html = file.read()
                            msg = content_html.replace("{lines}", lines).replace("{json}", json.dumps(association_json)).replace("{results.json}", "Disease.json").replace("{Id}",query_disease)
                            
                elif query_target !="" and query_disease != "":
                    dict_associations = get_query_association(query_target, query_disease)
                    lines, association_json = association_table(dict_associations, float(query_score))
                    if ((not dict_associations) or lines) == "":
                        msg = msg_incorrect_query
                        self.set_response(404)
                    else:
                        self.set_response(200)
                        with open("results.html", "r", encoding="utf-8") as file:
                            content_html = file.read()
                            msg = content_html.replace("{lines}", lines).replace("{json}", json.dumps(association_json)).replace("{results.json}", "Association.json").replace("{Id}", query_target+" and "+query_disease)
                        
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    msg = msg_not_associations
    
            else:
                msg = msg_notfound
                self.set_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
            self.wfile.write(msg.encode('utf-8'))
        except Exception:
            if msg == msg_error_servidor:
                msg = msg_error_servidor
                self.set_response(500)
                
            self.wfile.write(msg.encode('utf-8'))

    def do_POST(self):
    
        if self.path == "/results":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            self.path = f"/results?{post_data}"
            self.do_GET()
        
        

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """ follows example shown on docs.python.org """
    server_address = (HOST_ADDRESS, HOST_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=RequestHandler)