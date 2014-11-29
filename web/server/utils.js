module.exports = {

  validate: function (pass) {

    'use strict';

    if (!pass) return false;

    var
      result = true,
      test = function(value) {

        if (!result) {

          return false
        }
        if (value instanceof Array) {

          value.forEach(test);
          return result;

        }

        switch (value) {
          case 'l2tpd':
            result = true;
            break;
          case '*':
            result = true;
            break;
          default:
            var re = /^([a-zA-Z]|\d){6,32}$/;
            result = re.test(value);
            break;
        }
        if (!result) {

          console.log('Not valid: ' + value);
        }
        return result
      };

    test(pass);
    return result
  },
  
  l2tpReload: function () {
    
    'use strict';
    
  }
};
