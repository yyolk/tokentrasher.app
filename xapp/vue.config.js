process.env.VUE_APP_NAME = require('./package.json').name || 'tokentrasher.app'


module.exports = {
  devServer: {
    disableHostCheck: true
  }
}
