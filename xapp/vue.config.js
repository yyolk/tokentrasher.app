process.env.VUE_APP_NAME = require('./package.json').name || 'tokentrasher.app'


module.exports = {
  devServer: {
    disableHostCheck: true,
    proxy: "https://7rasy4a4dh.execute-api.us-east-1.amazonaws.com",
    // headers: { "Authorization": "" },
  }
}
