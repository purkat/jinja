#!/usr/bin/env python
import os
import jinja2
import webapp2

from datetime import datetime

import program

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        params = {"sporocilo": "Tukaj sem tudi jaz, MainHandler"}
        self.render_template("hello.html", params=params)

    def post(self):
        moj_tekst = "Uporabnik je vpisal: "
        vsebina_input_polja_z_imenom_moje_vnosno_polje = self.request.get("moje_vnosno_polje")
        skupaj = program.sestej(moj_tekst, vsebina_input_polja_z_imenom_moje_vnosno_polje)
        izhodni_podatki = {
            "sporocilo" : skupaj
        }

        self.render_template("hello.html", params=izhodni_podatki)


class CasHandler(BaseHandler):
    def get(self):
        params = {"sporocilo": datetime.now()}
        self.render_template("hello.html", params=params)

class SiHandler(BaseHandler):
    def get(self):
        params = {
            "naslov": "SmartNinja osnovna Jinja predloga",
            "pozdrav": "Zivjo, SmartNinja!",
            "sporocilo": datetime.now()
        }
        self.render_template("jeziki.html", params=params)

class EnHandler(BaseHandler):
    def get(self):
        params = {
            "naslov": "SmartNinja basic Jinja template",
            "pozdrav": "Hello, SmartNinja!",
            "sporocilo": datetime.now()
        }
        self.render_template("jeziki.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/cas', CasHandler),
    webapp2.Route('/si', SiHandler),
    webapp2.Route('/en', EnHandler)
], debug=True)
