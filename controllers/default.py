# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import pygal
from pygal.style import CleanStyle

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def products():
    return dict(message=T('Hello World!!'))

def specifications():
    return auth.wiki()

def good_reviews():
    return dict(message=T('Hello World!!'))

def bad_reviews():
    return dict(message=T('Hello World!!'))

def features():
    return dict(message=T('Hello World!!'))

def phone():
    return dict(message=T('Hello World!!'))

def profile():
    grid = SQLFORM.grid(db.register,user_signature=False)
    return locals()


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def register():
    form=SQLFORM(db.register, request.args(0))
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        abc=request.vars['user_name']
        redirect(URL('index', vars=dict(user=abc)))
    elif form.errors:
       response.flash = 'Please correct the error(s).'
    else:
       response.flash = 'Try again - no fields can be empty.'
    return dict(form=form)

def login():
    form = FORM(TABLE(TBODY(TR(TD(LABEL('User Name:'), _class="w2p_fl"),
              TD(INPUT(_name='name', requires=[IS_NOT_EMPTY(),IS_IN_DB(db, 'register.user_name')],), _class="w2p_fw")), _id="auth_user_email__row" ),
              TR(TD(LABEL('Password:'), _class="w2p_fw"),
              TD(INPUT(_name='password', _type='password', _class="input"))),_id="auth_user_password__row"),
              TR(TD(INPUT(_type='submit'),_class="btn"),_id="submit_record__row"))

    if form.accepts(request,session):
        name = request.vars['name']
        rows = db(db.register.user_name==name).select(db.register.password)
        for r in rows:
            actual_password = r.password
        typed_password = request.vars['password']
        if actual_password==typed_password:
            redirect(URL('index', vars=dict(user=name, password=actual_password)))
        else:
            redirect(URL('login'))
            response.flash = T("User Name and Password doesn't match")
    elif form.errors:
       response.flash = 'Please correct the error(s).'
    else:
       response.flash = 'Try again - no fields can be empty.'

    return dict(form=form)

def all_records():
      grid = SQLFORM.grid(db.register,user_signature=False)
      return locals()