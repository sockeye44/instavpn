module.exports = function(root) {

  var
    env = process.env.NODE_ENV || 'development',
    path = require('path'),
    fs = require('fs')
    ;

  root = path.normalize(root || __dirname + '/../..');

  return {
    env: env,
    host: '0.0.0.0',
    port: 8080,
    path: {
      root: root,
      www: root + '/public',
      upload: root + '/public/upload/',
      route: __dirname + '/route',
      views: __dirname + '/views'
    },
    i18n: {
      locales: ['en', 'ru', 'zh_CN' ,'zh_TW'],
      defaultLocale: 'en',
      directory: __dirname + '/locales'
    },
    file: {
      psk: '/etc/ipsec.secrets',
      chap: '/etc/ppp/chap-secrets'
    },
    admin: JSON.parse(fs.readFileSync(__dirname + '/credentials.json')).admin
  }
};