# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('mysql://root:neo&trinity@localhost/phone_reviews',pool_size=1,check_reserved=['all'])
    db1 = DAL('mysql://root:neo&trinity@localhost/training_data',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    db1 = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db.define_table('register',
    Field('first_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()],),
    Field('last_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
    Field('user_name', unique=True, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
    Field('email', unique=True, requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
    Field('password', 'password', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(), ]),
    migrate=False)
db.register.email.requires=IS_NOT_IN_DB(db,'register.email')
db.register.user_name.requires=IS_NOT_IN_DB(db,'register.user_name')

db.define_table('product_list',
    Field('imageUrl'),
    Field('description'),
    Field('name'),
    Field('link'),
    Field('manufacturer'),
    migrate=False)

db.define_table('manufacturer',
    Field('name'),
    migrate=False)

db.define_table('reviews',
    Field('user_name'),
    Field('dates'),
    Field('manufacturer_id'),
    Field('phone_id'),
    Field('review'),
    Field('types'),
    migrate=False)

db.define_table('phone_id',
    Field('name'),
    Field('manufacturer_id'),
    Field('good'),
    Field('bad'),
    Field('rating'),
    migrate=False)

db.define_table('specifications',
    Field('phone_id'),
    Field('DeviceType'),
    Field('OS'),
    Field('Dimensions'),
    Field('Weight'),
    Field('PhysicalSize'),
    Field('Resolution'),
    Field('UMTS'),
    Field('Accessories'),
    Field('Capacity'),
    Field('Notifications'),
    Field('Speakers'),
    Field('Features'),
    Field('StandbyTime'),
    Field('Datas'),
    Field('BodyMaterial'),
    Field('Navigations'),
    Field('WirelessCharging'),
    Field('GSM'),
    Field('Colors'),
    Field('MicroSim'),
    Field('Talktime'),
    Field('YoutubePlayer'),
    Field('Other'),
    migrate=False)

db.define_table('phone_images',
    Field('phone_id'),
    Field('images'),
    migrate=False)

db1.define_table('doc_frequency',
    Field('words'),
    Field('total'),
    migrate=False)

db1.define_table('negative_words',
    Field('words'),
    Field('frequency'),
    migrate=False)

db1.define_table('positive_words',
    Field('words'),
    Field('frequency'),
    migrate=False)
