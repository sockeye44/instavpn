var
  config = require('./server/config')(__dirname),
  express = require('express'),
  app = express(),
  cookieParser = require('cookie-parser'),
  bodyParser = require('body-parser'),
  flash = require('connect-flash'),
  md5 = require('MD5'),
  session = require('express-session'),
  bouncer = require('express-bouncer')(),
  i18n = require('i18n')
;

app.set('config', config);
app.set('views', config.path.views);
app.set('view engine', 'jade');

i18n.configure(config.i18n);

bouncer.blocked = function (req, res, next, remaining) {

    req.flash("error", res.__("Too many requests, please wait %s seconds", "" + (remaining / 1000).toFixed(0)));
    res.redirect('/');
};
app.use(express.static(config.path.www));
app.use(bodyParser.urlencoded({extended: true}));
app.use(cookieParser());
app.use(i18n.init);
app.use(flash());
app.use(session({
  secret: md5(Math.floor(Math.random() * (2000000000 - -2000000000 + 1) + -2000000000)),
  saveUninitialized: true, // (default: true)
  resave: true // (default: true)
}));
require(config.path.route)(app, bouncer);
app.listen(config.port, config.host);