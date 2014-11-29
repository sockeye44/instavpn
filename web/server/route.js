require('shelljs/global');
module.exports = function (app, bouncer) {
    'use strict';

    var
      fs = require('fs');

    app.get('/', function (req, res) {

      res.render('index', {message: req.flash('error')});
    });

    app.get('/panel', function (req, res) {

      if (typeof req.session.username == 'undefined') {

        req.flash('error', res.__('Your session has expired. Please log in again'));
        res.redirect('/');
        return
      }

      fs.readFile(app.get('config').file.psk, 'utf8', function (err, psk) {

        if (err) {
          psk = psk || '';
          console.log(err)
        }
        psk = psk.split("\n")[0].split('"');
        psk = psk[psk.length - 2];

        fs.readFile(app.get('config').file.chap, 'utf8', function (err, chap) {

          if (err) {
            chap = chap || '';
            console.log(err)
          }
          var users = [], clean = [{'username': '','password': ''}];

          chap.split("\n").forEach(function(ch){
            var
              tmp = ch.split(' ')
              ;
            users.push({'username': tmp[0],'password': tmp[2]})
          });

          if (!users.length) {
            users.push(clean)
          }

          res.render('panel', {
              psk: psk,
              users: users,
              hiddenUser: clean,
              error: req.flash('panel-error'),
              message: req.flash('panel-message')
          });

        });

      });

    });

    app.post('/panel', function (req, res) {

      if (typeof req.session.username == 'undefined') {

        req.flash('error', res.__('Your session has expired. Please log in again'));
        res.redirect('/');
        return
      }

      var
        utils = require('./utils');

      if (req.body.psk) {
        if (!(
            utils.validate(req.body.psk)
          )) {

          req.flash('panel-error', res.__('All fields must contain alphanumeric characters only and have length between 6 and 32'));
          res.redirect('/panel#users');
          return
        }

        fs.writeFile(app.get('config').file.psk, 'IP.ADDR %any: PSK "' + req.body.psk + '"', function (err) {

          if (err) {
            console.log(err)
          }
          req.flash('panel-message', res.__('Ok'));
        });
      }

      if (req.body.users) {

        if (!(
            utils.validate(req.body.users)
          )) {

          req.flash('panel-error', res.__('All fields must contain alphanumeric characters only and have length between 6 and 32'));
          res.redirect('/panel#users');
          return
        }
        var
          chap = [];

        req.body.users.forEach(function(value){

          if (value instanceof Array) {
            var
              line = []
              ;
            value.forEach(function(val) {
              line.push(val)
            });
            chap.push(line.join(" "))

          } else {

            chap.push(value)
          }
        });
        var
          glue = ' '
        ;
        if (chap.length > 1) {
          glue = "\n"
        }
        fs.writeFile(app.get('config').file.chap, chap.join(glue), function (err) {

          if (err) {
            console.log(err);
          }

          console.log(exec('/etc/init.d/ipsec restart && /etc/init.d/xl2tpd restart', {silent:true}).output);

          req.flash('panel-message', res.__('Ok'));
        });

      }
      res.redirect('/panel#users');

    });

    app.post('/', bouncer.block, function (req, res) {

      if ((
        req.body.user === app.get('config').admin.login) &&
        (req.body.password === app.get('config').admin.password)
      ) {

        req.session.authorized = true;
        req.session.username = app.get('config').admin.login;
        req.session.cookie.expires = new Date(Date.now() + 3600000);//hour
        console.log(req.connection.remoteAddress + ' authorized');
        bouncer.reset(req);
        res.redirect('/panel');
      }
      else {

        req.flash('error', res.__('Incorrect password'));
        res.redirect('/');
      }
    });

    app.get('/logout', function (req, res) {

      req.session.destroy();
      res.redirect('/');
    });
};